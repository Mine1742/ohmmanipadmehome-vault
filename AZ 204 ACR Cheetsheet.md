
![[Pasted image 20260130113019.png]]


# Azure Container Registry (ACR)

Think of ACR as your **private Docker Hub, hosted in Azure**. It's where you store, manage, and distribute your container images and related artifacts — fully integrated with the rest of Azure's ecosystem.

---

## The Core Concept

When you build a container image, it needs to live somewhere so it can be pulled by ACI, AKS, Container Apps, or any other runtime. Docker Hub is the public option, but for enterprise and production workloads you want a **private, controlled registry** that lives inside your Azure environment, close to your other resources, with proper access control and security scanning baked in.

ACR is that registry. It's also not just for Docker images — it supports Helm charts, OCI artifacts, and even WASM modules.

---

## Key Concepts

**Registry** — the top-level resource. Lives in your subscription, has its own login server URL like `myregistry.azurecr.io`. Think of it like the server itself.

**Repository** — a named collection of related images inside the registry. For example `myregistry.azurecr.io/myapp` is a repository. You can have many repositories inside one registry.

**Image** — a specific container image stored in a repository. Identified by a tag: `myregistry.azurecr.io/myapp:v1.0` or `myregistry.azurecr.io/myapp:latest`.

**Tag** — a human-readable label pointing to a specific image version. Tags are mutable — `latest` can be reassigned to a new image at any time. For production you should use specific version tags, not `latest`, so deployments are deterministic.

**Digest** — an immutable SHA256 hash that uniquely identifies a specific image layer set. Even if someone reassigns the `v1.0` tag, the digest never changes. For truly locked-down deployments, reference images by digest rather than tag.

**Artifact** — the broader term for anything stored in ACR. Images are artifacts, but so are Helm charts and OCI-compatible packages.

---

## Service Tiers

ACR has three tiers and the differences matter for the exam:

**Basic** — entry level. Lower storage (10 GB) and throughput. No geo-replication, no content trust, limited webhooks. Fine for development and learning.

**Standard** — the most common production tier. More storage (100 GB), better throughput, supports webhooks. Still no geo-replication.

**Premium** — full feature set. Unlimited storage scaling, **geo-replication**, **private endpoints (VNet integration)**, **dedicated data endpoints**, content trust, higher throughput. Required if your workloads are globally distributed or if you need network isolation.

The exam will expect you to know that geo-replication and private endpoints are **Premium-only features**.

---

## Authentication

This is a big topic for AZ-204. There are several ways to authenticate to ACR:

### Admin Account

Every registry has an optional admin user (disabled by default). You enable it and get a username + two passwords. Simple, but bad practice for production — it's a shared credential that can't be scoped or audited properly. Fine for quick testing.

```bash
az acr update --name myregistry --admin-enabled true
az acr credential show --name myregistry
```

### Service Principal

Create a service principal, assign it an ACR role, use its client ID and secret as credentials. Works well for CI/CD pipelines and non-Azure workloads. The downside is you're managing a secret that needs rotation.

```bash
SP=$(az ad sp create-for-rbac --name myacrsp --skip-assignment)
SP_ID=$(echo $SP | jq -r .appId)
SP_PASSWORD=$(echo $SP | jq -r .password)

ACR_ID=$(az acr show --name myregistry --query id -o tsv)
az role assignment create --assignee $SP_ID --role AcrPull --scope $ACR_ID
```

### Managed Identity (Recommended)

The cleanest approach for Azure-hosted workloads. Your ACI, AKS, or Container Apps resource gets a managed identity, that identity gets an ACR role assignment, and Azure handles all token exchange behind the scenes. No secrets to manage. You saw this in the ACI deep dive.

### Azure AD / Individual Login (for developers)

When a developer needs to push/pull locally, they authenticate with their own Azure AD credentials:

```bash
az acr login --name myregistry
```

This gets a short-lived token using your `az login` session. Nothing stored, nothing to rotate. This is the recommended local dev workflow.

---

## ACR Roles

ACR uses Azure RBAC with these built-in roles:

**AcrPull** — can only pull images. Assign this to your runtime workloads (ACI, AKS nodes, etc.).

**AcrPush** — can pull and push images. Assign this to your CI/CD pipelines.

**AcrDelete** — can delete images and tags.

**AcrImageSigner** — can sign images (used with content trust).

**Owner / Contributor** — full control including registry management. Not for workloads — for admins only.

The principle of least privilege applies directly here: your production AKS cluster only needs `AcrPull`, never `AcrPush`.

---

## Pushing and Pulling Images

The standard workflow for getting an image into ACR:

```bash
# 1. Log in to your registry
az acr login --name myregistry

# 2. Build your image locally (or use ACR Tasks — see below)
docker build -t myapp:v1.0 .

# 3. Tag it with the full ACR path
docker tag myapp:v1.0 myregistry.azurecr.io/myapp:v1.0

# 4. Push it
docker push myregistry.azurecr.io/myapp:v1.0
```

Pulling is just the reverse:

```bash
docker pull myregistry.azurecr.io/myapp:v1.0
```

---

## ACR Tasks — Build in the Cloud

ACR Tasks is one of the most useful features and commonly tested. Instead of building your image locally and pushing it, you can offload the entire build process to Azure.

### Quick Task (on-demand build)

```bash
az acr build --registry myregistry --image myapp:v1.0 .
```

This sends your build context (the current directory) to Azure, builds the image in a temporary container in the cloud, and pushes the result directly into your registry. You don't even need Docker installed locally. Great for CI environments.

### Scheduled / Triggered Tasks

You can define multi-step tasks that trigger automatically on events:

- **On code commit** — trigger a build whenever you push to a GitHub or Azure DevOps repo
- **On base image update** — automatically rebuild your image when the base image it depends on (e.g. `node:18`) gets an update in Docker Hub or ACR itself
- **On a schedule** — cron-style scheduling for regular builds

```bash
# Create a task that triggers on GitHub commits
az acr task create \
  --registry myregistry \
  --name buildtask \
  --image myapp:{{.Run.ID}} \
  --context https://github.com/myorg/myrepo.git \
  --file Dockerfile \
  --git-access-token $GITHUB_TOKEN
```

This is a powerful pattern — your entire build pipeline can live inside ACR without needing a separate CI system for container builds.

---

## Geo-Replication (Premium)

When you geo-replicate a registry, ACR automatically replicates your images to multiple Azure regions. Your workloads in each region pull from a local copy, which means faster pull times and no cross-region bandwidth costs.

```bash
# Replicate your registry to West Europe
az acr replication create --registry myregistry --location westeurope
```

The registry URL stays the same (`myregistry.azurecr.io`) — Azure's traffic manager routes pull requests to the closest replica automatically. You push once, it's everywhere.

---

## Content Trust & Image Signing

Content trust lets you **sign images** so consumers can verify that an image actually came from a trusted source and hasn't been tampered with. Built on Notary v1 (there's a newer Notary v2 / ORAS path emerging, but v1 is what's in scope for the exam).

```bash
# Enable content trust for your Docker client session
export DOCKER_CONTENT_TRUST=1
export DOCKER_CONTENT_TRUST_SERVER=https://myregistry.azurecr.io
```

When enabled, Docker will refuse to pull unsigned images from the registry. Useful in high-security environments where you want to ensure only approved images can be deployed.

---

## Vulnerability Scanning

ACR integrates with **Microsoft Defender for Containers** (formerly Defender for container registries) to automatically scan pushed images for known vulnerabilities (CVEs). When enabled, every image push triggers a scan and results are surfaced in Microsoft Defender for Cloud.

This is a toggle you enable at the Defender plan level — not a native ACR feature per se, but closely associated with it and worth knowing for the exam.

---

## Retention Policies & Lifecycle Management

Registries can accumulate a lot of untagged images over time — every CI build that pushes `latest` leaves behind an untagged manifest. ACR supports **retention policies** (Premium tier) to automatically purge untagged manifests after a set number of days.

You can also run `acr purge` as an ACR Task on a schedule to clean up old tagged images:

```bash
# Purge images older than 30 days from the myapp repo
az acr run \
  --registry myregistry \
  --cmd "acr purge --filter 'myapp:.*' --ago 30d --untagged" \
  /dev/null
```

---

## Private Endpoints (Premium)

By default ACR is accessible over the public internet (authenticated, but public). For fully locked-down environments you can deploy a **private endpoint** into your VNet — your registry gets a private IP address, and DNS resolves `myregistry.azurecr.io` to that private IP within your network. Traffic never leaves your VNet.

```bash
az network private-endpoint create \
  --name myACRPrivateEndpoint \
  --resource-group myRG \
  --vnet-name myVNet \
  --subnet mySubnet \
  --private-connection-resource-id $(az acr show --name myregistry --query id -o tsv) \
  --group-id registry \
  --connection-name myACRConnection
```

You'd pair this with **disabling public network access** on the registry so it's only reachable from within your VNet or peered networks.

---

## How ACR Fits the Broader Container Story

ACR is the **hub that connects everything**. The flow in a real deployment looks like this:

```
Developer / CI Pipeline
        │
        │  docker build + push
        ▼
  Azure Container Registry  ◄──── ACR Tasks (auto-build on commit)
        │
        │  pull on deploy
        ├──────────────────► ACI (container groups)
        ├──────────────────► AKS (node pools pull images)
        └──────────────────► Container Apps (pulls at revision deploy)
```

Every container runtime in Azure is designed to integrate with ACR natively, particularly with managed identity so no credentials ever need to be managed.

---

## AZ-204 Exam Summary

The key things to have solid for the exam are the **three service tiers and what's exclusive to Premium** (geo-replication, private endpoints), the **authentication options and when to use each** (managed identity for workloads, service principal for CI/CD, `az acr login` for local dev), the difference between **tags and digests**, how **ACR Tasks** work for cloud-based builds, and how to **integrate ACR with ACI and AKS using managed identity**.

# Integrating ACR with ACI and AKS Using Managed Identity

Before diving in, a quick refresher on why managed identity matters here. The alternative — service principals with passwords — means you're storing secrets somewhere, rotating them on a schedule, and hoping nothing leaks. Managed identity eliminates all of that. Azure handles the credential lifecycle entirely. Your workload just says "I need to pull from ACR" and Azure proves its identity automatically.

---

## Understanding the Two Types of Managed Identity

You'll encounter both in these integrations so it's worth being clear on the difference upfront.

**System-assigned** — tied directly to a specific Azure resource. Created and deleted with that resource. One resource, one identity. No sharing across resources.

**User-assigned** — created as a standalone Azure resource. Can be attached to multiple resources simultaneously. Persists independently of any single resource. Better for shared infrastructure and reuse across environments.

For ACR integration the pattern is the same either way — you're granting the identity the `AcrPull` role on the registry. The choice between system and user-assigned comes down to your architecture preferences.

---

## ACR + ACI Integration

### System-Assigned Identity

```bash
# 1. Create the registry
az acr create \
  --resource-group myRG \
  --name myregistry \
  --sku Basic

# 2. Create the container group with system-assigned identity
#    (we create it first with a placeholder image to get the identity, 
#    then update — or we do it all in Bicep which is cleaner)
az container create \
  --resource-group myRG \
  --name mycontainergroup \
  --image mcr.microsoft.com/azuredocs/aci-helloworld \
  --assign-identity '[system]'

# 3. Get the principal ID of the system identity
PRINCIPAL_ID=$(az container show \
  --resource-group myRG \
  --name mycontainergroup \
  --query identity.principalId \
  --output tsv)

# 4. Get the ACR resource ID
ACR_ID=$(az acr show --name myregistry --query id --output tsv)

# 5. Grant AcrPull to the container group's identity
az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role AcrPull \
  --scope $ACR_ID
```

The problem with this CLI approach is the chicken-and-egg situation — you need the container group to exist to get its principal ID, but you want it to pull from ACR on creation. **Bicep solves this cleanly** because it can resolve the identity and role assignment in a single deployment.

---

### Bicep — ACI with User-Assigned Identity (Recommended Pattern)

With a user-assigned identity you create it first, grant it AcrPull, then attach it to the container group. No chicken-and-egg problem.

```bicep
// main.bicep

param location string = resourceGroup().location
param registryName string = 'myregistry'
param containerGroupName string = 'mycontainergroup'
param identityName string = 'myaciidentity'

// Reference existing ACR
resource acr 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' existing = {
  name: registryName
}

// Create user-assigned managed identity
resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

// Built-in AcrPull role definition ID (this is a fixed GUID in Azure)
var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'

// Grant AcrPull to the identity on the registry
resource acrRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, identity.id, acrPullRoleId)
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

// Create container group using the identity to pull from ACR
resource containerGroup 'Microsoft.ContainerInstance/containerGroups@2021-09-01' = {
  name: containerGroupName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    imageRegistryCredentials: [
      {
        server: acr.properties.loginServer          // e.g. myregistry.azurecr.io
        identity: identity.id                        // tells ACI to use this identity for auth
      }
    ]
    containers: [
      {
        name: 'mycontainer'
        properties: {
          image: '${acr.properties.loginServer}/myapp:latest'
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1
            }
          }
          ports: [{ port: 80 }]
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
  dependsOn: [
    acrRoleAssignment   // ensure the role is assigned before the container tries to pull
  ]
}
```

The `dependsOn: [acrRoleAssignment]` is important. Without it, Azure might try to create the container group and pull the image before the role assignment has propagated, causing a pull failure. This is a subtle race condition that catches a lot of people.

---

## ACR + AKS Integration

AKS is slightly different because it's not a single container pulling an image — it's a cluster of nodes, each running a kubelet process that pulls images on behalf of pods. The identity needs to be attached at the cluster level.

There are two approaches that matter for the exam.

---

### Approach 1: The `--attach-acr` Flag (Simplest)

When creating or updating an AKS cluster, you can use `--attach-acr` to automatically set up the role assignment. This is the fastest path and what you'd use in most real scenarios.

```bash
# Create AKS cluster and attach ACR in one command
az aks create \
  --resource-group myRG \
  --name myakscluster \
  --node-count 2 \
  --generate-ssh-keys \
  --attach-acr myregistry
```

Or if your cluster already exists:

```bash
az aks update \
  --resource-group myRG \
  --name myakscluster \
  --attach-acr myregistry
```

What this does behind the scenes: AKS has a **kubelet managed identity** (either system or user-assigned depending on how you created the cluster). The `--attach-acr` flag grants that kubelet identity the `AcrPull` role on the specified registry. That's the entire integration — once that role assignment exists, every node in the cluster can pull images from that registry without any credentials in your pod specs or Kubernetes secrets.

You can verify it worked:

```bash
az aks check-acr \
  --resource-group myRG \
  --name myakscluster \
  --acr myregistry.azurecr.io
```

---

### Approach 2: Manual Role Assignment (Full Control)

If you need to understand exactly what's happening, or if you're managing this through Bicep/ARM in a pipeline, do it manually.

```bash
# Get the kubelet identity's object ID
# AKS uses a separate identity for the kubelet (node pool image pulls)
# vs the control plane identity
KUBELET_IDENTITY=$(az aks show \
  --resource-group myRG \
  --name myakscluster \
  --query identityProfile.kubeletidentity.objectId \
  --output tsv)

# Get ACR resource ID
ACR_ID=$(az acr show --name myregistry --query id --output tsv)

# Grant AcrPull
az role assignment create \
  --assignee $KUBELET_IDENTITY \
  --role AcrPull \
  --scope $ACR_ID
```

Notice it's `identityProfile.kubeletidentity` not just `identity`. AKS actually has **two separate identities**:

- **Control plane identity** (`identity`) — used by the AKS control plane to manage Azure resources like load balancers, disks, and NICs on your behalf.
- **Kubelet identity** (`identityProfile.kubeletidentity`) — used by the nodes to pull container images. This is the one that needs `AcrPull`.

This is an important distinction the exam can test. Granting `AcrPull` to the control plane identity instead of the kubelet identity is a common mistake — the pulls will still fail.

---

### Bicep — AKS + ACR Integration

```bicep
param location string = resourceGroup().location
param clusterName string = 'myakscluster'
param registryName string = 'myregistry'

resource acr 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' existing = {
  name: registryName
}

resource aksCluster 'Microsoft.ContainerService/managedClusters@2023-01-01' = {
  name: clusterName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: clusterName
    agentPoolProfiles: [
      {
        name: 'nodepool1'
        count: 2
        vmSize: 'Standard_DS2_v2'
        mode: 'System'
      }
    ]
    // Use managed identity for kubelet (node image pulls)
    identityProfile: {
      kubeletidentity: {
        resourceId: kubeletIdentity.id
        clientId: kubeletIdentity.properties.clientId
        objectId: kubeletIdentity.properties.principalId
      }
    }
  }
}

resource kubeletIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${clusterName}-kubelet-identity'
  location: location
}

var acrPullRoleId = '7f951dda-4ed3-4680-a7ca-43fe172d538d'

resource acrRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, kubeletIdentity.id, acrPullRoleId)
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', acrPullRoleId)
    principalId: kubeletIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}
```

---

### What This Looks Like in Practice — Pod Spec

Once the integration is set up, your Kubernetes pod specs don't need any `imagePullSecrets`. The pull happens transparently at the node level.

```yaml
# No imagePullSecrets needed — kubelet identity handles auth
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry.azurecr.io/myapp:v1.0   # private ACR image, no secret needed
        ports:
        - containerPort: 80
```

Compare this to what you'd need without the managed identity integration — a Kubernetes secret containing base64-encoded registry credentials, referenced in every pod spec. Managed identity completely eliminates that overhead.

---

## Side-by-Side Comparison

||**ACI + Managed Identity**|**AKS + Managed Identity**|
|---|---|---|
|Identity type used|Container group identity|Kubelet identity (not control plane)|
|Where identity is configured|`identity` block + `imageRegistryCredentials` in container group|`identityProfile.kubeletidentity` on the cluster|
|Role needed|`AcrPull` on ACR|`AcrPull` on ACR|
|Quickest setup method|Bicep deployment|`--attach-acr` flag|
|Pod/container spec change needed|No `imagePullSecrets`|No `imagePullSecrets`|
|Race condition risk|Yes — use `dependsOn`|Less common but role propagation delay possible|

---

## Common Mistakes to Watch For

**Using the wrong identity for AKS** — granting `AcrPull` to the control plane identity (`identity.principalId`) instead of the kubelet identity (`identityProfile.kubeletidentity.objectId`). The cluster won't error loudly — your pods will just fail to pull images with a vague `ImagePullBackOff`.

**Missing `dependsOn` in Bicep for ACI** — role assignments take a moment to propagate. If the container group starts before the assignment is active, the first pull fails. Always declare the dependency explicitly.

**Attaching ACR to the wrong resource group** — `--attach-acr` accepts either the registry name or resource ID. If you have registries in multiple resource groups with the same name, be explicit with the resource ID to avoid attaching to the wrong one.

**Using `latest` tag in production** — unrelated to managed identity but worth noting: once your auth is solid, don't undermine your deployment reliability with mutable tags. Pin to specific versions or digests.

---

That's the complete picture of ACR + managed identity for both ACI and AKS. Want to move on to another AZ-204 topic, or would a mock exam scenario on this be useful?