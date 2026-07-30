# AZ-204: Developing Solutions for Microsoft Azure
## Complete Study Guide for Beginner Developers

---

## Table of Contents
1. [Exam Overview](#exam-overview)
2. [Prerequisites & Preparation Timeline](#prerequisites--preparation-timeline)
3. [Exam Objectives Breakdown](#exam-objectives-breakdown)
4. [Study Resources](#study-resources)
5. [Hands-On Lab Plan](#hands-on-lab-plan)
6. [Practice Questions Strategy](#practice-questions-strategy)
7. [Exam Day Tips](#exam-day-tips)

---

## Exam Overview

**Exam Code:** AZ-204  
**Certification:** Microsoft Certified: Azure Developer Associate  
**Exam Cost:** $165 USD  
**Duration:** 100 minutes  
**Passing Score:** 700/1000  
**Question Types:** Multiple choice, case studies, drag-and-drop, build lists, interactive tasks  
**Languages:** English, Japanese, Chinese (Simplified/Traditional), Korean, French, German, Spanish, Portuguese (Brazil), Italian

### What This Certification Validates
- End-to-end cloud solution development on Azure
- Designing, building, testing, and maintaining cloud applications
- Implementation of Azure compute, storage, security, and monitoring solutions
- Integration with Azure services and third-party APIs
- DevOps practices and cloud-native development

### Target Audience
Developers with:
- At least 2 years of programming experience
- Proficiency with Azure SDKs (C#, Python, JavaScript, Java)
- Experience with Azure CLI and Azure PowerShell
- Understanding of cloud concepts and development lifecycle

---

## Prerequisites & Preparation Timeline

### Recommended Background
Before starting AZ-204 preparation, ensure you have:
- **Azure Fundamentals (AZ-900)** - Recommended but not required
- **Programming Skills:** Proficiency in at least one language (C#, Python, JavaScript, Java)
- **Basic Cloud Concepts:** Understanding of IaaS, PaaS, SaaS
- **Development Tools:** Visual Studio Code, Git, command-line interfaces
- **REST APIs:** Basic understanding of HTTP methods and JSON

### Suggested Study Timeline

**For Complete Beginners (12-16 weeks):**
- Weeks 1-2: Azure fundamentals review
- Weeks 3-6: Compute solutions (App Service, Functions, Containers)
- Weeks 7-8: Storage solutions (Cosmos DB, Blob Storage)
- Weeks 9-10: Security and identity
- Weeks 11-12: Monitoring and integration
- Weeks 13-15: Practice exams and hands-on labs
- Week 16: Final review and exam

**For Experienced Developers (6-8 weeks):**
- Weeks 1-2: All compute solutions
- Weeks 3-4: Storage, security, and monitoring
- Weeks 5-6: Integration and messaging
- Weeks 7-8: Practice exams and weak area focus

---

## Exam Objectives Breakdown

### 1. Develop Azure Compute Solutions (25-30%)

#### 1.1 Implement Containerized Solutions

**Key Topics:**
- Container fundamentals (Docker concepts, images, containers)
- Azure Container Registry (ACR)
  - Creating and configuring ACR
  - Pushing and pulling images
  - ACR authentication methods
  - Image replication and geo-replication
- Azure Container Instances (ACI)
  - Creating and managing container groups
  - Environment variables and secrets
  - Persistent storage with Azure Files
  - Container restart policies
- Azure Container Apps
  - Creating Container Apps and environments
  - Configuring scaling rules
  - Managing revisions and traffic splitting
  - Implementing ingress and networking

**Study Focus:**
```bash
# Essential CLI Commands to Practice
az acr create
az acr build
az acr import
az container create
az containerapp create
az containerapp update
```

**Hands-On Labs:**
1. Build a custom Docker image and push to ACR
2. Deploy multi-container applications with ACI
3. Create a Container App with auto-scaling
4. Implement blue-green deployment with Container Apps

**Key Concepts to Master:**
- Dockerfile best practices (multi-stage builds, layer optimization)
- Container security (scanning, least privilege)
- Networking in containerized environments
- State management in containers

---

#### 1.2 Implement Azure App Service Web Apps

**Key Topics:**
- App Service Plans and pricing tiers
- Creating and configuring Web Apps
  - Runtime stack selection (.NET, Node.js, Python, Java, PHP)
  - Platform settings (32/64-bit, ARR affinity, websockets)
  - Always On feature
- Deployment methods
  - Local Git, GitHub Actions, Azure DevOps
  - ZIP deploy, FTP deployment
  - Continuous deployment setup
- Deployment slots
  - Creating staging/production slots
  - Slot-specific settings
  - Swap operations and auto-swap
  - Testing in production (TiP)
- Configuration and settings
  - Application settings and connection strings
  - TLS/SSL certificate management
  - Custom domains and DNS
  - CORS configuration
  - Service connections (managed identity to databases)
- Diagnostics and logging
  - Application logging (filesystem, blob storage)
  - Web server logging
  - Detailed error messages
  - Failed request tracing
  - Live metrics and diagnostic console
- Autoscaling
  - Scale-up vs scale-out
  - Metrics-based autoscaling rules
  - Schedule-based scaling
  - Default, minimum, maximum instances

**Study Focus:**
```bash
# Essential CLI Commands
az webapp create
az webapp deployment slot create
az webapp deployment slot swap
az webapp config appsettings set
az webapp log config
az monitor autoscale create
```

**Configuration Scenarios:**
```json
// appsettings.json structure for Azure
{
  "ConnectionStrings": {
    "SqlDatabase": "@Microsoft.KeyVault(...)"
  },
  "AppSettings": {
    "StorageAccountKey": "...",
    "SlotSpecificSetting": "..."
  }
}
```

**Hands-On Labs:**
1. Deploy a web application using multiple methods
2. Configure custom domains and SSL certificates
3. Implement blue-green deployment with slots
4. Set up autoscaling based on CPU and custom metrics
5. Configure application insights integration

**Key Concepts to Master:**
- When to use different App Service plan tiers
- Deployment slot swap mechanics and slot settings
- Kudu (SCM) site usage
- Webjobs vs Azure Functions
- App Service networking (VNet integration, hybrid connections)

---

#### 1.3 Implement Azure Functions

**Key Topics:**
- Function App architecture
  - Hosting plans: Consumption, Premium, Dedicated
  - Runtime versions and language support
  - Function app settings
- Triggers and bindings
  - HTTP trigger (authorization levels, route templates)
  - Timer trigger (CRON expressions)
  - Blob trigger and bindings
  - Queue trigger and bindings
  - Cosmos DB trigger and bindings
  - Event Grid trigger
  - Event Hub trigger
  - Service Bus trigger
- Durable Functions concepts
  - Function chaining
  - Fan-out/fan-in
  - Async HTTP APIs
  - Monitoring and management
- Function development
  - In-portal development
  - Local development with Core Tools
  - Dependency injection
  - Testing strategies

**Study Focus:**
```csharp
// HTTP Trigger Example
[FunctionName("HttpExample")]
public static async Task<IActionResult> Run(
    [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequest req,
    [Blob("container/{name}", FileAccess.Write)] Stream outputBlob,
    ILogger log)
{
    // Function logic
}
```

```javascript
// Timer Trigger Example (Node.js)
module.exports = async function (context, myTimer) {
    // Runs every 5 minutes: "0 */5 * * * *"
};
```

**Common CRON Expressions:**
- `0 */5 * * * *` - Every 5 minutes
- `0 0 * * * *` - Every hour
- `0 0 9 * * *` - Every day at 9 AM
- `0 0 9 * * 1-5` - Weekdays at 9 AM

**Hands-On Labs:**
1. Create HTTP-triggered function with blob output binding
2. Implement queue-triggered function with retry policies
3. Build timer-triggered function for scheduled tasks
4. Create Durable Function orchestration
5. Implement local development and testing workflow

**Key Concepts to Master:**
- Choosing the right hosting plan
- Binding direction (in, out, inout)
- Function authorization levels
- Cold start mitigation strategies
- Best practices for function design (stateless, idempotent)
- Application settings vs function.json configuration

---

### 2. Develop for Azure Storage (15-20%)

#### 2.1 Develop Solutions that Use Azure Cosmos DB

**Key Topics:**
- Cosmos DB fundamentals
  - Account, database, container, item hierarchy
  - Partition key selection and design
  - Request Units (RUs) and throughput
  - Consistency levels (Strong, Bounded Staleness, Session, Consistent Prefix, Eventual)
- SDK operations
  - Creating and configuring clients
  - CRUD operations on items
  - Querying with SQL API
  - Batch operations
  - Transactions within a partition
- Advanced features
  - Change feed processor
  - Time-to-Live (TTL)
  - Indexing policies
  - Stored procedures, triggers, UDFs
  - Global distribution and multi-region writes

**Study Focus:**
```csharp
// C# SDK v3 Examples
using Microsoft.Azure.Cosmos;

// Initialize client
CosmosClient client = new CosmosClient(endpoint, key);
Database database = await client.CreateDatabaseIfNotExistsAsync("mydb");
Container container = await database.CreateContainerIfNotExistsAsync(
    "mycontainer", "/partitionKey", 400);

// Create item
ItemResponse<MyItem> response = await container.CreateItemAsync(
    item, new PartitionKey(item.PartitionKey));

// Query items
var query = container.GetItemQueryIterator<MyItem>(
    "SELECT * FROM c WHERE c.category = @category",
    requestOptions: new QueryRequestOptions { PartitionKey = new PartitionKey("electronics") });

// Change feed processor
ChangeFeedProcessor processor = container
    .GetChangeFeedProcessorBuilder<MyItem>("processorName", HandleChangesAsync)
    .WithInstanceName("instance1")
    .WithLeaseContainer(leaseContainer)
    .Build();
```

**Consistency Level Decision Matrix:**
| Consistency | Use Case | Availability | Latency |
|-------------|----------|--------------|---------|
| Strong | Financial transactions | Lower | Higher |
| Bounded Staleness | Collaborative apps | Medium | Medium |
| Session | User-specific data | Higher | Lower |
| Consistent Prefix | Social feeds | Higher | Lower |
| Eventual | Non-critical data | Highest | Lowest |

**Hands-On Labs:**
1. Design partition key strategy for different scenarios
2. Implement CRUD operations with SDK
3. Create change feed processor for real-time updates
4. Query optimization and indexing policy tuning
5. Multi-region configuration and failover testing

**Key Concepts to Master:**
- Partition key design principles (cardinality, distribution)
- RU calculation and optimization
- When to use different consistency levels
- Change feed patterns (one processor per container partition)
- Cosmos DB vs. other database options

---

#### 2.2 Develop Solutions that Use Azure Blob Storage

**Key Topics:**
- Blob storage architecture
  - Storage accounts (Standard, Premium)
  - Container access levels (Private, Blob, Container)
  - Blob types (Block, Append, Page)
  - Access tiers (Hot, Cool, Archive)
- SDK operations
  - BlobServiceClient, BlobContainerClient, BlobClient
  - Uploading and downloading blobs
  - Blob properties and metadata
  - Lease operations
  - Listing blobs with prefix/delimiter
- Advanced features
  - Lifecycle management policies
  - Immutable storage (WORM)
  - Blob versioning
  - Soft delete
  - Point-in-time restore
  - Object replication
- Security
  - Shared Access Signatures (SAS)
  - Stored access policies
  - Azure AD authentication
  - Encryption at rest and in transit

**Study Focus:**
```csharp
// C# SDK v12 Examples
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;

// Upload blob with metadata
BlobClient blobClient = new BlobClient(connectionString, "container", "blob.txt");
var metadata = new Dictionary<string, string> { { "author", "John" } };
await blobClient.UploadAsync(stream, new BlobUploadOptions 
{ 
    Metadata = metadata,
    AccessTier = AccessTier.Cool 
});

// Set blob properties
await blobClient.SetHttpHeadersAsync(new BlobHttpHeaders
{
    ContentType = "application/pdf",
    CacheControl = "max-age=3600"
});

// Generate SAS token
BlobSasBuilder sasBuilder = new BlobSasBuilder
{
    BlobContainerName = "container",
    BlobName = "blob.txt",
    Resource = "b",
    StartsOn = DateTimeOffset.UtcNow,
    ExpiresOn = DateTimeOffset.UtcNow.AddHours(1)
};
sasBuilder.SetPermissions(BlobSasPermissions.Read);
```

**Lifecycle Management Policy Example:**
```json
{
  "rules": [
    {
      "name": "move-to-cool",
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["logs/"]
        },
        "actions": {
          "baseBlob": {
            "tierToCool": { "daysAfterModificationGreaterThan": 30 },
            "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
            "delete": { "daysAfterModificationGreaterThan": 365 }
          }
        }
      }
    }
  ]
}
```

**Hands-On Labs:**
1. Implement blob upload/download with progress tracking
2. Create lifecycle management policy for cost optimization
3. Configure blob versioning and soft delete
4. Generate and use SAS tokens with different permissions
5. Implement blob lease for distributed locking

**Key Concepts to Master:**
- When to use Block vs Page vs Append blobs
- Access tier economics and lifecycle policies
- SAS token best practices (minimal permissions, short expiry)
- Blob indexing and querying
- Optimizing large file uploads (chunking, parallelism)

---

### 3. Implement Azure Security (15-20%)

#### 3.1 Implement User Authentication and Authorization

**Key Topics:**
- Microsoft Identity Platform
  - Azure AD vs Azure AD B2C
  - Application registration
  - Authentication flows (authorization code, client credentials, device code)
  - Token acquisition and refresh
  - OAuth 2.0 and OpenID Connect
- Microsoft Entra ID (formerly Azure AD)
  - Service principals and managed identities
  - Application roles and permissions
  - Consent framework (admin vs user consent)
  - Multi-tenant applications
- Microsoft Authentication Library (MSAL)
  - MSAL.NET, MSAL.js, MSAL Python
  - Public vs confidential client applications
  - Token caching
  - Silent authentication
- Shared Access Signatures (SAS)
  - Service SAS vs Account SAS
  - User delegation SAS
  - Stored access policies
- Microsoft Graph API
  - Graph SDK usage
  - Common endpoints (/me, /users, /groups)
  - Permissions (delegated vs application)
  - Batch requests
  - Change notifications

**Study Focus:**
```csharp
// MSAL.NET Examples
using Microsoft.Identity.Client;

// Public client (desktop/mobile apps)
IPublicClientApplication app = PublicClientApplicationBuilder
    .Create(clientId)
    .WithAuthority(AzureCloudInstance.AzurePublic, tenantId)
    .WithRedirectUri("http://localhost")
    .Build();

// Confidential client (web apps/APIs)
IConfidentialClientApplication app = ConfidentialClientApplicationBuilder
    .Create(clientId)
    .WithClientSecret(clientSecret)
    .WithAuthority(new Uri($"https://login.microsoftonline.com/{tenantId}"))
    .Build();

// Acquire token silently, fallback to interactive
AuthenticationResult result;
try
{
    result = await app.AcquireTokenSilent(scopes, account).ExecuteAsync();
}
catch (MsalUiRequiredException)
{
    result = await app.AcquireTokenInteractive(scopes).ExecuteAsync();
}

// Microsoft Graph SDK
GraphServiceClient graphClient = new GraphServiceClient(authProvider);
var user = await graphClient.Me.Request().GetAsync();
var events = await graphClient.Me.Events.Request().Top(10).GetAsync();
```

**Authentication Flow Decision Matrix:**
| Flow | Use Case | User Interaction | Token Type |
|------|----------|------------------|------------|
| Authorization Code | Web apps | Yes | Access + Refresh |
| Client Credentials | Service-to-service | No | Access only |
| On-Behalf-Of | API calling another API | No | Access (delegated) |
| Device Code | IoT/CLI apps | Yes (different device) | Access + Refresh |

**Hands-On Labs:**
1. Register application in Azure AD
2. Implement OAuth 2.0 authentication in web app
3. Acquire tokens using MSAL in console app
4. Call Microsoft Graph API to read user data
5. Implement multi-tenant application

**Key Concepts to Master:**
- OAuth 2.0 vs OpenID Connect (authentication vs authorization)
- When to use each authentication flow
- Token lifetime and refresh token rotation
- API permissions (delegated vs application)
- Managed identity vs service principal

---

#### 3.2 Implement Secure Azure Solutions

**Key Topics:**
- Azure App Configuration
  - Creating App Configuration store
  - Key-value pairs and feature flags
  - Configuration refresh in applications
  - Integration with Azure Key Vault
- Azure Key Vault
  - Secrets, keys, and certificates management
  - Key Vault references in App Service
  - SDK operations (get, set, delete secrets)
  - Soft-delete and purge protection
  - Access policies vs RBAC
  - Key rotation strategies
- Managed Identities
  - System-assigned vs user-assigned
  - Assigning identity to Azure resources
  - Authenticating to Azure services
  - Using DefaultAzureCredential
  - Identity in local development

**Study Focus:**
```csharp
// Azure Key Vault SDK
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

// Using managed identity (works in Azure, uses VS/CLI locally)
var client = new SecretClient(
    new Uri($"https://{vaultName}.vault.azure.net/"),
    new DefaultAzureCredential());

// Secret operations
await client.SetSecretAsync("MySecret", "SecretValue");
KeyVaultSecret secret = await client.GetSecretAsync("MySecret");
await client.UpdateSecretPropertiesAsync("MySecret", 
    new SecretProperties { Enabled = false });

// Azure App Configuration
using Azure.Data.AppConfiguration;

var configClient = new ConfigurationClient(connectionString);
await configClient.SetConfigurationSettingAsync("AppName:Setting", "Value");

// Using Key Vault reference in App Configuration
await configClient.SetConfigurationSettingAsync(
    "ConnectionString",
    "{\"uri\":\"https://keyvault.vault.azure.net/secrets/DbConnection\"}",
    label: "Production");

// In application code with .NET
var builder = new ConfigurationBuilder();
builder.AddAzureAppConfiguration(options =>
{
    options.Connect(connectionString)
           .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()))
           .UseFeatureFlags();
});
```

**Managed Identity Example:**
```bash
# Enable system-assigned identity for App Service
az webapp identity assign --name myapp --resource-group mygroup

# Grant Key Vault access to managed identity
az keyvault set-policy --name myvault \
  --object-id <identity-principal-id> \
  --secret-permissions get list
```

**Hands-On Labs:**
1. Create Key Vault and manage secrets via SDK
2. Enable managed identity on App Service and access Key Vault
3. Set up App Configuration with Key Vault references
4. Implement secret rotation in application
5. Use DefaultAzureCredential for local and Azure authentication

**Key Concepts to Master:**
- When to use App Configuration vs Key Vault
- Managed identity authentication flow
- DefaultAzureCredential chain (order of credential providers)
- Key Vault access policies vs Azure RBAC
- Secret versioning and rotation strategies
- Never storing secrets in code or configuration files

---

### 4. Monitor, Troubleshoot, and Optimize Azure Solutions (5-10%)

#### 4.1 Monitor and Troubleshoot Solutions by Using Application Insights

**Key Topics:**
- Application Insights fundamentals
  - Workspace-based vs classic resources
  - Instrumentation key vs connection string
  - Auto-instrumentation vs manual SDK
  - Sampling strategies
- Monitoring capabilities
  - Live metrics stream
  - Application Map
  - Transaction search
  - Performance metrics
  - Failure analysis
- Logging and telemetry
  - ILogger integration
  - Custom events and metrics
  - Custom dimensions and properties
  - Correlation and operation IDs
  - Log levels and filtering
- Distributed tracing
  - Request tracking across services
  - Dependency tracking
  - End-to-end transaction view
- Alerts and availability
  - Metric alerts
  - Log query alerts
  - Web tests (URL ping, multi-step)
  - Smart detection and anomalies
- Query and analysis
  - Kusto Query Language (KQL) basics
  - Common query patterns
  - Workbooks and dashboards

**Study Focus:**
```csharp
// Application Insights SDK
using Microsoft.ApplicationInsights;
using Microsoft.ApplicationInsights.Extensibility;

// Initialize TelemetryClient
TelemetryConfiguration config = TelemetryConfiguration.CreateDefault();
config.ConnectionString = "InstrumentationKey=...";
var telemetryClient = new TelemetryClient(config);

// Track custom events
telemetryClient.TrackEvent("OrderPlaced", 
    properties: new Dictionary<string, string> 
    { 
        { "ProductId", "123" },
        { "UserId", "user@example.com" }
    },
    metrics: new Dictionary<string, double>
    {
        { "OrderValue", 99.99 }
    });

// Track custom metrics
telemetryClient.TrackMetric("QueueLength", queue.Count);

// Track dependencies
var startTime = DateTime.UtcNow;
var timer = Stopwatch.StartNew();
try
{
    var response = await httpClient.GetAsync(url);
    telemetryClient.TrackDependency("HTTP", url, "GET", startTime, timer.Elapsed, response.IsSuccessStatusCode);
}
catch (Exception ex)
{
    telemetryClient.TrackDependency("HTTP", url, "GET", startTime, timer.Elapsed, false);
    telemetryClient.TrackException(ex);
}

// Using ILogger (auto-captured by App Insights)
logger.LogInformation("Processing order {OrderId}", orderId);
logger.LogWarning("Low inventory for product {ProductId}", productId);
logger.LogError(exception, "Failed to process payment for order {OrderId}", orderId);
```

**Common KQL Queries:**
```kql
// Failed requests in last 24 hours
requests
| where timestamp > ago(24h)
| where success == false
| summarize count() by resultCode
| order by count_ desc

// Average response time by operation
requests
| where timestamp > ago(1h)
| summarize avg(duration) by operation_Name
| order by avg_duration desc

// Exceptions by type
exceptions
| where timestamp > ago(7d)
| summarize count() by type
| order by count_ desc

// Custom event analysis
customEvents
| where name == "OrderPlaced"
| extend productId = tostring(customDimensions.ProductId)
| summarize count(), avg(todouble(customMeasurements.OrderValue)) by productId
```

**Hands-On Labs:**
1. Enable Application Insights in App Service
2. Instrument application with custom telemetry
3. Create availability test and alert rules
4. Analyze performance issues using Application Map
5. Build custom dashboard with KQL queries

**Key Concepts to Master:**
- Difference between metrics and events
- Telemetry correlation across distributed systems
- Sampling techniques and impact
- When to use ILogger vs TelemetryClient
- KQL fundamentals for troubleshooting
- Cost optimization strategies (sampling, filtering)

---

### 5. Connect to and Consume Azure Services and Third-Party Services (20-25%)

#### 5.1 Implement Azure API Management

**Key Topics:**
- API Management concepts
  - Products, APIs, operations
  - Subscriptions and subscription keys
  - Developer portal
  - Backends and backend pools
- Instance creation and configuration
  - Pricing tiers (Developer, Basic, Standard, Premium, Consumption)
  - VNet integration
  - Custom domains and certificates
- API documentation
  - OpenAPI/Swagger import
  - API versioning strategies
  - API revision management
- Access control
  - Subscription keys
  - OAuth 2.0 integration
  - IP filtering
  - CORS configuration
- Policies
  - Inbound, outbound, backend, on-error sections
  - Policy expressions and variables
  - Common policies (rate limiting, caching, transformation)
  - Policy templates

**Study Focus:**
```xml
<!-- Common API Management Policies -->

<!-- Rate limiting -->
<inbound>
    <rate-limit calls="100" renewal-period="60" />
    <quota calls="10000" renewal-period="604800" />
</inbound>

<!-- Response caching -->
<inbound>
    <cache-lookup vary-by-developer="true" vary-by-developer-groups="false" />
</inbound>
<outbound>
    <cache-store duration="60" />
</outbound>

<!-- Request/Response transformation -->
<inbound>
    <set-header name="X-Custom-Header" exists-action="override">
        <value>@(context.Request.Headers.GetValueOrDefault("User-Agent"))</value>
    </set-header>
    <rewrite-uri template="/api/v2/{path}" />
</inbound>
<outbound>
    <set-body>@{
        var response = context.Response.Body.As<JObject>();
        response["timestamp"] = DateTime.UtcNow.ToString();
        return response.ToString();
    }</set-body>
</outbound>

<!-- Backend routing -->
<backend>
    <choose>
        <when condition="@(context.Request.Url.Query.GetValueOrDefault("version") == "2")">
            <set-backend-service base-url="https://api-v2.example.com" />
        </when>
        <otherwise>
            <set-backend-service base-url="https://api-v1.example.com" />
        </otherwise>
    </choose>
</backend>

<!-- Error handling -->
<on-error>
    <set-variable name="errorMessage" value="@(context.LastError.Message)" />
    <return-response>
        <set-status code="500" reason="Internal Server Error" />
        <set-body>@{
            return new JObject(
                new JProperty("error", context.LastError.Message),
                new JProperty("requestId", context.RequestId)
            ).ToString();
        }</set-body>
    </return-response>
</on-error>
```

**Hands-On Labs:**
1. Create APIM instance and import OpenAPI spec
2. Implement rate limiting and quota policies
3. Configure OAuth 2.0 authentication
4. Set up response caching with variation
5. Implement request transformation policies

**Key Concepts to Master:**
- When to use APIM vs Azure Front Door
- Policy execution order (inbound → backend → outbound → on-error)
- Policy expressions and context variables
- API versioning vs revisions
- Subscription key management and security

---

#### 5.2 Develop Event-Based Solutions

**Key Topics:**
- Azure Event Grid
  - Event sources and handlers
  - System topics and custom topics
  - Event schema (Event Grid, CloudEvents)
  - Event filtering (subject, advanced filters)
  - Event subscriptions and dead-lettering
  - Retry policies
- Azure Event Hubs
  - Event Hub namespace and Event Hubs
  - Producer and consumer patterns
  - Partitions and partition keys
  - Consumer groups
  - Checkpointing and offset management
  - Event Hubs Capture to Blob/Data Lake
  - Throughput units vs Processing units (Standard vs Premium)

**Study Focus:**
```csharp
// Event Grid - Publishing custom events
using Azure.Messaging.EventGrid;

EventGridPublisherClient client = new EventGridPublisherClient(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey));

var events = new List<EventGridEvent>
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "OrderPlaced",
        dataVersion: "1.0",
        data: new { OrderId = "12345", Total = 99.99 })
};

await client.SendEventsAsync(events);

// Event Grid - Handling events in Azure Function
[FunctionName("HandleOrderEvent")]
public static async Task Run(
    [EventGridTrigger] EventGridEvent eventGridEvent,
    ILogger log)
{
    log.LogInformation($"Event type: {eventGridEvent.EventType}");
    var orderData = eventGridEvent.Data.ToObjectFromJson<OrderData>();
}

// Event Hubs - Producing events
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;

await using var producer = new EventHubProducerClient(connectionString, eventHubName);

var eventBatch = await producer.CreateBatchAsync();
eventBatch.TryAdd(new EventData(Encoding.UTF8.GetBytes("Event 1")));
eventBatch.TryAdd(new EventData(Encoding.UTF8.GetBytes("Event 2")));

await producer.SendAsync(eventBatch);

// Event Hubs - Consuming events
using Azure.Messaging.EventHubs.Consumer;
using Azure.Messaging.EventHubs.Processor;

var storageClient = new BlobContainerClient(storageConnectionString, containerName);
var processor = new EventProcessorClient(
    storageClient,
    EventHubConsumerClient.DefaultConsumerGroupName,
    connectionString,
    eventHubName);

processor.ProcessEventAsync += async (args) =>
{
    string data = Encoding.UTF8.GetString(args.Data.Body.ToArray());
    await args.UpdateCheckpointAsync();
};

processor.ProcessErrorAsync += (args) =>
{
    Console.WriteLine($"Error: {args.Exception.Message}");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync();
```

**Event Grid vs Event Hubs Comparison:**
| Feature | Event Grid | Event Hubs |
|---------|-----------|------------|
| Pattern | Pub-Sub (push) | Streaming (pull) |
| Throughput | Millions of events/sec | Millions of events/sec |
| Ordering | No guarantee | Per-partition ordering |
| Retention | 24 hours | 1-7 days (90 days Premium) |
| Use Case | Reactive programming | High-throughput streaming |
| Examples | Resource notifications | IoT telemetry, logs |

**Hands-On Labs:**
1. Create custom Event Grid topic and subscription
2. Implement event filtering and dead-lettering
3. Send events to Event Hub with partitioning
4. Process Event Hub stream with checkpointing
5. Configure Event Hub Capture to storage

**Key Concepts to Master:**
- Event Grid event schema and CloudEvents format
- Partition key selection for Event Hubs
- Event Hub consumer groups and offset management
- Retry and dead-lettering strategies
- When to use Event Grid vs Event Hubs vs Service Bus

---

#### 5.3 Develop Message-Based Solutions

**Key Topics:**
- Azure Service Bus
  - Queues vs Topics/Subscriptions
  - Message properties and headers
  - Message sessions (FIFO guarantee)
  - Dead-letter queues
  - Message deferral and scheduling
  - Transactions and batch operations
  - Duplicate detection
  - Auto-forwarding and auto-delete
- Azure Queue Storage
  - Queue operations (enqueue, dequeue, peek)
  - Message visibility timeout
  - Poison message handling
  - Queue metadata and properties

**Study Focus:**
```csharp
// Service Bus - Sending messages
using Azure.Messaging.ServiceBus;

await using var client = new ServiceBusClient(connectionString);
ServiceBusSender sender = client.CreateSender(queueName);

// Send single message
var message = new ServiceBusMessage("Hello, Service Bus!")
{
    Subject = "OrderProcessing",
    TimeToLive = TimeSpan.FromMinutes(5),
    MessageId = Guid.NewGuid().ToString()
};
message.ApplicationProperties.Add("Priority", "High");
await sender.SendMessageAsync(message);

// Send batch
var messageBatch = await sender.CreateMessageBatchAsync();
for (int i = 0; i < 10; i++)
{
    if (!messageBatch.TryAddMessage(new ServiceBusMessage($"Message {i}")))
    {
        await sender.SendMessagesAsync(messageBatch);
        messageBatch = await sender.CreateMessageBatchAsync();
        messageBatch.TryAddMessage(new ServiceBusMessage($"Message {i}"));
    }
}
await sender.SendMessagesAsync(messageBatch);

// Service Bus - Receiving messages
ServiceBusReceiver receiver = client.CreateReceiver(queueName);

while (true)
{
    ServiceBusReceivedMessage message = await receiver.ReceiveMessageAsync(TimeSpan.FromSeconds(30));
    if (message == null) break;

    try
    {
        // Process message
        Console.WriteLine($"Message: {message.Body}");
        
        // Complete the message
        await receiver.CompleteMessageAsync(message);
    }
    catch (Exception ex)
    {
        // Dead-letter the message
        await receiver.DeadLetterMessageAsync(message, 
            deadLetterReason: "ProcessingError",
            deadLetterErrorDescription: ex.Message);
    }
}

// Service Bus - Sessions (FIFO)
ServiceBusSessionReceiver sessionReceiver = await client.AcceptNextSessionAsync(queueName);
while (true)
{
    var message = await sessionReceiver.ReceiveMessageAsync(TimeSpan.FromSeconds(5));
    if (message == null) break;
    
    await sessionReceiver.CompleteMessageAsync(message);
}

// Queue Storage - Basic operations
using Azure.Storage.Queues;

QueueClient queueClient = new QueueClient(connectionString, queueName);
await queueClient.CreateIfNotExistsAsync();

// Send message
await queueClient.SendMessageAsync("Hello, Queue!");

// Receive and process
QueueMessage[] messages = await queueClient.ReceiveMessagesAsync(maxMessages: 10);
foreach (var message in messages)
{
    Console.WriteLine($"Message: {message.MessageText}");
    await queueClient.DeleteMessageAsync(message.MessageId, message.PopReceipt);
}
```

**Service Bus vs Queue Storage Comparison:**
| Feature | Service Bus | Queue Storage |
|---------|-------------|---------------|
| Max message size | 256 KB (1 MB Premium) | 64 KB |
| Ordering | Sessions guarantee FIFO | No ordering guarantee |
| Max queue size | 80 GB+ | Unlimited |
| TTL | Configurable | 7 days max |
| Duplicate detection | Yes | No |
| Transactions | Yes | No |
| Cost | Higher | Lower |
| Use case | Enterprise messaging | Simple async processing |

**Hands-On Labs:**
1. Implement Service Bus queue sender and receiver
2. Configure topic subscriptions with filters
3. Handle dead-letter messages
4. Implement session-based processing
5. Compare Queue Storage vs Service Bus performance

**Key Concepts to Master:**
- When to use queues vs topics/subscriptions
- Message settlement operations (complete, abandon, dead-letter, defer)
- Session-based processing for ordering
- Duplicate detection windows
- At-least-once vs exactly-once delivery semantics
- Message batching for performance

---

## Study Resources

### Official Microsoft Resources
1. **Microsoft Learn** (Free)
   - [AZ-204 Learning Paths](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/)
   - Interactive modules with hands-on sandboxes
   - Progress tracking and achievements

2. **Microsoft Documentation**
   - Azure service documentation: https://docs.microsoft.com/azure
   - Code samples and quickstarts
   - SDK reference documentation

3. **Microsoft Exam Readiness Zone** (Free)
   - Video series covering all exam objectives
   - Taught by Microsoft experts
   - 5-part series for AZ-204

4. **Official Practice Assessment** (Free)
   - Available at Microsoft Learn
   - Realistic exam questions
   - Identifies knowledge gaps

### Recommended Training Courses

**Video Courses:**
1. **Scott Duffy's AZ-204 Course** (Udemy)
   - Comprehensive coverage, regularly updated
   - Includes practice test
   - ~30 hours of content

2. **Alan Rodrigues AZ-204 Course** (Udemy)
   - In-depth explanations
   - Multiple practice tests
   - Good for beginners

3. **Coursera - Microsoft Azure Developer** (Free audit)
   - 8-course professional certificate
   - Hands-on with Azure sandbox
   - Created by Microsoft

**Books:**
1. "Exam Ref AZ-204 Developing Solutions for Microsoft Azure"
   - Official Microsoft exam reference
   - Organized by exam objectives

### Practice Question Resources

**Recommended Sources:**
1. **MeasureUp** ($99-149)
   - Most realistic practice tests
   - Test pass guarantee
   - 200+ questions with detailed explanations

2. **Whizlabs** ($20-40)
   - 250+ practice questions
   - Full-length mock exams
   - Scenario-based questions

3. **Exam Topics** (Free with registration)
   - Community-contributed questions
   - Discussion forums
   - Use with caution (quality varies)

4. **Microsoft Official Practice Assessment** (Free)
   - ~50 questions
   - Similar style to real exam
   - Take multiple times

### Hands-On Practice

**Azure Free Account:**
- $200 credit for 30 days
- 12 months of free services
- Always-free services
- Sign up: https://azure.microsoft.com/free

**Azure Sandbox (Microsoft Learn):**
- Free temporary Azure environment
- No credit card required
- Integrated with learning modules
- 10 sandboxes per day

### Community Resources

1. **r/AzureCertification** (Reddit)
   - Study tips and experiences
   - Practice question discussions
   - Exam feedback

2. **Microsoft Q&A**
   - Technical question forum
   - Microsoft MVPs and experts
   - Tag: azure-developer

3. **Azure Developer Community**
   - Tech Community forums
   - Blog posts and articles
   - Webinars and events

---

## Hands-On Lab Plan

### Week 1-2: Compute Foundations
**Labs:**
1. Create Docker image and push to ACR
2. Deploy multi-container app with ACI
3. Create App Service with multiple deployment slots
4. Implement autoscaling rules
5. Create HTTP-triggered Function with blob bindings

**Verification:**
- [ ] Can explain difference between ACI and Container Apps
- [ ] Can perform blue-green deployment
- [ ] Understand when to use Consumption vs Premium Functions plan

### Week 3-4: Storage and Data
**Labs:**
1. Design Cosmos DB partition strategy for e-commerce app
2. Implement CRUD operations with Cosmos DB SDK
3. Create change feed processor
4. Upload/download blobs with metadata
5. Implement lifecycle management policy

**Verification:**
- [ ] Can choose appropriate consistency level
- [ ] Can calculate RU requirements
- [ ] Understand blob access tiers and costs

### Week 5-6: Security and Identity
**Labs:**
1. Register app in Azure AD and acquire tokens
2. Call Microsoft Graph API
3. Store secrets in Key Vault
4. Use managed identity from App Service to Key Vault
5. Implement SAS tokens with minimal permissions

**Verification:**
- [ ] Can explain OAuth 2.0 flows
- [ ] Understand MSAL token caching
- [ ] Can use DefaultAzureCredential

### Week 7-8: Messaging and Integration
**Labs:**
1. Create Event Grid custom topic
2. Send events to Event Hub with partitioning
3. Process Event Hub stream with checkpointing
4. Send/receive Service Bus messages
5. Implement APIM policies

**Verification:**
- [ ] Can choose between Event Grid/Event Hubs/Service Bus
- [ ] Understand partition key impact
- [ ] Can write basic APIM policies

### Week 9-10: Monitoring and Optimization
**Labs:**
1. Enable Application Insights
2. Add custom telemetry
3. Create availability tests
4. Write KQL queries
5. Set up alerts

**Verification:**
- [ ] Can troubleshoot using Application Map
- [ ] Understand correlation in distributed systems
- [ ] Can analyze performance issues

---

## Practice Questions Strategy

### Phase 1: Knowledge Check (Weeks 1-10)
- Take topic-specific quizzes after each learning module
- Use Microsoft Learn built-in assessments
- Don't worry about passing scores yet
- Focus on understanding explanations

### Phase 2: Practice Tests (Weeks 11-14)
**Week 11:**
- Take first full practice exam
- Don't time yourself
- Note all incorrect answers
- Review explanations thoroughly

**Week 12:**
- Review weak areas identified
- Hands-on labs for difficult topics
- Take second practice exam (untimed)
- Target: 70%+ score

**Week 13:**
- Take timed practice exam
- Simulate real conditions (100 minutes)
- No resources or notes
- Target: 80%+ score

**Week 14:**
- Take final practice exam (timed)
- Focus on time management
- Target: 85-90%+ score
- If passing 3 consecutive times at 90%, you're ready

### Question Analysis Technique
For each incorrect answer:
1. Why was my answer wrong?
2. What concept did I misunderstand?
3. Where can I review this topic?
4. What hands-on lab would reinforce this?

### Common Question Patterns
1. **Scenario-based**: Given requirements, choose the best service
2. **Code completion**: Fill in the blank with correct SDK method
3. **Configuration**: Select appropriate settings for a situation
4. **Troubleshooting**: Identify the cause of an issue
5. **Best practices**: Choose the most secure/efficient approach

---

## Exam Day Tips

### Week Before Exam
- [ ] Review all objectives one more time
- [ ] Retake any failed practice tests
- [ ] Review incorrect answers from all practice tests
- [ ] Get good sleep every night
- [ ] Don't cram new material

### Day Before Exam
- [ ] Light review of key concepts only
- [ ] Prepare workspace if testing at home
- [ ] Test webcam and microphone
- [ ] Prepare valid ID
- [ ] Get 8 hours of sleep
- [ ] No alcohol or heavy meals

### Exam Day
**Before Exam:**
- [ ] Eat a good meal 2 hours before
- [ ] Arrive/login 30 minutes early
- [ ] Use the bathroom
- [ ] Have water available
- [ ] Clear desk area (for online proctoring)

**During Exam:**
- **Time Management**: ~1.2 minutes per question (100 min / ~80 questions)
- **Strategy**: Mark difficult questions for review
- **Case Studies**: Read questions before the scenario
- **Code Questions**: Eliminate obviously wrong answers first
- **Don't Panic**: If stuck, make an educated guess and move on

**Question Strategies:**
1. Read carefully - look for "EXCEPT", "NOT", "LEAST"
2. Eliminate obviously wrong answers
3. Consider cost, security, and simplicity
4. Choose Azure-native solutions over custom code
5. When in doubt, choose the most secure option

### After Exam
- Results available immediately
- Passing score: 700/1000
- If you fail:
  - Review score report for weak areas
  - Must wait 24 hours for first retake
  - Focus hands-on practice on weak areas
  - Retake within 30 days while knowledge is fresh

---

## Key Success Factors

### 1. Hands-On Experience is Critical
- Reading alone is not enough
- Build actual projects using the services
- Break things and fix them
- Use Azure Portal, CLI, and SDK

### 2. Understand Concepts, Not Just Facts
- Why this service over another?
- What are the trade-offs?
- When would you NOT use this?
- How do services integrate?

### 3. Focus on Exam Objectives
- Not every Azure service is on the exam
- Study guide is your roadmap
- Prioritize high-percentage topics
- Don't get distracted by tangential topics

### 4. Practice Questions are Essential
- Expose you to question formats
- Identify weak areas
- Build exam stamina
- Improve time management

### 5. Community and Support
- Join study groups
- Ask questions on forums
- Share your knowledge
- Learn from others' experiences

---

## Quick Reference Cheat Sheet

### Service Decision Matrix

**Compute:**
- Containers, full control → ACI or AKS
- Serverless containers, auto-scale → Container Apps
- Web hosting → App Service
- Event-driven code → Azure Functions
- Long-running background tasks → WebJobs

**Storage:**
- NoSQL, global distribution → Cosmos DB
- Relational database → Azure SQL Database
- Files, unstructured data → Blob Storage
- Shared file system → Azure Files
- Big data analytics → Data Lake Storage

**Messaging:**
- Discrete events, reactive → Event Grid
- High-throughput streaming → Event Hubs
- Enterprise messaging, ordering → Service Bus
- Simple async queue → Queue Storage

**Security:**
- User authentication → Azure AD / Microsoft Identity Platform
- App-to-app auth → Managed Identity
- Secrets management → Key Vault
- Feature flags, config → App Configuration

**Monitoring:**
- Application performance → Application Insights
- Infrastructure metrics → Azure Monitor
- Logging → Log Analytics
- Alerting → Azure Monitor Alerts

### Common CLI Commands

```bash
# Login
az login
az account set --subscription "subscription-name"

# App Service
az webapp create --name myapp --resource-group rg --plan myplan
az webapp deployment slot create --name myapp --resource-group rg --slot staging
az webapp deployment slot swap --name myapp --resource-group rg --slot staging

# Functions
az functionapp create --name myfunc --resource-group rg --storage-account mystorage --consumption-plan-location eastus

# Container Registry
az acr create --name myacr --resource-group rg --sku Basic
az acr build --registry myacr --image myimage:v1 .

# Key Vault
az keyvault create --name myvault --resource-group rg
az keyvault secret set --vault-name myvault --name MySecret --value SecretValue
az keyvault secret show --vault-name myvault --name MySecret

# Cosmos DB
az cosmosdb create --name mycosmosdb --resource-group rg
az cosmosdb sql database create --account-name mycosmosdb --name mydb --resource-group rg
az cosmosdb sql container create --account-name mycosmosdb --database-name mydb --name mycontainer --partition-key-path /pk --resource-group rg

# Service Bus
az servicebus namespace create --name myns --resource-group rg
az servicebus queue create --namespace-name myns --name myqueue --resource-group rg
az servicebus topic create --namespace-name myns --name mytopic --resource-group rg
```

---

## Final Checklist Before Scheduling Exam

- [ ] Completed all official Microsoft Learn paths
- [ ] Hands-on labs for each major service
- [ ] Consistent 85%+ on practice exams
- [ ] Understand all exam objectives
- [ ] Can explain when to use each service
- [ ] Comfortable with C# or Python SDK code
- [ ] Know Azure CLI commands
- [ ] Can write basic KQL queries
- [ ] Understand ARM templates basics
- [ ] Reviewed score reports from practice tests

---

## Additional Tips for Beginners

### 1. Start with Fundamentals
If you're new to Azure, consider:
- Taking AZ-900 first (optional but helpful)
- Understanding cloud concepts
- Learning Azure Portal navigation
- Getting comfortable with CLI

### 2. Choose Your Primary Language
- C# is most common in examples
- Python is growing in popularity
- JavaScript/TypeScript for web apps
- Java for enterprise

### 3. Development Environment Setup
```bash
# Install Azure CLI
# Windows: Download installer from Microsoft
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Install SDKs (C# example)
dotnet add package Azure.Storage.Blobs
dotnet add package Azure.Identity
dotnet add package Microsoft.Azure.Cosmos
dotnet add package Azure.Messaging.ServiceBus
dotnet add package Microsoft.ApplicationInsights
```

### 4. Cost Management During Study
- Use free tier services whenever possible
- Delete resources after each lab
- Set up budget alerts
- Use Azure Sandbox (free)
- Stop/deallocate VMs when not in use

### 5. Learning Style Adaptation
**Visual Learners:**
- Watch video courses (Scott Duffy, Alan Rodrigues)
- Draw architecture diagrams
- Use Azure Portal for exploration

**Reading/Writing Learners:**
- Follow Microsoft Docs tutorials
- Take detailed notes
- Write blog posts about what you learn

**Kinesthetic Learners:**
- Focus heavily on hands-on labs
- Build actual projects
- Type out code samples (don't copy-paste)

### 6. Common Beginner Mistakes to Avoid
- ❌ Memorizing without understanding
- ❌ Skipping hands-on practice
- ❌ Relying only on dumps (they're often outdated/wrong)
- ❌ Not reading questions carefully
- ❌ Studying too many resources (stick to 2-3)
- ✅ Understand the "why" behind each service
- ✅ Build real projects
- ✅ Use official Microsoft resources
- ✅ Practice time management
- ✅ Focus on exam objectives

---

## Motivation and Mindset

### This Certification Will Help You:
- Validate your Azure development skills
- Stand out in job applications
- Increase earning potential (avg. 15-20% salary increase)
- Gain confidence in cloud development
- Open doors to advanced certifications (AZ-400, AZ-305)

### When You Feel Overwhelmed:
- Break study into small chunks (1 objective at a time)
- Remember that everyone finds some topics difficult
- Join study groups for support
- Take breaks when needed
- Celebrate small wins

### You've Got This!
The AZ-204 is challenging but absolutely achievable with:
- Consistent daily study (1-2 hours)
- Hands-on practice
- Quality resources
- Practice exams
- Determination

---

## Next Steps After AZ-204

### Career Paths:
1. **Azure Developer**
   - Build cloud-native applications
   - Salary: $90K-140K

2. **Cloud Solutions Architect**
   - Get AZ-305 next
   - Design enterprise solutions
   - Salary: $120K-180K

3. **DevOps Engineer**
   - Get AZ-400 next
   - CI/CD, automation
   - Salary: $100K-160K

### Advanced Certifications:
- **AZ-400**: DevOps Engineer Expert
- **AZ-305**: Azure Solutions Architect Expert
- **AZ-500**: Azure Security Engineer
- **Specialty**: AI, Data, IoT

---

**Good luck with your AZ-204 journey! You're investing in a valuable skill that will serve you throughout your career.**

**Remember:** The certification is not the goal - the knowledge and skills you gain are what matter most. Build projects, solve problems, and enjoy the learning process!

---

*Last Updated: January 2026*
*Based on exam version as of July 21, 2025*
