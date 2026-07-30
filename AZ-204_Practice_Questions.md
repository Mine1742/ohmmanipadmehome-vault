# AZ-204 Practice Questions by Exam Objective
## Study Aid and Self-Assessment Tool

---

## How to Use This Document

1. **Study by Topic**: Work through questions as you complete each objective
2. **Self-Assessment**: Test yourself before moving to the next topic
3. **Final Review**: Use as a comprehensive review before the exam
4. **Answer Key**: Detailed explanations at the end of each section

**Note**: These are practice questions to help you prepare. They are similar in style to the actual exam but are not actual exam questions.

---

## Section 1: Develop Azure Compute Solutions (25-30%)

### Topic 1.1: Implement Containerized Solutions

**Question 1:**
You are developing a containerized application that needs to be deployed to Azure. The application consists of a web frontend and a background processing service. You need to ensure the containers can scale independently based on CPU usage.

Which Azure service should you use?

A) Azure Container Instances (ACI)
B) Azure Container Apps
C) Azure App Service with containers
D) Azure Kubernetes Service (AKS)

**Answer: B** - Azure Container Apps

**Explanation:** Container Apps provides built-in autoscaling based on HTTP traffic, CPU, memory, and custom metrics. Each container in a Container App can scale independently. ACI doesn't support autoscaling. AKS requires more management overhead. App Service with containers doesn't allow independent scaling of multiple containers.

---

**Question 2:**
You need to build a Docker image from source code and push it to Azure Container Registry using the Azure CLI. The image should be tagged as 'v1.2.0'.

Which command should you use?

A) `az acr build --registry myacr --image myapp:v1.2.0 --file Dockerfile .`
B) `az acr push --registry myacr --image myapp:v1.2.0 .`
C) `az acr create --registry myacr --image myapp:v1.2.0 .`
D) `az container create --registry myacr --image myapp:v1.2.0 .`

**Answer: A** - `az acr build --registry myacr --image myapp:v1.2.0 --file Dockerfile .`

**Explanation:** The `az acr build` command builds the image in Azure (no local Docker required) and pushes it to ACR in one step. Option B uses `push` which requires a pre-built image. C and D use incorrect commands.

---

**Question 3:**
You have an Azure Container Instance that runs a data processing job. The job downloads files from Azure Blob Storage, processes them, and uploads results. The container should only run once per execution and should not restart on failure.

What should you configure?

A) Set restart policy to 'Always'
B) Set restart policy to 'OnFailure'
C) Set restart policy to 'Never'
D) Configure auto-scaling rules

**Answer: C** - Set restart policy to 'Never'

**Explanation:** For one-time jobs that shouldn't retry on failure, use 'Never'. 'Always' would continuously restart, 'OnFailure' would retry on failures. Auto-scaling is not relevant for one-time jobs.

---

**Question 4:**
Your company wants to deploy a container application that requires persistent storage across container restarts. The storage should be accessible to multiple containers.

What should you use?

A) Azure Container Apps with built-in storage
B) Azure Container Instances with Azure Files volume mount
C) Azure Container Instances with emptyDir volume
D) Azure Container Registry with blob storage

**Answer: B** - Azure Container Instances with Azure Files volume mount

**Explanation:** Azure Files provides SMB/NFS file shares that can be mounted to multiple container instances, providing persistent storage. emptyDir is ephemeral and lost on restart.

---

**Question 5:**
You are deploying a Container App that receives varying amounts of HTTP traffic. You need to configure scaling to handle between 1 and 20 concurrent requests per container instance.

Which scaling rule should you configure?

```yaml
A) 
scale:
  minReplicas: 1
  maxReplicas: 20
  rules:
  - name: http-rule
    http:
      metadata:
        concurrentRequests: '10'

B)
scale:
  minReplicas: 10
  maxReplicas: 20
  rules:
  - name: cpu-rule
    custom:
      type: cpu
      metadata:
        value: '70'

C)
scale:
  replicas: 1
  rules:
  - name: http-rule
    http:
      requests: 20

D)
scale:
  minReplicas: 1
  maxReplicas: 1
  rules:
  - name: http-rule
    http:
      metadata:
        concurrentRequests: '20'
```

**Answer: A** - The first configuration

**Explanation:** This correctly configures HTTP-based scaling with 1-20 replicas based on concurrent requests. The concurrentRequests metadata specifies the target number of requests per instance.

---

### Topic 1.2: Implement Azure App Service Web Apps

**Question 6:**
You are deploying a production web application to Azure App Service. The application should be available 99.95% of the time and should minimize costs.

Which App Service plan tier should you use?

A) Free (F1)
B) Shared (D1)
C) Basic (B1)
D) Standard (S1)

**Answer: D** - Standard (S1)

**Explanation:** Standard tier provides 99.95% SLA and includes deployment slots, autoscaling, and custom domains. Free and Shared don't provide SLAs. Basic provides SLA but doesn't support deployment slots or autoscaling.

---

**Question 7:**
You need to implement a blue-green deployment for your web application. After deploying to the staging slot, you want to route 10% of traffic to the new version before performing a full swap.

What feature should you use?

A) Deployment slots with auto-swap
B) Deployment slots with testing in production
C) Application Gateway with backend pools
D) Azure Front Door with weighted routing

**Answer: B** - Deployment slots with testing in production

**Explanation:** Testing in Production (TiP) allows routing a percentage of traffic to different slots before a full swap. This is perfect for gradual rollouts.

---

**Question 8:**
Your web application requires an SSL certificate for a custom domain. The certificate should be automatically renewed and managed by Azure.

What should you do?

A) Upload a .pfx certificate to App Service
B) Create a free App Service Managed Certificate
C) Use Azure Key Vault to store the certificate
D) Configure Let's Encrypt manually

**Answer: B** - Create a free App Service Managed Certificate

**Explanation:** App Service Managed Certificates are free, automatically renewed, and fully managed by Azure. They're the simplest option for custom domains.

---

**Question 9:**
You need to configure autoscaling for an App Service. The application should scale out when average CPU exceeds 70% for 5 minutes and scale in when it drops below 30%.

Complete the Azure CLI command:

```bash
az monitor autoscale create \
  --resource-group myRG \
  --resource myAppServicePlan \
  --resource-type Microsoft.Web/serverfarms \
  --min-count 1 \
  --max-count 5 \
  --count 2 \
  --scale-out-cpu-percentage _____ \
  --scale-out-duration _____ \
  --scale-in-cpu-percentage _____ \
  --scale-in-duration _____
```

A) 70, 5, 30, 5
B) 30, 5, 70, 5
C) 70, 300, 30, 300
D) 30, 300, 70, 300

**Answer: C** - 70, 300, 30, 300

**Explanation:** Duration is in seconds (300 seconds = 5 minutes). Scale out at 70% CPU, scale in at 30% CPU.

---

**Question 10:**
You deployed a new version to your staging slot. After testing, you want to swap to production, but some settings should remain in the staging slot.

Which settings are swapped during a slot swap? (Choose all that apply)

A) App settings marked as "deployment slot setting"
B) Connection strings marked as "deployment slot setting"
C) General settings like Always On
D) Custom domain SSL bindings
E) App settings without the "deployment slot setting" flag

**Answer: C, E** - General settings and non-slot-specific app settings

**Explanation:** Settings marked as "deployment slot setting" (A and B) stay with their slot. SSL bindings (D) stay with the domain. General settings and unmarked app settings are swapped.

---

**Question 11:**
You need to enable Application Insights for your web app and configure it to send telemetry data. The connection string is stored in Azure Key Vault.

What's the correct approach?

A) Set APPINSIGHTS_INSTRUMENTATIONKEY app setting to @Microsoft.KeyVault(SecretUri=...)
B) Set APPLICATIONINSIGHTS_CONNECTION_STRING app setting to @Microsoft.KeyVault(SecretUri=...)
C) Enable Application Insights in the portal and manually enter the key
D) Use managed identity and configure in code only

**Answer: B** - Set APPLICATIONINSIGHTS_CONNECTION_STRING to Key Vault reference

**Explanation:** The correct app setting name is `APPLICATIONINSIGHTS_CONNECTION_STRING` and it supports Key Vault references using the @ syntax.

---

### Topic 1.3: Implement Azure Functions

**Question 12:**
You are developing an Azure Function that processes uploaded images. The function should trigger when a new blob is added to a container named 'uploads'.

Complete the function signature:

```csharp
[FunctionName("ProcessImage")]
public static void Run(
    [_____("uploads/{name}", Connection = "AzureWebJobsStorage")] Stream imageBlob,
    string name,
    ILogger log)
{
    log.LogInformation($"Processing {name}");
}
```

A) BlobTrigger
B) Blob
C) QueueTrigger
D) HttpTrigger

**Answer: A** - BlobTrigger

**Explanation:** BlobTrigger activates when a new blob is created. The path pattern "uploads/{name}" monitors the uploads container and captures the blob name.

---

**Question 13:**
You need to create a timer-triggered function that runs every weekday at 6:00 AM UTC.

What CRON expression should you use?

A) `0 0 6 * * *`
B) `0 6 * * * *`
C) `0 0 6 * * 1-5`
D) `0 6 * * 1-5 *`

**Answer: C** - `0 0 6 * * 1-5`

**Explanation:** CRON format: second minute hour day month weekday. `0 0 6 * * 1-5` means 0 seconds, 0 minutes, 6 hours (6 AM), every day, every month, Monday-Friday (1-5).

---

**Question 14:**
Your company wants to minimize costs for Azure Functions that run infrequently (10-20 times per day) but may need to scale quickly during peak times.

Which hosting plan should you choose?

A) Consumption plan
B) Premium plan
C) Dedicated (App Service) plan
D) Container Apps

**Answer: A** - Consumption plan

**Explanation:** For infrequent workloads, Consumption plan is most cost-effective (pay per execution). It can still scale quickly when needed. Premium plan would be expensive for infrequent use.

---

**Question 15:**
You are developing a function that needs to make an HTTP call to an external API, then write the result to a Cosmos DB container.

Complete the function signature using bindings:

```csharp
[FunctionName("SaveData")]
public static async Task<IActionResult> Run(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequest req,
    [_____] IAsyncCollector<Document> outputDocuments,
    ILogger log)
{
    // Function logic
}
```

A) CosmosDBInput
B) CosmosDB(databaseName: "mydb", collectionName: "mycollection", ConnectionStringSetting = "CosmosDBConnection")
C) Blob
D) Queue

**Answer: B** - CosmosDB binding with parameters

**Explanation:** Output bindings to Cosmos DB require specifying the database, collection, and connection string setting. IAsyncCollector allows adding multiple documents.

---

**Question 16:**
You have a function that needs to call another function to create a complex workflow. The workflow should continue even if the first function fails, and you need to track the overall workflow state.

What should you use?

A) Multiple HTTP-triggered functions
B) Durable Functions with orchestrator pattern
C) Azure Logic Apps
D) Function chaining with Queue triggers

**Answer: B** - Durable Functions with orchestrator pattern

**Explanation:** Durable Functions provide reliable workflow orchestration with state management, retry policies, and complex patterns. Perfect for multi-step workflows.

---

**Question 17:**
Your function receives messages from a Service Bus queue. Occasionally, message processing fails due to transient errors. You want messages to be retried up to 5 times before being moved to the dead-letter queue.

Where should you configure this?

A) In the function code using try-catch
B) In the host.json file
C) In the Service Bus queue properties
D) In the function.json binding configuration

**Answer: C** - In the Service Bus queue properties

**Explanation:** Max delivery count is configured on the Service Bus queue itself, not in function configuration. The queue handles retries and dead-lettering automatically.

---

## Section 2: Develop for Azure Storage (15-20%)

### Topic 2.1: Develop Solutions that Use Azure Cosmos DB

**Question 18:**
You are designing a Cosmos DB container for an e-commerce application that stores product reviews. Each review is associated with a product and a user. The application frequently queries reviews by productId.

What should you use as the partition key?

A) /id
B) /productId
C) /userId
D) /reviewDate

**Answer: B** - /productId

**Explanation:** Since queries are frequently filtered by productId, using it as the partition key enables efficient queries without cross-partition fanout. /id would create single-item partitions (not scalable). /userId would require cross-partition queries for product reviews.

---

**Question 19:**
Your application requires strong consistency when reading data that was just written, but you want to minimize latency for read operations in other scenarios.

Which consistency level should you use?

A) Strong
B) Bounded Staleness
C) Session
D) Eventual

**Answer: C** - Session

**Explanation:** Session consistency guarantees that reads within the same session see writes (strong for the writer), while reads from other sessions can be eventually consistent (lower latency). Strong would have higher latency for all reads. Eventual provides no guarantees.

---

**Question 20:**
You need to execute a transaction that creates an order and decrements inventory in Cosmos DB. Both operations must succeed or fail together.

What is the requirement for this transaction?

A) Both items must be in the same database
B) Both items must be in the same container
C) Both items must have the same partition key value
D) Use stored procedures across containers

**Answer: C** - Both items must have the same partition key value

**Explanation:** Cosmos DB transactions (including in stored procedures) are scoped to a single logical partition. Both documents must have the same partition key value.

---

**Question 21:**
Complete the code to query items from Cosmos DB using the SDK:

```csharp
Container container = cosmosClient.GetContainer("database", "orders");

var query = container.GetItemQueryIterator<Order>(
    "SELECT * FROM c WHERE c.status = @status AND c.total > @minTotal",
    requestOptions: new QueryRequestOptions 
    { 
        _____ = new PartitionKey("completed"),
        MaxItemCount = 100
    });
```

A) PartitionKeyValue
B) PartitionKey
C) PartitionKeyPath
D) Key

**Answer: B** - PartitionKey

**Explanation:** The property is `PartitionKey` in QueryRequestOptions. Specifying the partition key makes the query more efficient by targeting a specific partition.

---

**Question 22:**
You want to automatically delete items from a Cosmos DB container 30 days after they are created.

What should you configure?

A) Indexing policy with TTL
B) Time to Live (TTL) on the container
C) Change feed processor to delete old items
D) Azure Function with timer trigger

**Answer: B** - Time to Live (TTL) on the container

**Explanation:** TTL can be set at the container level (applies to all items) or item level. Setting TTL on items deletes them automatically after expiration. This is the most efficient solution.

---

**Question 23:**
Your application needs to respond in real-time to changes in a Cosmos DB container. You have deployed multiple instances of your application for high availability.

What should you implement?

A) Polling the container every second
B) Change feed with a single processor
C) Change feed processor with lease container
D) Triggers and stored procedures

**Answer: C** - Change feed processor with lease container

**Explanation:** Change feed processor uses a lease container to coordinate between multiple instances, preventing duplicate processing. Each instance can process different partitions.

---

### Topic 2.2: Develop Solutions that Use Azure Blob Storage

**Question 24:**
You are storing application logs in Blob Storage. Logs are frequently accessed for 7 days, occasionally accessed for 30 days, and rarely accessed after that. You want to minimize storage costs.

What should you implement?

A) Store all blobs in Archive tier
B) Create a lifecycle management policy
C) Manually move blobs between tiers
D) Use a separate storage account for old logs

**Answer: B** - Create a lifecycle management policy

**Explanation:** Lifecycle management policies can automatically transition blobs between access tiers based on age and access patterns. This automates cost optimization.

---

**Question 25:**
Complete the code to upload a blob with metadata:

```csharp
BlobClient blobClient = blobServiceClient
    .GetBlobContainerClient("documents")
    .GetBlobClient("file.pdf");

var metadata = new Dictionary<string, string>
{
    { "Author", "John Doe" },
    { "Department", "Sales" }
};

await blobClient.UploadAsync(stream, new _____
{
    Metadata = metadata,
    HttpHeaders = new BlobHttpHeaders 
    { 
        ContentType = "application/pdf" 
    }
});
```

A) BlobOptions
B) BlobUploadOptions
C) BlobRequestOptions
D) UploadOptions

**Answer: B** - BlobUploadOptions

**Explanation:** BlobUploadOptions is the parameter type for UploadAsync method that includes metadata, headers, conditions, and other upload options.

---

**Question 26:**
You need to generate a SAS token that allows a user to read a specific blob for the next 2 hours but not list other blobs in the container.

Complete the code:

```csharp
BlobSasBuilder sasBuilder = new BlobSasBuilder
{
    BlobContainerName = "documents",
    BlobName = "report.pdf",
    Resource = "_____",
    ExpiresOn = DateTimeOffset.UtcNow.AddHours(2)
};
sasBuilder.SetPermissions(BlobSasPermissions._____);
```

A) Resource = "b", Permissions = Read
B) Resource = "c", Permissions = Read | List
C) Resource = "blob", Permissions = Read
D) Resource = "b", Permissions = Read | List

**Answer: A** - Resource = "b", Permissions = Read

**Explanation:** Resource "b" specifies a blob (not container). Read permission allows reading the blob content but not listing. "c" would be container-level which would allow listing.

---

**Question 27:**
Your application processes large video files (2GB+) uploaded to Blob Storage. You want to optimize upload performance.

What should you do?

A) Upload the file in a single operation
B) Split file into blocks and upload in parallel
C) Use Page blobs instead of Block blobs
D) Enable archive tier during upload

**Answer: B** - Split file into blocks and upload in parallel

**Explanation:** For large files (>256MB), split into blocks (up to 4000 blocks, 100MB each) and upload in parallel for better performance. The SDK's UploadAsync does this automatically.

---

**Question 28:**
You need to ensure that blobs cannot be modified or deleted for 7 years to comply with regulatory requirements.

What feature should you enable?

A) Soft delete with 7-year retention
B) Blob versioning
C) Immutable storage with time-based retention policy
D) Lifecycle management with legal hold

**Answer: C** - Immutable storage with time-based retention policy

**Explanation:** Immutable storage (WORM - Write Once, Read Many) with time-based retention prevents modification/deletion for the specified period. This meets regulatory compliance needs.

---

## Section 3: Implement Azure Security (15-20%)

### Topic 3.1: Implement User Authentication and Authorization

**Question 29:**
You are building a web application that needs to authenticate users with Azure AD. After authentication, the app needs to call Microsoft Graph API on behalf of the signed-in user.

Which OAuth 2.0 flow should you use?

A) Client credentials flow
B) Authorization code flow
C) Device code flow
D) Implicit flow

**Answer: B** - Authorization code flow

**Explanation:** Authorization code flow is the standard OAuth 2.0 flow for web applications. It allows the app to get an access token to call APIs on behalf of the user. Client credentials is for service-to-service (no user).

---

**Question 30:**
Your daemon application (no user interaction) needs to read data from SharePoint Online using Microsoft Graph.

What should you configure?

A) Delegated permissions with user consent
B) Application permissions with admin consent
C) User-assigned managed identity
D) Service principal with interactive login

**Answer: B** - Application permissions with admin consent

**Explanation:** Daemon apps (no interactive user) require application permissions (not delegated). Admin consent is required for application permissions.

---

**Question 31:**
Complete the MSAL code to acquire a token silently with fallback to interactive:

```csharp
IPublicClientApplication app = PublicClientApplicationBuilder
    .Create(clientId)
    .WithAuthority(authority)
    .Build();

AuthenticationResult result;
try
{
    var accounts = await app.GetAccountsAsync();
    result = await app.AcquireTokenSilent(scopes, accounts.FirstOrDefault())
                      .ExecuteAsync();
}
catch (_____)
{
    result = await app.AcquireTokenInteractive(scopes)
                      .ExecuteAsync();
}
```

A) AuthenticationException
B) MsalUiRequiredException
C) UnauthorizedAccessException
D) MsalServiceException

**Answer: B** - MsalUiRequiredException

**Explanation:** MsalUiRequiredException is thrown when silent token acquisition fails (expired refresh token, no cached token). This indicates user interaction is needed.

---

**Question 32:**
You need to call Microsoft Graph API to read the signed-in user's profile and calendar events.

Which permissions should you request? (Choose two)

A) User.Read
B) User.ReadWrite
C) Calendars.Read
D) Calendars.ReadWrite
E) Directory.ReadWrite.All

**Answer: A, C** - User.Read and Calendars.Read

**Explanation:** User.Read allows reading the user's profile. Calendars.Read allows reading calendar events. ReadWrite permissions grant more access than needed (principle of least privilege).

---

**Question 33:**
Your application needs to generate a SAS token for a blob that allows a user to upload files for the next hour.

Complete the code:

```csharp
BlobSasBuilder sasBuilder = new BlobSasBuilder
{
    BlobContainerName = "uploads",
    Resource = "c",
    StartsOn = DateTimeOffset.UtcNow,
    ExpiresOn = DateTimeOffset.UtcNow.AddHours(1)
};
sasBuilder.SetPermissions(BlobContainerSasPermissions._____);
```

A) Read
B) Write
C) Write | Create
D) All

**Answer: B** - Write

**Explanation:** For uploads, Write permission is needed. Create is not a valid BlobContainerSasPermissions value (Write includes creation).

---

**Question 34:**
You are building a multi-tenant SaaS application. Users from different organizations should be able to sign in with their own Azure AD accounts.

What should you configure in the app registration?

A) Single tenant (your organization only)
B) Multitenant (any Azure AD directory)
C) Multitenant (any Azure AD directory and personal Microsoft accounts)
D) Personal Microsoft accounts only

**Answer: B** - Multitenant (any Azure AD directory)

**Explanation:** For SaaS applications where organizational users sign in with their company Azure AD, use multitenant without personal accounts.

---

### Topic 3.2: Implement Secure Azure Solutions

**Question 35:**
You are deploying a web application that needs database connection strings. The connection strings should be stored securely and accessible by the application.

What is the recommended approach?

A) Store in appsettings.json file
B) Store as App Service application settings
C) Store in Azure Key Vault and reference from App Service
D) Store encrypted in Azure Blob Storage

**Answer: C** - Store in Azure Key Vault and reference from App Service

**Explanation:** Key Vault provides secure storage with access logging and RBAC. App Service can reference secrets using @Microsoft.KeyVault() syntax. This is the Azure-recommended best practice.

---

**Question 36:**
Your App Service needs to retrieve secrets from Azure Key Vault. You want to use the most secure authentication method without managing credentials.

What should you enable?

A) Service principal with client secret
B) Service principal with certificate
C) System-assigned managed identity
D) Connection string authentication

**Answer: C** - System-assigned managed identity

**Explanation:** Managed identity provides passwordless authentication to Azure services. It's more secure than service principals (no credential management) and simpler to configure.

---

**Question 37:**
Complete the code to retrieve a secret from Key Vault using managed identity:

```csharp
var client = new SecretClient(
    new Uri("https://myvault.vault.azure.net/"),
    new _____());

KeyVaultSecret secret = await client.GetSecretAsync("DatabasePassword");
string password = secret.Value;
```

A) ClientSecretCredential(tenantId, clientId, clientSecret)
B) ManagedIdentityCredential()
C) DefaultAzureCredential()
D) AzureCliCredential()

**Answer: C** - DefaultAzureCredential()

**Explanation:** DefaultAzureCredential works in both Azure (uses managed identity) and local development (uses Visual Studio/Azure CLI credentials). It's the recommended approach for flexibility.

---

**Question 38:**
You want to use different configuration values for development, staging, and production environments. The configuration should support feature flags.

What should you use?

A) Multiple appsettings.json files
B) Azure App Configuration with labels
C) Environment variables only
D) Azure Key Vault with multiple vaults

**Answer: B** - Azure App Configuration with labels

**Explanation:** App Configuration supports labels for environment-specific configuration and feature flags. This provides centralized, dynamic configuration management.

---

**Question 39:**
You need to rotate a database password stored in Key Vault every 90 days. The application should get the latest password automatically.

What should you do?

A) Create a new secret version every 90 days; application uses SecretClient.GetSecretAsync()
B) Update the same secret value every 90 days
C) Create multiple secrets with different names
D) Use Azure Automation to update App Service settings

**Answer: A** - Create new secret version; application uses GetSecretAsync()

**Explanation:** Key Vault supports secret versioning. GetSecretAsync() without version always gets the latest version. This allows seamless rotation without application changes.

---

**Question 40:**
Your application uses Key Vault to store secrets. You want developers to be able to read secrets in development but not in production.

What's the best approach?

A) Use Key Vault access policies with different permissions per environment
B) Use separate Key Vaults for each environment
C) Store development secrets in code
D) Use Azure RBAC on the same Key Vault

**Answer: B** - Use separate Key Vaults for each environment

**Explanation:** Separate vaults per environment provides complete isolation and simpler access control. Developers get full access to dev vault, no access to production vault.

---

## Section 4: Monitor, Troubleshoot, and Optimize (5-10%)

### Topic 4.1: Monitor and Troubleshoot with Application Insights

**Question 41:**
You want to track custom business events in your application, such as "Order Placed" with order amount and product category.

What should you use?

A) TelemetryClient.TrackMetric()
B) TelemetryClient.TrackEvent()
C) TelemetryClient.TrackTrace()
D) ILogger.LogInformation()

**Answer: B** - TelemetryClient.TrackEvent()

**Explanation:** TrackEvent() is for custom business events with properties (event type, custom dimensions) and metrics (numeric values). TrackMetric is for standalone numeric values. TrackTrace is for diagnostic logging.

---

**Question 42:**
Your distributed application consists of a web frontend, API service, and background workers. You need to trace a single user request across all services.

What ensures correlation?

A) Shared application insights resource
B) Operation ID and correlation context
C) Custom event properties
D) Request ID in headers

**Answer: B** - Operation ID and correlation context

**Explanation:** Application Insights uses Operation ID to correlate telemetry across components. The SDK automatically propagates this through HTTP headers and creates the correlation chain.

---

**Question 43:**
Complete the KQL query to find all failed HTTP requests in the last 24 hours:

```kql
requests
| where timestamp > _____
| where _____ == false
| summarize count() by resultCode
```

A) ago(24h), success
B) now()-24h, failed
C) ago(1d), success
D) yesterday(), failed

**Answer: A** - ago(24h), success

**Explanation:** `ago(24h)` or `ago(1d)` calculates time relative to now. The `success` field is boolean (true/false). Checking `success == false` finds failures.

---

**Question 44:**
You want to be alerted when your application's average response time exceeds 2 seconds for 5 minutes.

What type of alert should you create?

A) Log alert with KQL query
B) Metric alert on server response time
C) Activity log alert
D) Smart detection alert

**Answer: B** - Metric alert on server response time

**Explanation:** Metric alerts are ideal for numeric thresholds like response time. They evaluate faster than log alerts and are designed for this scenario.

---

**Question 45:**
You need to test if your application's login page is accessible from multiple locations worldwide every 5 minutes.

What should you configure?

A) Live metrics stream
B) URL ping test
C) Multi-step web test
D) Availability set

**Answer: B** - URL ping test

**Explanation:** URL ping tests check HTTP endpoint availability from multiple Azure regions. They can run every 5 minutes (minimum interval). Multi-step tests require Visual Studio and are more complex.

---

**Question 46:**
Your application logs include sensitive user information. You want to filter this data before it's sent to Application Insights.

What should you implement?

A) Telemetry processor
B) Sampling
C) Log filtering in ILogger
D) KQL query filters

**Answer: A** - Telemetry processor

**Explanation:** Telemetry processors run in the pipeline before data is sent, allowing filtering or modification. This is the correct place to remove sensitive data. Sampling reduces volume but doesn't filter specific data.

---

## Section 5: Connect to and Consume Services (20-25%)

### Topic 5.1: Implement Azure API Management

**Question 47:**
You need to limit API calls to 100 requests per minute per subscription key.

Which policy should you use?

```xml
A)
<inbound>
    <rate-limit calls="100" renewal-period="60" />
</inbound>

B)
<inbound>
    <quota calls="100" renewal-period="60" />
</inbound>

C)
<inbound>
    <throttle calls="100" interval="60" />
</inbound>

D)
<inbound>
    <rate-limit-by-key calls="100" renewal-period="60" counter-key="@(context.Subscription.Id)" />
</inbound>
```

**Answer: A** - rate-limit with calls and renewal-period

**Explanation:** `rate-limit` policy limits calls per time period (renewal-period in seconds). Quota is for longer periods (daily, weekly). Option D would be for per-key limiting.

---

**Question 48:**
Your API returns user data including sensitive fields. You want to remove the "ssn" field from all responses.

Complete the policy:

```xml
<outbound>
    <set-body>@{
        var response = context.Response.Body.As<JObject>();
        response._____(\"ssn\");
        return response.ToString();
    }</set-body>
</outbound>
```

A) Delete
B) Remove
C) Exclude
D) Filter

**Answer: B** - Remove

**Explanation:** JObject.Remove() deletes a property from the JSON object. This is the correct method in C# for removing JSON properties.

---

**Question 49:**
You want to cache API responses for 60 seconds, but the cache should be different for each user.

What policy should you use?

```xml
<inbound>
    <cache-lookup vary-by-_____ />
</inbound>
<outbound>
    <cache-store duration="60" />
</outbound>
```

A) user
B) subscription
C) developer
D) header

**Answer: C** - developer

**Explanation:** `vary-by-developer` creates separate cache entries for each authenticated developer/user. This ensures each user gets their own cached data.

---

**Question 50:**
Your backend API URL is changing from v1 to v2. You want to rewrite incoming requests from /api/products to /api/v2/products.

Which policy should you use?

A) `<rewrite-uri template="/api/v2/products" />`
B) `<redirect-content-urls template="/api/v2/products" />`
C) `<set-backend-service base-url="/api/v2" />`
D) `<forward-request url="/api/v2/products" />`

**Answer: A** - rewrite-uri template

**Explanation:** `rewrite-uri` modifies the request URL path before forwarding to the backend. This is the correct policy for URL transformation.

---

### Topic 5.2: Develop Event-Based Solutions

**Question 51:**
You need to send custom events to an Event Grid topic when orders are placed in your application.

Complete the code:

```csharp
EventGridPublisherClient client = new EventGridPublisherClient(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey));

var events = new[] 
{
    new _____( 
        subject: "orders/12345",
        eventType: "OrderPlaced",
        dataVersion: "1.0",
        data: new { OrderId = "12345", Total = 99.99 })
};

await client.SendEventsAsync(events);
```

A) EventGridEvent
B) CloudEvent
C) Event
D) EventData

**Answer: A** - EventGridEvent

**Explanation:** EventGridEvent is the standard event format for Event Grid in Azure SDK. CloudEvent is also supported but EventGridEvent is more common in Azure.

---

**Question 52:**
You are creating an Event Grid subscription for blob created events. You only want events for .pdf files in the "documents" container.

Which filter should you apply?

A) Subject begins with `/blobServices/default/containers/documents/blobs/` AND ends with `.pdf`
B) Data field `contentType` equals `application/pdf`
C) Event type equals `Microsoft.Storage.BlobCreated` AND subject contains `.pdf`
D) Advanced filter on `data.url` contains `documents` AND `pdf`

**Answer: A** - Subject filter

**Explanation:** For blob events, the subject follows the pattern `/blobServices/default/containers/{container}/blobs/{blobname}`. Filtering on subject beginning and ending is the most efficient approach.

---

**Question 53:**
Your application sends telemetry data to Event Hubs. You need to ensure that events from the same device are always processed in order.

What should you use?

A) Event Grid topic
B) Event Hub with partition key set to device ID
C) Service Bus topic with sessions
D) Queue Storage

**Answer: B** - Event Hub with partition key

**Explanation:** Events with the same partition key are sent to the same partition, guaranteeing order within that partition. Using device ID ensures all events from one device are ordered.

---

**Question 54:**
You are consuming events from an Event Hub. You want to process events at your own pace and resume from where you left off after a restart.

What should you implement?

A) Event Hub Capture
B) Consumer group with checkpointing
C) Direct partition read
D) Shared access signature

**Answer: B** - Consumer group with checkpointing

**Explanation:** Checkpointing stores the last processed event offset in blob storage. This allows resuming from the last checkpoint after restart. Consumer groups allow multiple independent consumers.

---

### Topic 5.3: Develop Message-Based Solutions

**Question 55:**
You need guaranteed FIFO ordering for messages in Service Bus. Messages belong to different customer orders.

What should you configure?

A) Enable sessions on queue; set SessionId to Order ID
B) Use topics with subscriptions
C) Enable duplicate detection
D) Set message Priority property

**Answer: A** - Enable sessions with SessionId

**Explanation:** Service Bus sessions guarantee FIFO ordering for messages with the same SessionId. Setting SessionId to Order ID ensures all messages for an order are processed in order.

---

**Question 56:**
A message processing operation occasionally fails with transient errors. You want Service Bus to retry delivery automatically.

What happens by default?

A) Message is immediately dead-lettered
B) Message is retried up to MaxDeliveryCount
C) Message is deferred for manual retry
D) Message is deleted

**Answer: B** - Message is retried up to MaxDeliveryCount

**Explanation:** Service Bus automatically redelivers messages until MaxDeliveryCount is reached. After that, the message is moved to the dead-letter queue.

---

**Question 57:**
Complete the code to send a scheduled message to Service Bus queue:

```csharp
ServiceBusSender sender = client.CreateSender(queueName);

var message = new ServiceBusMessage("Process this later")
{
    _____ = DateTimeOffset.UtcNow.AddHours(1)
};

await sender.SendMessageAsync(message);
```

A) ScheduledEnqueueTime
B) ScheduledTime
C) DelayedSendTime
D) EnqueueTimeUtc

**Answer: A** - ScheduledEnqueueTime

**Explanation:** ScheduledEnqueueTime sets when the message becomes visible in the queue. This allows scheduling messages for future delivery.

---

**Question 58:**
You want to implement a publish-subscribe pattern where multiple subscribers receive the same messages, but each subscriber should only receive messages matching their filter criteria.

What should you use?

A) Service Bus queue with multiple receivers
B) Service Bus topic with subscription filters
C) Event Grid custom topic
D) Queue Storage with visibility timeout

**Answer: B** - Service Bus topic with subscription filters

**Explanation:** Topics support publish-subscribe with multiple subscriptions. Each subscription can have SQL filters to receive only matching messages.

---

**Question 59:**
Your application processes messages from Queue Storage. A message fails processing and is retried 5 times. What should you implement to handle poison messages?

A) Check message dequeue count; if > 5, move to a separate queue
B) Enable dead-letter queue
C) Increase visibility timeout
D) Use Service Bus instead

**Answer: A** - Check dequeue count

**Explanation:** Queue Storage doesn't have automatic dead-lettering. You must check DequeueCount and manually move poison messages to a separate queue or blob for investigation.

---

## Additional Scenario-Based Questions

### Complex Scenario 1: E-Commerce Application

**Question 60:**
You are architecting a cloud-native e-commerce platform with the following requirements:
- User authentication with social providers and corporate accounts
- Real-time inventory updates when purchases are made
- Product images stored with CDN delivery
- Background processing for email confirmations
- Application monitoring and alerting

What services should you use for each requirement?

A) Azure AD B2C, Event Grid, Blob Storage + CDN, Logic Apps, App Insights
B) Azure AD, Service Bus, Blob Storage, Azure Functions, Azure Monitor
C) Azure AD B2C, Cosmos DB change feed, Blob Storage + CDN, Azure Functions, Application Insights
D) Azure AD, Event Hubs, Azure Files, Web Jobs, Log Analytics

**Answer: C** - Azure AD B2C, Cosmos DB change feed, Blob Storage + CDN, Azure Functions, Application Insights

**Explanation:**
- Azure AD B2C: Supports social providers (Google, Facebook) and B2B federation
- Cosmos DB change feed: Real-time updates when data changes (better than polling)
- Blob Storage + CDN: Optimal for static content delivery globally
- Azure Functions: Event-driven background processing (serverless, cost-effective)
- Application Insights: Application-level monitoring with distributed tracing

---

### Complex Scenario 2: Document Processing Pipeline

**Question 61:**
Your company receives PDF documents via email. The workflow requires:
1. Extract text from PDFs
2. Analyze sentiment of content
3. Store results in database
4. Notify users of completion
5. Handle failures with retry logic

Design the solution using Azure services. Which combination is most appropriate?

A) Logic Apps → Cognitive Services → Cosmos DB → SendGrid → Built-in retry
B) Event Grid → Azure Functions → Cognitive Services → SQL Database → Service Bus
C) Queue Storage → Azure Functions → Cognitive Services → Cosmos DB → Event Grid
D) Service Bus → Azure Functions → Cognitive Services → Cosmos DB → Event Grid + Service Bus dead-letter

**Answer: D** - Service Bus → Azure Functions → Cognitive Services → Cosmos DB → Event Grid + Service Bus dead-letter

**Explanation:**
- Service Bus: Reliable messaging with dead-letter queue for failed messages
- Azure Functions: Serverless compute triggered by Service Bus messages
- Cognitive Services: Text extraction and sentiment analysis
- Cosmos DB: Globally distributed database for results
- Event Grid: Lightweight event notification for completion
- Service Bus dead-letter: Automatic handling of failures with retry policies

---

### Complex Scenario 3: Multi-Tenant SaaS Application

**Question 62:**
You are building a multi-tenant SaaS application where:
- Each tenant has their own Azure AD
- Application needs to access tenant's Microsoft Graph data
- Configuration per tenant (connection strings, feature flags)
- Centralized monitoring across all tenants
- Secrets managed securely

What's the recommended architecture?

```
A)
- App Registration: Multi-tenant
- Permissions: Delegated (Microsoft Graph)
- Configuration: App Configuration with labels per tenant
- Secrets: Key Vault per tenant
- Monitoring: Shared Application Insights with tenant ID dimension

B)
- App Registration: Single tenant per customer
- Permissions: Application (Microsoft Graph)
- Configuration: Separate appsettings per tenant
- Secrets: Environment variables
- Monitoring: Separate Application Insights per tenant

C)
- App Registration: Multi-tenant
- Permissions: Application (Microsoft Graph)
- Configuration: App Configuration with labels per tenant
- Secrets: Single Key Vault with tenant-prefixed secrets
- Monitoring: Shared Application Insights with tenant ID dimension

D)
- App Registration: Multi-tenant
- Permissions: Delegated (Microsoft Graph) with admin consent
- Configuration: Cosmos DB with tenant configuration documents
- Secrets: Key Vault with RBAC per tenant
- Monitoring: Shared Application Insights with tenant ID dimension
```

**Answer: A** - Multi-tenant app with delegated permissions, App Configuration, Key Vault per tenant, shared monitoring

**Explanation:**
- Multi-tenant app registration: Single app works for all customer tenants
- Delegated permissions: Acts on behalf of the user (more secure than app permissions)
- App Configuration with labels: Centralized config with tenant-specific values
- Key Vault per tenant: Isolation of sensitive data between tenants
- Shared Application Insights with dimensions: Cost-effective monitoring with tenant segmentation

---

## Study Tips for Practice Questions

1. **Don't Memorize Answers**: Focus on understanding why each answer is correct
2. **Hands-On Verification**: Try implementing solutions you're unsure about
3. **Eliminate Obviously Wrong**: Process of elimination improves odds
4. **Watch for Tricks**: "EXCEPT", "NOT", "LEAST" change the question
5. **Time Yourself**: Practice under exam conditions
6. **Review Incorrect Answers**: Understand the gap in knowledge
7. **Create Flashcards**: For services, use cases, and limitations
8. **Teach Someone**: Explaining concepts solidifies understanding

---

## Question Analysis Framework

For each question you get wrong:

1. **Topic**: Which exam objective does this cover?
2. **Concept**: What specific concept did I miss?
3. **Why Wrong**: Why was my answer incorrect?
4. **Why Right**: Why is the correct answer better?
5. **How to Remember**: Create a mnemonic or analogy
6. **Related Topics**: What else should I review?
7. **Hands-On**: What lab would reinforce this?

---

## Common Question Types and Strategies

### Code Completion Questions
- Read the surrounding code carefully
- Understand the intent (what is it trying to do?)
- Eliminate syntactically incorrect options
- Choose the option that matches Azure SDK patterns

### Scenario-Based Questions
- Identify the key requirements (security, cost, performance, scalability)
- Eliminate options that don't meet a requirement
- Choose the simplest solution that meets all requirements
- Prefer Azure-native solutions over custom code

### Troubleshooting Questions
- Understand the symptoms described
- Think about what could cause those symptoms
- Consider where in the flow the problem occurs
- Choose the diagnostic approach that targets the root cause

### Best Practices Questions
- Think about security first
- Consider cost optimization
- Prefer managed services over custom solutions
- Follow the principle of least privilege

---

*This practice question set covers approximately 30% of the topics. For comprehensive preparation, use multiple sources including Microsoft Learn modules, practice exams from MeasureUp or Whizlabs, and hands-on labs.*

*Good luck with your AZ-204 preparation!*
