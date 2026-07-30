![[Pasted image 20260122132304.png]]

![[Pasted image 20260123084903.png]]

# Azure Container Instances (ACI)

Think of ACI as the **simplest, fastest way to run a container in Azure** — no VMs to manage, no orchestrator to set up, no cluster to maintain. You hand Azure a container image, and within seconds it's running.

---

## The Core Concept

ACI is **serverless containers**. Azure handles all the underlying infrastructure — you just define what container you want to run, how much CPU/memory it needs, and Azure spins it up. You're billed per second for the resources your container actually uses.

A good mental model: if Azure Kubernetes Service (AKS) is like buying and managing a whole fleet of trucks, ACI is like calling an Uber. You just need a ride right now, you don't want to own or maintain anything.

---

## Key Components

**Container Group** — the top-level resource in ACI. This is equivalent to a Kubernetes Pod. It's a collection of one or more containers that share the same lifecycle, network, and storage. They're always scheduled together on the same host.

**Container** — the actual running instance of your image. Pulled from Docker Hub, Azure Container Registry (ACR), or any other registry.

**Restart Policy** — controls what happens when a container finishes or crashes. Three options: `Always` (keep it running, good for long-running services), `Never` (run once and stop), or `OnFailure` (restart only if it exited with an error).

**Environment Variables** — passed into the container at startup, same as you'd use in any Docker workflow. Supports secure values (masked in the portal/API, used for secrets).

**Resource Requests** — you specify CPU cores (can be fractional, like 0.5) and memory in GB. ACI allocates exactly what you ask for.

---

## Networking

Each container group gets its own **public IP address** by default (optional), and you can expose specific ports. You can also deploy ACI into a **Virtual Network (VNet)** for private communication with other Azure resources — this is important for production scenarios where you don't want your container exposed to the public internet.

DNS name label is supported too, so instead of a raw IP you can get something like `myapp.eastus.azurecontainer.io`.

---

## Storage / Persistence

Containers are ephemeral by default — if the container restarts, local data is gone. To persist data you can mount:

**Azure File Shares** — mount an Azure Files share directly into the container as a volume. Good for shared or persistent file data.

**Azure Disk** (emptyDir / GitRepo volumes) — for temporary shared scratch space between containers in the same group.

---

## Multi-Container Groups

You can run multiple containers in a single container group, similar to a sidecar pattern in Kubernetes. A classic use case is running your main app container alongside a logging or proxy sidecar. They share the same IP, can communicate over `localhost`, and start/stop together.

---

## How It Fits in the Azure Ecosystem

This is where a lot of people get confused, so here's a clean breakdown of when to use what:

**ACI** — short-lived tasks, burst workloads, simple apps, CI/CD jobs, event-driven processing. No orchestration needed.

**AKS** — complex microservices, long-running production workloads, need autoscaling, rolling deployments, service mesh, etc.

**Azure Container Apps** — sits between the two. Built on top of Kubernetes but fully managed, supports KEDA-based scaling, Dapr, ingress — good for microservices without the overhead of managing AKS.

**App Service (containers)** — web apps and APIs in containers, simpler than AKS, has built-in scaling and deployment slots.

A common pattern is using **ACI as a burst worker** from AKS via the **Virtual Kubelet** — when your AKS cluster is under heavy load, it can spin up ACI containers to handle overflow, then tear them down when done.

---

## Common Real-World Use Cases

- Running a scheduled batch job (pull data, process it, exit)
- CI/CD pipeline steps (build, test, deploy in an isolated container)
- On-demand data processing triggered by an event (like an Event Hub or Service Bus message)
- Running a quick isolated environment for testing
- Sidecar containers for monitoring or logging alongside another service

---

## AZ-204 Relevance

For the cert you'll want to know how to **deploy a container group** (via CLI, ARM, Bicep, or the SDK), how to configure **environment variables and mounted volumes**, the difference between **restart policies**, and how ACI integrates with **ACR** for pulling private images (using a service principal or managed identity). You should also understand how ACI fits into the broader container story alongside AKS and Container Apps.

---

## Quick CLI Example (just to make it concrete)

```bash
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image mcr.microsoft.com/azuredocs/aci-helloworld \
  --cpu 1 \
  --memory 1.5 \
  --ports 80 \
  --dns-name-label myapp-demo \
  --restart-policy OnFailure
```

That's genuinely all it takes to get a container running with a public DNS name.


# ACI Deep Dive — AZ-204 Edition

---

## 1. Deploying a Container Group

### CLI

The most straightforward method. Good for quick deployments and scripts.

```bash
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myregistry.azurecr.io/myapp:latest \
  --cpu 1 \
  --memory 1.5 \
  --ports 80 443 \
  --dns-name-label myapp-demo \
  --restart-policy Always \
  --environment-variables KEY1=value1 KEY2=value2 \
  --secure-environment-variables SECRET_KEY=supersecret
```

To check status:

```bash
az container show --resource-group myRG --name mycontainer --query instanceView.state
```

To stream logs:

```bash
az container logs --resource-group myRG --name mycontainer --follow
```

---

### ARM Template

ARM is verbose but gives you full control and is good to recognize for the exam.

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "apiVersion": "2021-09-01",
      "name": "myContainerGroup",
      "location": "[resourceGroup().location]",
      "properties": {
        "containers": [
          {
            "name": "mycontainer",
            "properties": {
              "image": "myregistry.azurecr.io/myapp:latest",
              "resources": {
                "requests": {
                  "cpu": 1,
                  "memoryInGB": 1.5
                }
              },
              "ports": [{ "port": 80 }],
              "environmentVariables": [
                { "name": "KEY1", "value": "value1" },
                { "name": "SECRET_KEY", "secureValue": "supersecret" }
              ]
            }
          }
        ],
        "osType": "Linux",
        "restartPolicy": "Always",
        "ipAddress": {
          "type": "Public",
          "ports": [{ "protocol": "TCP", "port": 80 }]
        }
      }
    }
  ]
}
```

Deploy it with:

```bash
az deployment group create --resource-group myRG --template-file template.json
```

---

### Bicep

Bicep is the modern, cleaner alternative to ARM. Same end result, much more readable. This is increasingly what you'll see in the real world.

```bicep
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2021-09-01' = {
  name: 'myContainerGroup'
  location: resourceGroup().location
  properties: {
    containers: [
      {
        name: 'mycontainer'
        properties: {
          image: 'myregistry.azurecr.io/myapp:latest'
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1
            }
          }
          ports: [{ port: 80 }]
          environmentVariables: [
            { name: 'KEY1', value: 'value1' }
            { name: 'SECRET_KEY', secureValue: 'supersecret' }
          ]
        }
      }
    ]
    osType: 'Linux'
    restartPolicy: 'Always'
    ipAddress: {
      type: 'Public'
      ports: [{ protocol: 'Tcp', port: 80 }]
    }
  }
}
```

Deploy it with:

```bash
az deployment group create --resource-group myRG --template-file main.bicep
```

---

### .NET SDK

For when you're managing ACI programmatically from application code — a real AZ-204 scenario.

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.ContainerInstance;
using Azure.ResourceManager.ContainerInstance.Models;

var armClient = new ArmClient(new DefaultAzureCredential());
var subscription = await armClient.GetDefaultSubscriptionAsync();
var resourceGroup = await subscription.GetResourceGroups().GetAsync("myRG");

var containerGroupData = new ContainerGroupData(
    new AzureLocation("eastus"),
    new[]
    {
        new ContainerInstanceContainer("mycontainer",
            "myregistry.azurecr.io/myapp:latest",
            new ContainerResourceRequirements(
                new ContainerResourceRequestsContent(1.5, 1)))
    },
    ContainerInstanceOperatingSystemType.Linux)
{
    RestartPolicy = ContainerGroupRestartPolicy.Always,
    IPAddress = new ContainerGroupIPAddress(
        new[] { new ContainerGroupPort(80) },
        ContainerGroupIPAddressType.Public)
};

var containerGroups = resourceGroup.Value.GetContainerGroups();
await containerGroups.CreateOrUpdateAsync(
    Azure.WaitUntil.Completed,
    "myContainerGroup",
    containerGroupData);
```

---

## 2. Environment Variables

Environment variables are how you pass configuration into a running container — connection strings, feature flags, API endpoints, etc.

There are two types and the distinction matters for the exam:

**Regular** (`value`) — visible in the portal, in logs, via the API. Fine for non-sensitive config.

**Secure** (`secureValue`) — masked everywhere. Never returned in GET responses or shown in the portal. Used for secrets like passwords, API keys, connection strings. **Cannot be read back once set** — only the container itself can access the value at runtime.

```bash
# CLI example showing both types
az container create \
  --environment-variables APP_ENV=production DB_HOST=mydb.postgres.database.azure.com \
  --secure-environment-variables DB_PASSWORD=mysecretpassword
```

In ARM/Bicep, `value` vs `secureValue` is the property name difference — the exam may test that you know which property name to use.

For production workloads, a better pattern than secure env vars is to pull secrets directly from **Azure Key Vault** at runtime using a managed identity — but that's a slightly more advanced pattern involving the Key Vault SDK inside your container code.

---

## 3. Mounted Volumes

Since containers are ephemeral, any data written to the container's local filesystem is lost on restart. Volumes solve this.

### Azure File Share (most common)

Persists data across restarts and can be shared between multiple containers or container groups.

```bash
# First create the storage account and file share
az storage account create --name mystorageacct --resource-group myRG --sku Standard_LRS
az storage share create --name myshare --account-name mystorageacct

# Get the storage key
STORAGE_KEY=$(az storage account keys list --account-name mystorageacct --query [0].value -o tsv)

# Mount it when creating the container
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myapp:latest \
  --azure-file-volume-account-name mystorageacct \
  --azure-file-volume-account-key $STORAGE_KEY \
  --azure-file-volume-share-name myshare \
  --azure-file-volume-mount-path /data
```

In Bicep, it looks like this:

```bicep
properties: {
  containers: [
    {
      name: 'mycontainer'
      properties: {
        volumeMounts: [
          {
            name: 'myvolume'
            mountPath: '/data'
          }
        ]
      }
    }
  ]
  volumes: [
    {
      name: 'myvolume'
      azureFile: {
        shareName: 'myshare'
        storageAccountName: 'mystorageacct'
        storageAccountKey: 'your-storage-key'
      }
    }
  ]
}
```

### emptyDir

A temporary scratch volume shared between containers _within the same container group_. Wiped when the group restarts. Useful for sidecar patterns where two containers need to exchange files.

```bicep
volumes: [
  {
    name: 'scratch'
    emptyDir: {}
  }
]
```

### gitRepo (legacy)

Clones a Git repo into a volume at container startup. Rarely used now — mostly replaced by baking the code into the image at build time.

---

## 4. Restart Policies

This is clean and testable for the exam. Three options:

**`Always`** — container is always restarted if it stops, regardless of exit code. Use this for long-running services like a web server or background worker that should stay up indefinitely.

**`Never`** — container runs once and is never restarted, regardless of whether it succeeded or failed. Use this for one-shot jobs where you want to inspect the result afterward regardless of outcome. The container group stays in a "Terminated" state so you can still pull logs.

**`OnFailure`** — container is restarted only if it exits with a non-zero exit code (i.e., it crashed or errored). If it exits cleanly (exit code 0), it stays stopped. This is the sweet spot for **batch jobs and scheduled tasks** — run to completion successfully, stop; crash, retry automatically.

A memory trick: think about what you'd want for each scenario:

- Web API → `Always` (never stop)
- Nightly data export job → `OnFailure` (retry on crash, stop on success)
- One-time database migration → `Never` (run once, let me check the result)

---

## 5. Integrating with ACR (Private Registry)

By default ACI can pull from public Docker Hub. For private images in ACR you need to authenticate. Two ways to do it:

---

### Option A: Service Principal

A service principal is an app identity with credentials (client ID + client secret). You grant it the `AcrPull` role on your ACR, then pass those credentials to ACI.

```bash
# Create service principal and capture credentials
SP=$(az ad sp create-for-rbac --name acisp --skip-assignment)
SP_ID=$(echo $SP | jq -r .appId)
SP_PASSWORD=$(echo $SP | jq -r .password)

# Get ACR resource ID
ACR_ID=$(az acr show --name myregistry --query id -o tsv)

# Grant AcrPull role
az role assignment create --assignee $SP_ID --role AcrPull --scope $ACR_ID

# Use credentials when creating container
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myregistry.azurecr.io/myapp:latest \
  --registry-login-server myregistry.azurecr.io \
  --registry-username $SP_ID \
  --registry-password $SP_PASSWORD
```

This works but has a downside — you're managing a secret (the SP password). That password needs to be rotated and stored somewhere securely.

---

### Option B: Managed Identity (Preferred)

A managed identity is an identity that Azure manages entirely — no passwords, no secrets, no rotation. Your container group gets an identity, and that identity is granted permission to pull from ACR. Azure handles the token exchange behind the scenes.

```bash
# Create a user-assigned managed identity
az identity create --name myaciidentity --resource-group myRG
IDENTITY_ID=$(az identity show --name myaciidentity --resource-group myRG --query id -o tsv)
IDENTITY_CLIENT_ID=$(az identity show --name myaciidentity --resource-group myRG --query clientId -o tsv)

# Grant it AcrPull on your registry
ACR_ID=$(az acr show --name myregistry --query id -o tsv)
az role assignment create --assignee $IDENTITY_CLIENT_ID --role AcrPull --scope $ACR_ID
```

Then in your Bicep/ARM template:

```bicep
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2021-09-01' = {
  name: 'myContainerGroup'
  location: resourceGroup().location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    imageRegistryCredentials: [
      {
        server: 'myregistry.azurecr.io'
        identity: identity.id
      }
    ]
    // ... rest of properties
  }
}
```

The exam will expect you to know that **managed identity is the more secure, recommended approach** because it eliminates credential management entirely.

---

## 6. ACI's Place in the Broader Container Story

Here's a clean comparison you can reason from rather than just memorize:

||**ACI**|**Container Apps**|**AKS**|
|---|---|---|---|
|Complexity|Minimal|Medium|High|
|Management overhead|None|None|High|
|Scaling|Manual / none|Auto (KEDA)|Auto (HPA/KEDA)|
|Networking|Basic|Built-in ingress|Full control|
|Long-running services|Yes (basic)|Yes (better)|Yes (best)|
|Batch / burst jobs|Best fit|Good|Overkill|
|Microservices|Awkward|Good (Dapr support)|Best fit|
|Cost model|Per second|Per second|Always-on nodes|
|When to choose|Simple tasks, jobs, burst|Microservices without k8s overhead|Full control, complex workloads|

The key insight for the exam: **these services exist on a spectrum of control vs. simplicity**. ACI trades away nearly all control for maximum simplicity. AKS gives you everything but demands you know what you're doing. Container Apps is the pragmatic middle ground for microservice-style workloads.

A pattern worth knowing: ACI is often used as a **burst worker pool behind AKS** via Virtual Nodes (powered by Virtual Kubelet). When your AKS cluster is at capacity, it can schedule pods onto ACI transparently — those pods run as ACI container groups, and you pay per-second only during the burst. When load drops, the ACI containers are terminated.
