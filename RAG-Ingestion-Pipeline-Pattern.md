---
tags:
  - azure
  - ai-200
  - container-apps
  - keda
  - rag
  - cosmos-db
  - event-grid
  - service-bus
  - openai
created: 2026-04-17
status: reference
---

# RAG Document Ingestion Pipeline — End to End

## Overview

A complete event-driven document ingestion pipeline for Retrieval-Augmented Generation (RAG). Covers core AI-200 exam objectives: containerized compute, event-driven pipelines, vector-enabled databases, secret management, scale-to-zero, and distributed observability.

### Architecture Flow

```
User uploads PDF
  → Azure Blob Storage (uploads container)
    → Event Grid (BlobCreated event)
      → Service Bus Queue (doc-ingestion)
        → Container App Worker (KEDA-scaled, 0→N replicas)
          ├── Download blob from Storage
          ├── Chunk text (sliding window)
          ├── Generate embeddings (Azure OpenAI)
          └── Write vectors to Cosmos DB
              → Queue empty → scale back to 0
                → Application Insights traces every step
```

### AI-200 Objectives Covered

| Objective | Implementation |
|---|---|
| Containerized compute | Docker + ACR + Container Apps |
| Event-driven AI pipelines | Event Grid → Service Bus → KEDA worker |
| Vector-enabled databases | Cosmos DB with vector index + cosine similarity |
| Secret management | Container App `secretref:` pattern |
| Scale-to-zero / serverless | `minReplicas: 0` + KEDA Service Bus scaler |
| Distributed observability | Application Insights linked to ACA environment |

---

## Step 1 — Provision Infrastructure

```bash
# Variables
RG="rg-rag-pipeline"
LOCATION="eastus"
STORAGE="stragpipeline$RANDOM"
SB_NS="sb-rag-pipeline"
ACR="acrragpipeline"
ACA_ENV="env-rag-pipeline"
COSMOS_ACCT="cosmos-rag-pipeline"

# Resource group
az group create --name $RG --location $LOCATION

# Storage account + container (user upload target)
az storage account create --name $STORAGE --resource-group $RG \
  --location $LOCATION --sku Standard_LRS

az storage container create --name uploads \
  --account-name $STORAGE

# Service Bus namespace + queue (decouples upload from worker)
az servicebus namespace create --name $SB_NS \
  --resource-group $RG --location $LOCATION --sku Standard

az servicebus queue create --name doc-ingestion \
  --namespace-name $SB_NS --resource-group $RG

# Azure Container Registry (stores worker image)
az acr create --name $ACR --resource-group $RG \
  --sku Basic --admin-enabled true

# Container Apps environment
az containerapp env create --name $ACA_ENV \
  --resource-group $RG --location $LOCATION
```

---

## Step 2 — Wire Blob → Service Bus via Event Grid

No code required. Event Grid handles the routing automatically.

```bash
# Get resource IDs
STORAGE_ID=$(az storage account show --name $STORAGE \
  --resource-group $RG --query id -o tsv)

SB_QUEUE_ID=$(az servicebus queue show --name doc-ingestion \
  --namespace-name $SB_NS --resource-group $RG --query id -o tsv)

# Create Event Grid subscription
az eventgrid event-subscription create \
  --name blob-to-servicebus \
  --source-resource-id $STORAGE_ID \
  --endpoint-type servicebusqueue \
  --endpoint $SB_QUEUE_ID \
  --included-event-types Microsoft.Storage.BlobCreated \
  --subject-begins-with /blobServices/default/containers/uploads
```

> **Key concept:** Event Grid is the glue between Blob Storage and Service Bus. The queue acts as a durable buffer — if the worker is scaled to zero, messages wait until KEDA spins replicas up.

---

## Step 3 — Worker Application

### `worker.py`

```python
import os
import json
import time
import logging
from azure.servicebus import ServiceBusClient
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
from azure.cosmos import CosmosClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# All config injected via Container App env vars / secrets
SB_CONNECTION    = os.environ["SERVICEBUS_CONNECTION"]
SB_QUEUE         = os.environ["SERVICEBUS_QUEUE"]
STORAGE_CONN     = os.environ["STORAGE_CONNECTION"]
COSMOS_URL       = os.environ["COSMOS_URL"]
COSMOS_KEY       = os.environ["COSMOS_KEY"]
COSMOS_DB        = os.environ["COSMOS_DB"]
COSMOS_CONTAINER = os.environ["COSMOS_CONTAINER"]
AOAI_ENDPOINT    = os.environ["AOAI_ENDPOINT"]
AOAI_KEY         = os.environ["AOAI_KEY"]
EMBED_MODEL      = "text-embedding-3-small"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Naive sliding window chunker over word tokens."""
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


def get_embeddings(client: AzureOpenAI, chunks: list[str]) -> list[list[float]]:
    response = client.embeddings.create(model=EMBED_MODEL, input=chunks)
    return [item.embedding for item in response.data]


def process_message(msg_body: dict):
    blob_name = msg_body["subject"].split("/blobs/")[-1]
    logger.info(f"Processing blob: {blob_name}")

    # 1. Download blob
    blob_client = BlobServiceClient.from_connection_string(STORAGE_CONN)
    blob = blob_client.get_blob_client(container="uploads", blob=blob_name)
    raw_text = blob.download_blob().readall().decode("utf-8")

    # 2. Chunk
    chunks = chunk_text(raw_text)
    logger.info(f"Created {len(chunks)} chunks")

    # 3. Embed via Azure OpenAI
    aoai = AzureOpenAI(azure_endpoint=AOAI_ENDPOINT, api_key=AOAI_KEY, api_version="2024-02-01")
    embeddings = get_embeddings(aoai, chunks)

    # 4. Write to Cosmos DB (vector items)
    cosmos = CosmosClient(COSMOS_URL, COSMOS_KEY)
    container = cosmos.get_database_client(COSMOS_DB).get_container_client(COSMOS_CONTAINER)

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        container.upsert_item({
            "id": f"{blob_name}-chunk-{i}",
            "source": blob_name,
            "chunk_index": i,
            "content": chunk,
            "embedding": embedding        # Cosmos DB vector field
        })

    logger.info(f"Wrote {len(chunks)} vectors to Cosmos DB")


def main():
    logger.info("Worker started, polling Service Bus...")
    with ServiceBusClient.from_connection_string(SB_CONNECTION) as sb_client:
        with sb_client.get_queue_receiver(SB_QUEUE, max_wait_time=10) as receiver:
            while True:
                messages = receiver.receive_messages(max_message_count=1, max_wait_time=10)
                if not messages:
                    logger.info("No messages. Waiting...")
                    time.sleep(5)
                    continue

                for msg in messages:
                    try:
                        body = json.loads(str(msg))
                        process_message(body)
                        receiver.complete_message(msg)   # Remove from queue on success
                    except Exception as e:
                        logger.error(f"Failed: {e}")
                        receiver.abandon_message(msg)    # Returns to queue for retry


if __name__ == "__main__":
    main()
```

### `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .

CMD ["python", "worker.py"]
```

### `requirements.txt`

```
azure-servicebus
azure-storage-blob
azure-identity
azure-cosmos
openai
```

---

## Step 4 — Build and Push to ACR

```bash
az acr build --registry $ACR \
  --image rag-worker:latest .
```

---

## Step 5 — Deploy Container App with KEDA Scaling

```bash
# Gather credentials
ACR_SERVER=$(az acr show --name $ACR --query loginServer -o tsv)
ACR_USER=$(az acr credential show --name $ACR --query username -o tsv)
ACR_PASS=$(az acr credential show --name $ACR --query passwords[0].value -o tsv)

SB_CONN_STR=$(az servicebus namespace authorization-rule keys list \
  --name RootManageSharedAccessKey \
  --namespace-name $SB_NS \
  --resource-group $RG \
  --query primaryConnectionString -o tsv)

# Deploy
az containerapp create \
  --name rag-worker \
  --resource-group $RG \
  --environment $ACA_ENV \
  --image "$ACR_SERVER/rag-worker:latest" \
  --registry-server $ACR_SERVER \
  --registry-username $ACR_USER \
  --registry-password $ACR_PASS \
  --cpu 1 --memory 2Gi \
  --min-replicas 0 \
  --max-replicas 10 \
  --secrets \
      "sb-conn=$SB_CONN_STR" \
      "storage-conn=$STORAGE_CONN_STR" \
      "cosmos-key=$COSMOS_KEY_VALUE" \
      "aoai-key=$AOAI_KEY_VALUE" \
  --env-vars \
      "SERVICEBUS_CONNECTION=secretref:sb-conn" \
      "SERVICEBUS_QUEUE=doc-ingestion" \
      "STORAGE_CONNECTION=secretref:storage-conn" \
      "COSMOS_URL=$COSMOS_URL" \
      "COSMOS_KEY=secretref:cosmos-key" \
      "COSMOS_DB=rag-db" \
      "COSMOS_CONTAINER=documents" \
      "AOAI_ENDPOINT=$AOAI_ENDPOINT" \
      "AOAI_KEY=secretref:aoai-key" \
  --scale-rule-name servicebus-scaler \
  --scale-rule-type azure-servicebus \
  --scale-rule-metadata "queueName=doc-ingestion" "messageCount=5" \
  --scale-rule-auth "connection=sb-conn"
```

> **KEDA scaling math:** `desired replicas = ceil(queue depth / messageCount)`
> - 0 messages → 0 replicas
> - 25 messages → 5 replicas (`ceil(25/5)`)
> - 100 messages → 10 replicas (capped at `maxReplicas`)

---

## Step 6 — Cosmos DB Vector Index

Set this on the container's indexing policy to enable vector similarity search.

```json
{
  "vectorEmbeddingPolicy": {
    "vectorEmbeddings": [
      {
        "path": "/embedding",
        "dataType": "float32",
        "dimensions": 1536,
        "distanceFunction": "cosine"
      }
    ]
  },
  "indexingPolicy": {
    "vectorIndexes": [
      {
        "path": "/embedding",
        "type": "quantizedFlat"
      }
    ]
  }
}
```

> **Note:** `dimensions: 1536` matches `text-embedding-3-small`. Use `3072` for `text-embedding-3-large`. `quantizedFlat` is suitable for moderate dataset sizes; use `diskANN` for large-scale production.

---

## Step 7 — Observability (Application Insights)

```bash
# Create App Insights resource
az monitor app-insights component create \
  --app rag-pipeline-insights \
  --resource-group $RG \
  --location $LOCATION \
  --kind web

# Get instrumentation key
APPINSIGHTS_KEY=$(az monitor app-insights component show \
  --app rag-pipeline-insights \
  --resource-group $RG \
  --query instrumentationKey -o tsv)

# Link to Container Apps environment
az containerapp env update \
  --name $ACA_ENV \
  --resource-group $RG \
  --logs-workspace-id $APPINSIGHTS_KEY
```

Add `opencensus-ext-azure` to `requirements.txt` and wrap `process_message()` in a trace span to get per-document latency breakdowns across chunking, embedding, and Cosmos writes.

---

## Key Concepts to Lock In

### Secret Management Pattern
Secrets are stored on the Container App, not in env vars directly. The `secretref:` prefix in `--env-vars` is what injects the value at runtime:
```
--secrets "cosmos-key=$COSMOS_KEY_VALUE"
--env-vars "COSMOS_KEY=secretref:cosmos-key"
```
For production, replace connection strings with **Managed Identity** + Key Vault references to eliminate secret rotation entirely.

### Message Handling
- `complete_message()` — removes from queue (success path)
- `abandon_message()` — returns to queue for retry (failure path)
- After N delivery attempts, Service Bus moves the message to the **dead-letter queue** automatically

### Scale to Zero Trade-off
`minReplicas: 0` means zero cost when idle, but the first message after a cold period incurs a startup delay (image pull + runtime init). For latency-sensitive workloads, use `minReplicas: 1`.

### KEDA Scaler Auth
The `--scale-rule-auth` flag tells KEDA which secret to use when polling the Service Bus queue for its depth metric. KEDA needs its own read access to the queue — separate from the app's read/write access.

---

## Related Notes

- [[KEDA — Kubernetes Event-Driven Autoscaling]]
- [[Azure Container Apps — Replicas and Scaling]]
- [[Cosmos DB — Vector Search and Indexing]]
- [[Azure OpenAI — Embeddings]]
- [[AI-200 Exam Objectives]]
