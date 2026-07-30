![[Pasted image 20260202144718.png]]

![[Pasted image 20260202144825.png]]


# Azure App Service

Think of App Service as **Azure's fully managed platform for hosting web applications**. You bring the code or container, Microsoft manages everything underneath — the OS, patching, load balancing, scaling infrastructure, certificates. You just focus on your app.

---

## The Core Concept

App Service is a **Platform as a Service (PaaS)** offering. The spectrum looks like this:

```
IaaS (VMs)          PaaS (App Service)          FaaS (Functions)
  │                        │                          │
Full control          Sweet spot                  No server thinking
OS management         No OS mgmt                  Event-driven only
You patch everything  Microsoft patches            Ephemeral
```

App Service sits in the middle — you get significant control over your application and runtime without ever thinking about the underlying servers. It supports .NET, Node.js, Python, Java, PHP, and Ruby natively, plus any language via custom containers.

---

## Key Components

### App Service Plan

This is the **underlying compute resource** that your apps run on. Think of it as the server (or set of servers) that App Service provisions on your behalf. Every App Service app must live inside a plan.

The plan defines:

- **Region** — where the compute lives
- **VM size** — how much CPU and memory each instance has
- **Tier** — determines what features are available
- **Instance count** — how many VMs are in the pool

Multiple apps can share the same App Service Plan and therefore share the same underlying compute. This is cost-efficient but means apps compete for resources.

```bash
# Create a plan
az appservice plan create \
  --resource-group myRG \
  --name myplan \
  --sku B1 \
  --is-linux
```

---

### Service Tiers

This is heavily tested. Know what each tier gives you:

**Free (F1)** — shared compute, no custom domain, no SSL, 60 minutes CPU per day. Dev/testing only.

**Shared (D1)** — shared compute, custom domain supported, still no SSL. Rarely used.

**Basic (B1/B2/B3)** — dedicated compute, custom domains, SSL, manual scaling only. Good for dev/test with consistent load.

**Standard (S1/S2/S3)** — dedicated compute, **auto-scaling**, **deployment slots** (up to 5), custom domains, SSL, **daily backups**, Traffic Manager support. The entry point for production workloads.

**Premium (P1v2/P2v2/P3v2 and v3 variants)** — everything in Standard plus **more deployment slots** (up to 20), **VNet integration**, larger VMs, zone redundancy available.

**Isolated (I1/I2/I3)** — runs in a dedicated **App Service Environment (ASE)**, your own VNet, highest scale, network isolation. For highly regulated industries or maximum isolation requirements.

The exam frequently tests the tier boundaries — particularly that **auto-scaling starts at Standard**, **VNet integration requires Premium**, and **ASE requires Isolated**.

---

## Deployment Methods

App Service supports many ways to get your code in. Know all of them.

### Local Git

App Service provisions a Git endpoint. You push your code directly to it like any remote.

```bash
az webapp deployment source config-local-git \
  --resource-group myRG \
  --name myapp

# Returns a Git URL like:
# https://<username>@myapp.scm.azurewebsites.net/myapp.git

git remote add azure https://<username>@myapp.scm.azurewebsites.net/myapp.git
git push azure main
```

### ZIP Deploy

Package your app as a ZIP and push it. Fast and simple — good for CI/CD pipelines.

```bash
az webapp deploy \
  --resource-group myRG \
  --name myapp \
  --src-path ./app.zip \
  --type zip
```

### GitHub Actions / Azure DevOps

The most common production pattern. Trigger a build and deploy pipeline on every push to a branch. App Service can auto-generate a GitHub Actions workflow file for you when you connect a repo in the portal.

### Container Deployment

Instead of code, deploy a Docker image from ACR, Docker Hub, or any private registry.

```bash
az webapp create \
  --resource-group myRG \
  --plan myplan \
  --name myapp \
  --deployment-container-image-name myregistry.azurecr.io/myapp:latest
```

### Run from Package (Recommended for production)

Instead of extracting files to the wwwroot folder, the app runs directly from a ZIP package mounted as a read-only filesystem. Benefits are faster cold starts, no partial deployment states, and consistent behavior.

```bash
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings WEBSITE_RUN_FROM_PACKAGE=1
```

---

## Deployment Slots

This is a major AZ-204 topic. Deployment slots are **live, independent copies of your app** with their own hostnames, settings, and deployed code. Standard tier gets 5, Premium gets 20.

The key operation is the **swap** — you deploy to a staging slot, warm it up, validate it, then swap staging into production. The swap is near-instantaneous (just a routing change) and if something goes wrong you can swap back.

```bash
# Create a staging slot
az webapp deployment slot create \
  --resource-group myRG \
  --name myapp \
  --slot staging

# Deploy to staging (not production)
az webapp deploy \
  --resource-group myRG \
  --name myapp \
  --slot staging \
  --src-path ./app.zip

# Swap staging into production
az webapp deployment slot swap \
  --resource-group myRG \
  --name myapp \
  --slot staging \
  --target-slot production
```

### Slot Settings vs. Sticky Settings

This is a subtle but commonly tested concept. When you swap slots, **most settings travel with the slot** (connection strings, app settings). But some settings you want to **stick to the slot** regardless of swaps — for example, a connection string pointing to a production database should stay in production, not follow the staging app over.

You mark settings as "slot-specific" (sticky) so they don't move during swaps:

```bash
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --slot-settings DB_CONNECTION_STRING="production-connection-string"
```

Now if you swap staging into production, the production DB connection string stays in production, and staging keeps its own staging DB connection string.

### Traffic Splitting (A/B Testing)

You can gradually route a percentage of production traffic to a slot for canary deployments or A/B testing:

```bash
az webapp traffic-routing set \
  --resource-group myRG \
  --name myapp \
  --distribution staging=20
```

This sends 20% of traffic to staging, 80% to production. Users are "sticky" — once routed to a slot, a cookie keeps them on that slot for their session.

---

## Configuration and App Settings

### Application Settings

Key-value pairs injected into your app as **environment variables** at runtime. These override anything in your config files (like `appsettings.json` in .NET). In .NET specifically, they follow a hierarchy where App Service settings win over local config.

```bash
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings KEY1=value1 KEY2=value2
```

Nested settings use double underscore in the key name: `MySection__MyKey` maps to `MySection:MyKey` in .NET configuration.

### Connection Strings

A separate category from app settings — functionally similar but shows up differently in .NET's `IConfiguration`. App Service prefixes them based on type (`SQLCONNSTR_`, `MYSQLCONNSTR_`, etc.) when exposing them as environment variables.

### Key Vault References

Instead of storing secrets directly in app settings, you can reference Key Vault secrets. The value looks like:

```
@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/mysecret/)
```

App Service resolves this at runtime using its managed identity. The secret value is never stored in App Service — it's fetched from Key Vault on each access. This is the recommended approach for secrets in production.

---

## Scaling

### Scale Up (Vertical)

Change the App Service Plan tier to get more CPU and memory. Requires a brief restart.

```bash
az appservice plan update \
  --resource-group myRG \
  --name myplan \
  --sku P2v3
```

### Scale Out (Horizontal)

Add more instances. Can be manual or automatic. **Auto-scale requires Standard tier or above.**

```bash
# Manual scale out
az appservice plan update \
  --resource-group myRG \
  --name myplan \
  --number-of-workers 3
```

For auto-scale you define rules based on metrics — CPU percentage, HTTP queue length, memory, custom metrics. You set a min/max instance count and rules that define when to add or remove instances.

```bash
# Create an auto-scale profile
az monitor autoscale create \
  --resource-group myRG \
  --resource myplan \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-rules \
  --min-count 1 \
  --max-count 10 \
  --count 2

# Add a scale-out rule: add 1 instance when CPU > 70% for 5 minutes
az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name autoscale-rules \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

---

## Networking

### Inbound Options

By default your app is reachable on `myapp.azurewebsites.net`. You can add a custom domain, bind an SSL certificate, and restrict access with **access restrictions** (IP allowlists/denylists or Service Tag filtering).

### VNet Integration (Premium+)

Allows your app to make **outbound connections** into a VNet — to reach databases, services, or other resources not exposed to the public internet. Note: VNet Integration is **outbound only**. It does not make your app private on the inbound side.

```bash
az webapp vnet-integration add \
  --resource-group myRG \
  --name myapp \
  --vnet myVNet \
  --subnet mySubnet
```

### Private Endpoints

For making your app **inaccessible from the public internet on the inbound side**, you use a Private Endpoint. Traffic comes in through your VNet only. Often paired with VNet Integration to create a fully private app that talks to private backends.

### Hybrid Connections

Allows your app to reach on-premises resources (like an on-prem SQL Server) without VPN or ExpressRoute, by using a relay agent installed on-prem. Available from Basic tier upward.

---

## Authentication / Authorization (Easy Auth)

App Service has built-in authentication middleware you can enable without writing any auth code in your app — known as **Easy Auth** or **Authentication / Authorization**. It sits in front of your app and handles the OAuth/OIDC flow.

Supported identity providers out of the box: Microsoft Entra ID (Azure AD), Google, Facebook, Twitter/X, Apple, any OpenID Connect provider.

When enabled, unauthenticated requests are either rejected with a 401/403 or redirected to a login page — your choice. Authenticated user info is passed to your app in HTTP headers (`X-MS-CLIENT-PRINCIPAL`, `X-MS-TOKEN-AAD-ACCESS-TOKEN`, etc.).

This is great for quickly locking down an internal tool or API without touching application code.

---

## Kudu and the SCM Endpoint

Every App Service app has a companion site at `https://myapp.scm.azurewebsites.net` — the **Kudu** diagnostic console. This is where deployments happen and where you can:

- Browse the filesystem of your app
- Run commands in a debug console (bash or PowerShell)
- View deployment logs
- Download log files
- Trigger WebJobs manually

For the exam know that Kudu is the deployment engine and that `.scm.azurewebsites.net` is how you access it.

---

## Logging and Diagnostics

App Service supports several logging mechanisms:

**Application Logging** — your app's own log output. Can be written to the filesystem (temporary, resets after 12 hours) or to Blob Storage (persistent).

**Web Server Logging** — raw HTTP request logs in W3C format.

**Detailed Error Pages** — captures full error pages for 400+ responses.

**Failed Request Tracing** — detailed tracing for failed requests including IIS pipeline steps. Very useful for debugging 500 errors.

**Deployment Logging** — logs from the deployment process itself.

Enable streaming logs for real-time tailing:

```bash
az webapp log tail --resource-group myRG --name myapp
```

All of this can be routed to **Azure Monitor / Log Analytics** for longer retention, alerting, and querying with KQL.

---

## WebJobs

A built-in way to run background tasks alongside your web app — scripts or executables that run in the same App Service Plan context.

**Continuous WebJobs** — start immediately and run in a loop. Good for queue processors.

**Triggered WebJobs** — run on demand or on a schedule (CRON expression). Good for batch tasks.

Worth knowing for the exam, though Azure Functions has largely superseded WebJobs for new workloads. The key reason WebJobs still exist: they run inside your App Service Plan at no extra cost, while Functions on a Consumption plan bills per execution.

---

## Managed Identity with App Service

App Service supports both system-assigned and user-assigned managed identities, exactly like ACI and AKS. This is how your app authenticates to Key Vault, ACR, Storage, or any other Azure service without storing credentials.

```bash
# Enable system-assigned identity
az webapp identity assign \
  --resource-group myRG \
  --name myapp

# Get the principal ID to use in role assignments
az webapp identity show \
  --resource-group myRG \
  --name myapp \
  --query principalId \
  --output tsv
```

Then grant it whatever roles it needs on downstream resources, same pattern as ACI and AKS.

---

## AZ-204 Exam Summary

The heaviest areas for App Service on the exam are **deployment slots and swap behavior** (especially sticky settings), **scaling tiers and what each unlocks**, **the different deployment methods**, **VNet Integration vs. Private Endpoints** (outbound vs. inbound), **Key Vault references for secrets**, and **managed identity integration**. You should also be comfortable reading and writing the CLI commands for creating apps, configuring settings, and managing slots.

