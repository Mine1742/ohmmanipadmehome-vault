---
tags:
  - azure
  - ai-200
  - managed-identity
  - key-vault
  - security
  - container-apps
  - rbac
created: 2026-04-17
status: reference
---

# Managed Identity + Key Vault Pattern

## The Problem with Connection Strings

Static credentials (connection strings, API keys) have a lifecycle problem:
- They need to be rotated manually
- They live in shell history, CI/CD pipelines, and secret stores
- A leaked key has a window of exposure until rotated
- Every new service = another credential to manage

**Managed Identity eliminates the credential entirely.** Azure's identity platform vouches for your app directly — no password, no rotation, no secret sprawl.

---

## Mental Model

> Think of it like building access. Connection strings = physical keys (copied, lost, stolen, rotated). Managed Identity = facial recognition. The building knows who you are. You carry nothing.

Azure plays the identity system. Your Container App has a certificate Azure manages automatically, and you grant that identity RBAC permissions on specific resources.

---

## Two Types of Managed Identity

| Type | Lifecycle | Best for |
|---|---|---|
| **System-Assigned** | Tied to the resource; deleted when resource is deleted | Single app, simple case |
| **User-Assigned** | Independent resource; survives the compute | Shared across multiple apps |

Use **system-assigned** for a single worker. Use **user-assigned** when multiple Container Apps share the same identity (e.g., a multi-stage pipeline where all stages need Cosmos DB access).

---

## Full Auth Flow

```
Container App (Managed Identity)
  → requests token from Azure AD (automatic, no code)
    → Azure AD validates identity
      → returns short-lived token
        → app uses token to call Key Vault
          → KV checks RBAC: does identity have Secret Reader?
            → returns secret value
              → app uses secret to connect (e.g. Azure OpenAI)
```

For Azure-native services (Service Bus, Storage, Cosmos DB), skip Key Vault entirely:

```
Container App (Managed Identity)
  → requests token from Azure AD
    → uses token directly against target service
      → service checks RBAC: does identity have required role?
        → grants access
```

Key Vault is for **non-Azure secrets** (third-party API keys, custom config). Azure-native services support direct RBAC.

---

## Step-by-Step Setup

### 1. Enable Managed Identity on Container App

```bash
az containerapp identity assign \
  --name rag-worker \
  --resource-group $RG \
  --system-assigned

# Capture principal ID for role assignments
PRINCIPAL_ID=$(az containerapp identity show \
  --name rag-worker \
  --resource-group $RG \
  --query principalId -o tsv)
```

### 2. Create Key Vault and Store Non-Azure Secrets

```bash
KV_NAME="kv-rag-pipeline"

az keyvault create \
  --name $KV_NAME \
  --resource-group $RG \
  --location $LOCATION \
  --enable-rbac-authorization true    # Use RBAC, not legacy access policies

# Store only secrets that don't support managed identity
az keyvault secret set --vault-name $KV_NAME \
  --name "cosmos-key" --value "$COSMOS_KEY_VALUE"

az keyvault secret set --vault-name $KV_NAME \
  --name "aoai-key" --value "$AOAI_KEY_VALUE"
```

> Azure OpenAI data plane does not yet support managed identity — key goes in Key Vault.

### 3. Grant Identity Access to Key Vault

```bash
KV_ID=$(az keyvault show --name $KV_NAME --query id -o tsv)

# Key Vault Secrets User = read-only (least privilege)
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

### 4. Grant Identity Direct RBAC on Azure Services

```bash
# Service Bus — receive messages from specific queue
SB_ID=$(az servicebus namespace show \
  --name $SB_NS --resource-group $RG --query id -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Azure Service Bus Data Receiver" \
  --scope "$SB_ID/queues/doc-ingestion"

# Blob Storage — read blobs
STORAGE_ID=$(az storage account show \
  --name $STORAGE --resource-group $RG --query id -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Storage Blob Data Reader" \
  --scope $STORAGE_ID

# Cosmos DB — read/write data
COSMOS_ID=$(az cosmosdb show \
  --name $COSMOS_ACCT --resource-group $RG --query id -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cosmos DB Built-in Data Contributor" \
  --scope $COSMOS_ID
```

### 5. Update Worker Code

`DefaultAzureCredential` handles the token lifecycle automatically. In a Container App it uses the managed identity. Locally it falls back to `az login`.

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.servicebus import ServiceBusClient
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from openai import AzureOpenAI
import os

credential = DefaultAzureCredential()

# Pull non-Azure secrets from Key Vault
kv_client = SecretClient(
    vault_url=os.environ["KEY_VAULT_URL"],
    credential=credential
)
cosmos_key = kv_client.get_secret("cosmos-key").value
aoai_key   = kv_client.get_secret("aoai-key").value

# Azure-native services: pass credential directly, no connection strings
sb_client = ServiceBusClient(
    fully_qualified_namespace=os.environ["SB_NAMESPACE"],
    credential=credential
)

blob_client = BlobServiceClient(
    account_url=os.environ["STORAGE_URL"],
    credential=credential
)

cosmos_client = CosmosClient(
    url=os.environ["COSMOS_URL"],
    credential=credential
)

# Azure OpenAI still uses key (from Key Vault)
aoai_client = AzureOpenAI(
    azure_endpoint=os.environ["AOAI_ENDPOINT"],
    api_key=aoai_key,
    api_version="2024-02-01"
)
```

### 6. Update Container App — Remove All Connection Strings

```bash
az containerapp update \
  --name rag-worker \
  --resource-group $RG \
  --remove-all-secrets \
  --set-env-vars \
      "KEY_VAULT_URL=https://$KV_NAME.vault.azure.net" \
      "SB_NAMESPACE=$SB_NS.servicebus.windows.net" \
      "SERVICEBUS_QUEUE=doc-ingestion" \
      "STORAGE_URL=https://$STORAGE.blob.core.windows.net" \
      "COSMOS_URL=https://$COSMOS_ACCT.documents.azure.com:443/" \
      "COSMOS_DB=rag-db" \
      "COSMOS_CONTAINER=documents" \
      "AOAI_ENDPOINT=$AOAI_ENDPOINT"
```

No `secretref:` needed — these are non-sensitive resource URLs.

### 7. KEDA Scaling — Also Use Managed Identity

Switch the Service Bus scaler off the connection string:

```bash
az containerapp update \
  --name rag-worker \
  --resource-group $RG \
  --scale-rule-name servicebus-scaler \
  --scale-rule-type azure-servicebus \
  --scale-rule-metadata \
      "queueName=doc-ingestion" \
      "messageCount=5" \
      "namespace=$SB_NS" \
  --scale-rule-identity system
```

Now nothing in the deployment — app or scaler — uses a static credential.

---

## Before vs. After

| | Connection Strings | Managed Identity |
|---|---|---|
| Credentials stored | Shell, CI/CD, Container App secrets | Nowhere |
| Rotation required | Yes, manually | No — tokens auto-renewed |
| Privilege scope | Coarse (full namespace) | Fine-grained (per-queue, per-container) |
| Audit trail | Limited | Every access logged in Azure Monitor |
| Local dev | Works anywhere | `az login` → `DefaultAzureCredential` picks it up |
| Secret sprawl | Grows with each service | Zero for Azure-native services |

---

## DefaultAzureCredential Resolution Chain

In order of precedence — first one that works wins:

1. `EnvironmentCredential` — checks `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
2. `WorkloadIdentityCredential` — Kubernetes workload identity
3. `ManagedIdentityCredential` — **used in Container Apps**
4. `SharedTokenCacheCredential` — cached tokens from VS/VS Code
5. `VisualStudioCodeCredential`
6. `AzureCliCredential` — **used in local dev after `az login`**
7. `AzurePowerShellCredential`

This chain is why the same code works both in the Container App (uses #3) and on your dev machine (uses #6) with no changes.

---

## RBAC Roles Quick Reference

| Service | Role | Scope |
|---|---|---|
| Key Vault | `Key Vault Secrets User` | Vault or individual secret |
| Service Bus | `Azure Service Bus Data Receiver` | Namespace or queue |
| Service Bus | `Azure Service Bus Data Sender` | Namespace or queue |
| Blob Storage | `Storage Blob Data Reader` | Account, container, or blob |
| Blob Storage | `Storage Blob Data Contributor` | Account or container |
| Cosmos DB | `Cosmos DB Built-in Data Reader` | Account or database |
| Cosmos DB | `Cosmos DB Built-in Data Contributor` | Account or database |

> Always scope role assignments as narrowly as possible (queue-level, not namespace-level).

---

## Key Concepts to Lock In

- **Managed Identity = no credential to store, rotate, or leak**
- **System-assigned** is tied to the resource's lifecycle; **user-assigned** is independent
- `DefaultAzureCredential` works in all environments — no code changes between local and cloud
- Use **direct RBAC** for Azure-native services; use **Key Vault** only for non-Azure secrets
- Scope role assignments to the **minimum required resource** (queue, not namespace)
- KEDA can also authenticate via managed identity — `--scale-rule-identity system`

---

## Related Notes

- [[RAG-Ingestion-Pipeline-Pattern]]
- [[KEDA — Kubernetes Event-Driven Autoscaling]]
- [[Azure Container Apps — Replicas and Scaling]]
- [[AI-200 Exam Objectives]]
