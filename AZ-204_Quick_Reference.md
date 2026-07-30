# AZ-204 Quick Reference Guide
## Commands, Code Snippets, and Decision Trees

---

## Table of Contents
1. [Azure CLI Commands](#azure-cli-commands)
2. [SDK Code Snippets](#sdk-code-snippets)
3. [Service Decision Trees](#service-decision-trees)
4. [Configuration Examples](#configuration-examples)
5. [Common Patterns](#common-patterns)
6. [Troubleshooting Commands](#troubleshooting-commands)

---

## Azure CLI Commands

### General Commands
```bash
# Login and set subscription
az login
az account list --output table
az account set --subscription "subscription-name-or-id"
az account show

# Resource Groups
az group create --name myResourceGroup --location eastus
az group list --output table
az group delete --name myResourceGroup --yes --no-wait
```

### Container Registry (ACR)
```bash
# Create ACR
az acr create --resource-group myRG --name myACR --sku Basic
az acr create --resource-group myRG --name myACR --sku Premium

# Login to ACR
az acr login --name myACR
docker login myacr.azurecr.io

# Build and push image (no local Docker required)
az acr build --registry myACR --image myapp:v1 .
az acr build --registry myACR --image myapp:v1 --file Dockerfile .

# List images
az acr repository list --name myACR --output table
az acr repository show-tags --name myACR --repository myapp --output table

# Enable admin account (for testing only)
az acr update --name myACR --admin-enabled true
az acr credential show --name myACR
```

### Container Instances (ACI)
```bash
# Create container instance
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myacr.azurecr.io/myapp:v1 \
  --registry-login-server myacr.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --dns-name-label myapp-dns \
  --ports 80

# Create with environment variables
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myimage \
  --environment-variables 'KEY1'='VALUE1' 'KEY2'='VALUE2' \
  --secure-environment-variables 'SECRET'='SecretValue'

# Create with Azure Files mount
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myimage \
  --azure-file-volume-account-name mystorageacct \
  --azure-file-volume-account-key <storage-key> \
  --azure-file-volume-share-name myshare \
  --azure-file-volume-mount-path /mnt/data

# Restart policies
az container create --restart-policy Always    # Default
az container create --restart-policy OnFailure # Retry on failure
az container create --restart-policy Never     # One-time jobs

# View logs and exec into container
az container logs --resource-group myRG --name mycontainer
az container attach --resource-group myRG --name mycontainer
az container exec --resource-group myRG --name mycontainer --exec-command "/bin/bash"

# Delete container
az container delete --resource-group myRG --name mycontainer --yes
```

### App Service
```bash
# Create App Service Plan
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myRG \
  --sku B1 \
  --is-linux

# Available SKUs: F1 (Free), D1 (Shared), B1/B2/B3 (Basic), S1/S2/S3 (Standard), P1v2/P2v2/P3v2 (Premium)

# Create Web App
az webapp create \
  --resource-group myRG \
  --plan myAppServicePlan \
  --name myWebApp \
  --runtime "NODE:18-lts"

# Deploy from local Git
az webapp deployment source config-local-git \
  --name myWebApp \
  --resource-group myRG

# Deploy from GitHub
az webapp deployment source config \
  --name myWebApp \
  --resource-group myRG \
  --repo-url https://github.com/user/repo \
  --branch main \
  --manual-integration

# Configure app settings
az webapp config appsettings set \
  --resource-group myRG \
  --name myWebApp \
  --settings SETTING1=value1 SETTING2=value2

# Set app setting as slot-specific
az webapp config appsettings set \
  --resource-group myRG \
  --name myWebApp \
  --slot-settings SETTING1=value1

# Configure connection strings
az webapp config connection-string set \
  --resource-group myRG \
  --name myWebApp \
  --connection-string-type SQLAzure \
  --settings DefaultConnection='Server=...'

# Enable logging
az webapp log config \
  --name myWebApp \
  --resource-group myRG \
  --application-logging filesystem \
  --level information \
  --web-server-logging filesystem

# Stream logs
az webapp log tail --name myWebApp --resource-group myRG

# Deployment slots
az webapp deployment slot create \
  --name myWebApp \
  --resource-group myRG \
  --slot staging

az webapp deployment slot swap \
  --name myWebApp \
  --resource-group myRG \
  --slot staging \
  --target-slot production

# Configure autoscaling
az monitor autoscale create \
  --resource-group myRG \
  --resource myAppServicePlan \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-settings \
  --min-count 1 \
  --max-count 5 \
  --count 2

az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name autoscale-settings \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1

az monitor autoscale rule create \
  --resource-group myRG \
  --autoscale-name autoscale-settings \
  --condition "Percentage CPU < 30 avg 5m" \
  --scale in 1

# Custom domain and SSL
az webapp config hostname add \
  --webapp-name myWebApp \
  --resource-group myRG \
  --hostname www.example.com

az webapp config ssl bind \
  --name myWebApp \
  --resource-group myRG \
  --certificate-thumbprint <thumbprint> \
  --ssl-type SNI
```

### Azure Functions
```bash
# Create Function App (Consumption plan)
az functionapp create \
  --resource-group myRG \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 18 \
  --functions-version 4 \
  --name myFunctionApp \
  --storage-account mystorageacct

# Create Function App (Premium plan)
az functionapp plan create \
  --resource-group myRG \
  --name myPremiumPlan \
  --location eastus \
  --sku EP1

az functionapp create \
  --resource-group myRG \
  --name myFunctionApp \
  --plan myPremiumPlan \
  --storage-account mystorageacct \
  --runtime node

# Configure app settings
az functionapp config appsettings set \
  --name myFunctionApp \
  --resource-group myRG \
  --settings "KEY=VALUE" "COSMOS_CONNECTION=@Microsoft.KeyVault(...)"

# Enable Application Insights
az functionapp config appsettings set \
  --name myFunctionApp \
  --resource-group myRG \
  --settings "APPINSIGHTS_INSTRUMENTATIONKEY=<key>"

# Deploy from local directory
func azure functionapp publish myFunctionApp

# Stream logs
az functionapp log tail --name myFunctionApp --resource-group myRG
```

### Storage Account
```bash
# Create storage account
az storage account create \
  --name mystorageacct \
  --resource-group myRG \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Get connection string
az storage account show-connection-string \
  --name mystorageacct \
  --resource-group myRG

# Get account keys
az storage account keys list \
  --account-name mystorageacct \
  --resource-group myRG

# Blob containers
az storage container create \
  --name mycontainer \
  --account-name mystorageacct \
  --public-access blob

az storage blob upload \
  --account-name mystorageacct \
  --container-name mycontainer \
  --name myblob.txt \
  --file ./local-file.txt

az storage blob list \
  --account-name mystorageacct \
  --container-name mycontainer \
  --output table

# Generate SAS token
az storage blob generate-sas \
  --account-name mystorageacct \
  --container-name mycontainer \
  --name myblob.txt \
  --permissions r \
  --expiry 2024-12-31T23:59Z

# Lifecycle management
az storage account management-policy create \
  --account-name mystorageacct \
  --policy @policy.json
```

### Cosmos DB
```bash
# Create Cosmos DB account
az cosmosdb create \
  --name mycosmosacct \
  --resource-group myRG \
  --default-consistency-level Session \
  --locations regionName=eastus failoverPriority=0 isZoneRedundant=False

# Create database
az cosmosdb sql database create \
  --account-name mycosmosacct \
  --name mydb \
  --resource-group myRG

# Create container
az cosmosdb sql container create \
  --account-name mycosmosacct \
  --database-name mydb \
  --name mycontainer \
  --partition-key-path /category \
  --throughput 400 \
  --resource-group myRG

# List connection strings
az cosmosdb keys list \
  --name mycosmosacct \
  --resource-group myRG \
  --type connection-strings

# Update throughput
az cosmosdb sql container throughput update \
  --account-name mycosmosacct \
  --database-name mydb \
  --name mycontainer \
  --throughput 1000 \
  --resource-group myRG
```

### Key Vault
```bash
# Create Key Vault
az keyvault create \
  --name mykeyvault \
  --resource-group myRG \
  --location eastus

# Set secret
az keyvault secret set \
  --vault-name mykeyvault \
  --name DatabasePassword \
  --value "SuperSecret123"

# Get secret
az keyvault secret show \
  --vault-name mykeyvault \
  --name DatabasePassword \
  --query value -o tsv

# List secrets
az keyvault secret list \
  --vault-name mykeyvault \
  --output table

# Grant access to managed identity
az keyvault set-policy \
  --name mykeyvault \
  --object-id <managed-identity-principal-id> \
  --secret-permissions get list

# Enable soft-delete and purge protection
az keyvault update \
  --name mykeyvault \
  --enable-soft-delete true \
  --enable-purge-protection true

# Create key
az keyvault key create \
  --vault-name mykeyvault \
  --name mykey \
  --protection software
```

### Service Bus
```bash
# Create namespace
az servicebus namespace create \
  --resource-group myRG \
  --name mysbnamespace \
  --location eastus \
  --sku Standard

# Create queue
az servicebus queue create \
  --resource-group myRG \
  --namespace-name mysbnamespace \
  --name myqueue \
  --max-size 1024 \
  --default-message-time-to-live P14D \
  --enable-dead-lettering-on-message-expiration true \
  --max-delivery-count 10

# Create topic
az servicebus topic create \
  --resource-group myRG \
  --namespace-name mysbnamespace \
  --name mytopic

# Create subscription
az servicebus topic subscription create \
  --resource-group myRG \
  --namespace-name mysbnamespace \
  --topic-name mytopic \
  --name mysubscription

# Create subscription with filter
az servicebus topic subscription rule create \
  --resource-group myRG \
  --namespace-name mysbnamespace \
  --topic-name mytopic \
  --subscription-name mysubscription \
  --name myrule \
  --filter-sql-expression "Priority = 'High'"

# Get connection string
az servicebus namespace authorization-rule keys list \
  --resource-group myRG \
  --namespace-name mysbnamespace \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv
```

### Event Hubs
```bash
# Create namespace
az eventhubs namespace create \
  --resource-group myRG \
  --name myehnamespace \
  --location eastus \
  --sku Standard \
  --capacity 1

# Create Event Hub
az eventhubs eventhub create \
  --resource-group myRG \
  --namespace-name myehnamespace \
  --name myeventhub \
  --partition-count 4 \
  --message-retention 7

# Create consumer group
az eventhubs eventhub consumer-group create \
  --resource-group myRG \
  --namespace-name myehnamespace \
  --eventhub-name myeventhub \
  --name myconsumergroup

# Get connection string
az eventhubs namespace authorization-rule keys list \
  --resource-group myRG \
  --namespace-name myehnamespace \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv
```

### Event Grid
```bash
# Create custom topic
az eventgrid topic create \
  --resource-group myRG \
  --name mytopic \
  --location eastus

# Create event subscription (to Azure Function)
az eventgrid event-subscription create \
  --source-resource-id /subscriptions/.../resourceGroups/myRG/providers/Microsoft.EventGrid/topics/mytopic \
  --name mysubscription \
  --endpoint-type azurefunction \
  --endpoint /subscriptions/.../resourceGroups/myRG/providers/Microsoft.Web/sites/myfunctionapp/functions/EventGridTrigger

# Create subscription with filter
az eventgrid event-subscription create \
  --source-resource-id /subscriptions/.../mytopic \
  --name filteredsubscription \
  --endpoint <endpoint-url> \
  --included-event-types "OrderPlaced" "OrderShipped" \
  --subject-begins-with "/orders/high-priority"
```

### Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --app myappinsights \
  --location eastus \
  --resource-group myRG \
  --application-type web

# Get instrumentation key
az monitor app-insights component show \
  --app myappinsights \
  --resource-group myRG \
  --query instrumentationKey -o tsv

# Get connection string
az monitor app-insights component show \
  --app myappinsights \
  --resource-group myRG \
  --query connectionString -o tsv

# Query logs
az monitor app-insights query \
  --app myappinsights \
  --resource-group myRG \
  --analytics-query "requests | where timestamp > ago(1h) | summarize count() by resultCode" \
  --offset 1h
```

---

## SDK Code Snippets

### C# - Azure Blob Storage
```csharp
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Azure.Storage.Blobs.Specialized;

// Create client
BlobServiceClient blobServiceClient = new BlobServiceClient(connectionString);
BlobContainerClient containerClient = blobServiceClient.GetBlobContainerClient("mycontainer");
await containerClient.CreateIfNotExistsAsync();

// Upload blob
BlobClient blobClient = containerClient.GetBlobClient("myblob.txt");
await blobClient.UploadAsync(stream, overwrite: true);

// Upload with options
await blobClient.UploadAsync(stream, new BlobUploadOptions
{
    HttpHeaders = new BlobHttpHeaders
    {
        ContentType = "application/pdf",
        CacheControl = "max-age=3600"
    },
    Metadata = new Dictionary<string, string>
    {
        { "Author", "John Doe" },
        { "Department", "Sales" }
    },
    AccessTier = AccessTier.Cool
});

// Download blob
BlobDownloadInfo download = await blobClient.DownloadAsync();
using (var streamReader = new StreamReader(download.Content))
{
    string content = await streamReader.ReadToEndAsync();
}

// List blobs
await foreach (BlobItem blobItem in containerClient.GetBlobsAsync())
{
    Console.WriteLine($"Blob: {blobItem.Name}, Size: {blobItem.Properties.ContentLength}");
}

// Generate SAS token
BlobSasBuilder sasBuilder = new BlobSasBuilder
{
    BlobContainerName = containerClient.Name,
    BlobName = blobClient.Name,
    Resource = "b",
    StartsOn = DateTimeOffset.UtcNow,
    ExpiresOn = DateTimeOffset.UtcNow.AddHours(1)
};
sasBuilder.SetPermissions(BlobSasPermissions.Read);

Uri sasUri = blobClient.GenerateSasUri(sasBuilder);

// Set metadata
var metadata = new Dictionary<string, string>
{
    { "DocumentType", "Invoice" },
    { "Year", "2024" }
};
await blobClient.SetMetadataAsync(metadata);

// Get properties
BlobProperties properties = await blobClient.GetPropertiesAsync();
Console.WriteLine($"Content-Type: {properties.ContentType}");
Console.WriteLine($"Last Modified: {properties.LastModified}");
```

### C# - Azure Cosmos DB
```csharp
using Microsoft.Azure.Cosmos;

// Create client
CosmosClient cosmosClient = new CosmosClient(endpoint, key);

// Create database and container
Database database = await cosmosClient.CreateDatabaseIfNotExistsAsync("mydb");
Container container = await database.CreateContainerIfNotExistsAsync(
    "mycontainer", 
    "/partitionKey", 
    throughput: 400);

// Create item
var item = new
{
    id = Guid.NewGuid().ToString(),
    partitionKey = "category1",
    name = "Product 1",
    price = 29.99
};

ItemResponse<dynamic> response = await container.CreateItemAsync(
    item, 
    new PartitionKey("category1"));

// Read item
ItemResponse<dynamic> readResponse = await container.ReadItemAsync<dynamic>(
    item.id, 
    new PartitionKey("category1"));

// Update item
item.price = 34.99;
ItemResponse<dynamic> updateResponse = await container.ReplaceItemAsync(
    item, 
    item.id, 
    new PartitionKey("category1"));

// Delete item
await container.DeleteItemAsync<dynamic>(
    item.id, 
    new PartitionKey("category1"));

// Query items
var query = new QueryDefinition(
    "SELECT * FROM c WHERE c.price > @minPrice AND c.partitionKey = @category")
    .WithParameter("@minPrice", 20)
    .WithParameter("@category", "category1");

var iterator = container.GetItemQueryIterator<dynamic>(
    query, 
    requestOptions: new QueryRequestOptions 
    { 
        PartitionKey = new PartitionKey("category1")
    });

while (iterator.HasMoreResults)
{
    FeedResponse<dynamic> resultSet = await iterator.ReadNextAsync();
    foreach (var doc in resultSet)
    {
        Console.WriteLine(doc);
    }
}

// Batch operations (same partition key)
TransactionalBatch batch = container.CreateTransactionalBatch(
    new PartitionKey("category1"));

batch.CreateItem(item1);
batch.ReplaceItem(item2.id, item2);
batch.DeleteItem(item3.id);

TransactionalBatchResponse batchResponse = await batch.ExecuteAsync();

// Change feed processor
Container leaseContainer = database.GetContainer("leases");

ChangeFeedProcessor processor = container
    .GetChangeFeedProcessorBuilder<dynamic>("processorName", HandleChangesAsync)
    .WithInstanceName("instance1")
    .WithLeaseContainer(leaseContainer)
    .WithStartTime(DateTime.UtcNow.AddHours(-1))
    .Build();

async Task HandleChangesAsync(
    ChangeFeedProcessorContext context,
    IReadOnlyCollection<dynamic> changes,
    CancellationToken cancellationToken)
{
    foreach (var document in changes)
    {
        Console.WriteLine($"Change detected: {document.id}");
    }
}

await processor.StartAsync();
```

### C# - Azure Service Bus
```csharp
using Azure.Messaging.ServiceBus;

// Create client
await using var client = new ServiceBusClient(connectionString);

// Send message to queue
ServiceBusSender sender = client.CreateSender("myqueue");

var message = new ServiceBusMessage("Hello, Service Bus!")
{
    ContentType = "application/json",
    Subject = "Order Processing",
    MessageId = Guid.NewGuid().ToString(),
    TimeToLive = TimeSpan.FromMinutes(5),
    ScheduledEnqueueTime = DateTimeOffset.UtcNow.AddMinutes(10)
};

message.ApplicationProperties.Add("Priority", "High");
message.ApplicationProperties.Add("OrderId", "12345");

await sender.SendMessageAsync(message);

// Send batch of messages
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

// Receive messages
ServiceBusReceiver receiver = client.CreateReceiver("myqueue");

ServiceBusReceivedMessage message = await receiver.ReceiveMessageAsync(
    TimeSpan.FromSeconds(30));

if (message != null)
{
    try
    {
        // Process message
        Console.WriteLine($"Body: {message.Body}");
        Console.WriteLine($"Priority: {message.ApplicationProperties["Priority"]}");
        
        // Complete the message
        await receiver.CompleteMessageAsync(message);
    }
    catch (Exception ex)
    {
        // Abandon message (back to queue)
        await receiver.AbandonMessageAsync(message);
        
        // Or dead-letter the message
        await receiver.DeadLetterMessageAsync(message,
            deadLetterReason: "ProcessingError",
            deadLetterErrorDescription: ex.Message);
    }
}

// Peek messages (without removing from queue)
ServiceBusReceivedMessage peekedMessage = await receiver.PeekMessageAsync();

// Session-based processing (FIFO)
ServiceBusSessionReceiver sessionReceiver = await client.AcceptNextSessionAsync("myqueue");
Console.WriteLine($"Session ID: {sessionReceiver.SessionId}");

while (true)
{
    var sessionMessage = await sessionReceiver.ReceiveMessageAsync(TimeSpan.FromSeconds(5));
    if (sessionMessage == null) break;
    
    await sessionReceiver.CompleteMessageAsync(sessionMessage);
}
```

### C# - Azure Event Hubs
```csharp
using Azure.Messaging.EventHubs;
using Azure.Messaging.EventHubs.Producer;
using Azure.Messaging.EventHubs.Consumer;
using Azure.Messaging.EventHubs.Processor;

// Produce events
await using var producer = new EventHubProducerClient(connectionString, eventHubName);

// Send single event
EventData eventData = new EventData(Encoding.UTF8.GetBytes("Event data"));
eventData.Properties.Add("EventType", "OrderPlaced");
await producer.SendAsync(new[] { eventData });

// Send batch with partition key
var eventBatch = await producer.CreateBatchAsync(new CreateBatchOptions
{
    PartitionKey = "device-001"
});

for (int i = 0; i < 10; i++)
{
    var eventData = new EventData($"Event {i}");
    if (!eventBatch.TryAdd(eventData))
    {
        await producer.SendAsync(eventBatch);
        eventBatch = await producer.CreateBatchAsync(new CreateBatchOptions
        {
            PartitionKey = "device-001"
        });
        eventBatch.TryAdd(eventData);
    }
}
await producer.SendAsync(eventBatch);

// Consume events with Event Processor
var storageClient = new BlobContainerClient(storageConnectionString, "checkpoints");
var processor = new EventProcessorClient(
    storageClient,
    EventHubConsumerClient.DefaultConsumerGroupName,
    connectionString,
    eventHubName);

processor.ProcessEventAsync += async (args) =>
{
    string data = Encoding.UTF8.GetString(args.Data.Body.ToArray());
    Console.WriteLine($"Partition: {args.Partition.PartitionId}, Data: {data}");
    
    // Update checkpoint
    await args.UpdateCheckpointAsync();
};

processor.ProcessErrorAsync += (args) =>
{
    Console.WriteLine($"Error: {args.Exception.Message}");
    return Task.CompletedTask;
};

await processor.StartProcessingAsync();
await Task.Delay(TimeSpan.FromMinutes(1));
await processor.StopProcessingAsync();
```

### C# - Azure Event Grid
```csharp
using Azure.Messaging.EventGrid;

// Publish events to custom topic
EventGridPublisherClient client = new EventGridPublisherClient(
    new Uri(topicEndpoint),
    new AzureKeyCredential(topicKey));

// Event Grid schema
var events = new List<EventGridEvent>
{
    new EventGridEvent(
        subject: "orders/12345",
        eventType: "OrderPlaced",
        dataVersion: "1.0",
        data: new 
        { 
            OrderId = "12345", 
            Total = 99.99,
            CustomerId = "C001"
        })
};

await client.SendEventsAsync(events);

// CloudEvents schema
var cloudEvents = new List<CloudEvent>
{
    new CloudEvent(
        source: "/orders",
        type: "OrderPlaced",
        jsonSerializableData: new { OrderId = "12345", Total = 99.99 })
    {
        Subject = "orders/12345",
        Id = Guid.NewGuid().ToString()
    }
};

await client.SendEventsAsync(cloudEvents);

// Handle Event Grid events in Azure Function
[FunctionName("HandleOrderEvent")]
public static async Task Run(
    [EventGridTrigger] EventGridEvent eventGridEvent,
    ILogger log)
{
    log.LogInformation($"Event type: {eventGridEvent.EventType}");
    log.LogInformation($"Subject: {eventGridEvent.Subject}");
    log.LogInformation($"Data: {eventGridEvent.Data}");
    
    // Parse event data
    var orderData = eventGridEvent.Data.ToObjectFromJson<OrderData>();
    log.LogInformation($"Order ID: {orderData.OrderId}");
}
```

### C# - Azure Key Vault
```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

// Create client with managed identity (or DefaultAzureCredential)
var client = new SecretClient(
    new Uri($"https://{vaultName}.vault.azure.net/"),
    new DefaultAzureCredential());

// Set secret
await client.SetSecretAsync("DatabasePassword", "SuperSecret123");

// Set secret with expiration
await client.SetSecretAsync(new KeyVaultSecret("ApiKey", "key123")
{
    Properties = 
    {
        ExpiresOn = DateTimeOffset.UtcNow.AddMonths(6),
        ContentType = "text/plain",
        Tags = 
        {
            ["Environment"] = "Production",
            ["CreatedBy"] = "Admin"
        }
    }
});

// Get secret (latest version)
KeyVaultSecret secret = await client.GetSecretAsync("DatabasePassword");
string password = secret.Value;

// Get specific version
KeyVaultSecret versionedSecret = await client.GetSecretAsync("DatabasePassword", "version-id");

// Update secret properties
SecretProperties properties = secret.Properties;
properties.Enabled = false;
await client.UpdateSecretPropertiesAsync(properties);

// List secrets
await foreach (SecretProperties secretProperty in client.GetPropertiesOfSecretsAsync())
{
    Console.WriteLine($"Name: {secretProperty.Name}");
}

// Delete and recover secret
DeleteSecretOperation operation = await client.StartDeleteSecretAsync("DatabasePassword");
await operation.WaitForCompletionAsync();

await client.RecoverDeletedSecretAsync("DatabasePassword");
```

### C# - Microsoft Identity Platform (MSAL)
```csharp
using Microsoft.Identity.Client;

// Public client (desktop/mobile apps)
IPublicClientApplication publicApp = PublicClientApplicationBuilder
    .Create(clientId)
    .WithAuthority(AzureCloudInstance.AzurePublic, tenantId)
    .WithRedirectUri("http://localhost")
    .Build();

// Acquire token interactively
string[] scopes = { "User.Read", "Calendars.Read" };
AuthenticationResult result = await publicApp
    .AcquireTokenInteractive(scopes)
    .WithPrompt(Prompt.SelectAccount)
    .ExecuteAsync();

// Acquire token silently (from cache)
var accounts = await publicApp.GetAccountsAsync();
AuthenticationResult silentResult = await publicApp
    .AcquireTokenSilent(scopes, accounts.FirstOrDefault())
    .ExecuteAsync();

// Confidential client (web apps/APIs)
IConfidentialClientApplication confidentialApp = ConfidentialClientApplicationBuilder
    .Create(clientId)
    .WithClientSecret(clientSecret)
    .WithAuthority(new Uri($"https://login.microsoftonline.com/{tenantId}"))
    .Build();

// Client credentials flow (service-to-service)
string[] appScopes = { "https://graph.microsoft.com/.default" };
AuthenticationResult tokenResult = await confidentialApp
    .AcquireTokenForClient(appScopes)
    .ExecuteAsync();

// Authorization code flow (web apps)
AuthenticationResult authResult = await confidentialApp
    .AcquireTokenByAuthorizationCode(scopes, authorizationCode)
    .ExecuteAsync();
```

### C# - Microsoft Graph API
```csharp
using Microsoft.Graph;
using Azure.Identity;

// Create Graph client
var graphClient = new GraphServiceClient(
    new DefaultAzureCredential(),
    new[] { "https://graph.microsoft.com/.default" });

// Get current user
var me = await graphClient.Me.GetAsync();
Console.WriteLine($"Name: {me.DisplayName}, Email: {me.Mail}");

// Get user's calendar events
var events = await graphClient.Me.Events
    .GetAsync(requestConfiguration =>
    {
        requestConfiguration.QueryParameters.Top = 10;
        requestConfiguration.QueryParameters.Select = new[] { "subject", "start", "end" };
        requestConfiguration.QueryParameters.Orderby = new[] { "start/dateTime" };
    });

foreach (var evt in events.Value)
{
    Console.WriteLine($"{evt.Subject} - {evt.Start.DateTime}");
}

// Send email
var message = new Microsoft.Graph.Models.Message
{
    Subject = "Test Email",
    Body = new ItemBody
    {
        ContentType = BodyType.Html,
        Content = "<h1>Hello</h1><p>This is a test email.</p>"
    },
    ToRecipients = new List<Recipient>
    {
        new Recipient
        {
            EmailAddress = new EmailAddress
            {
                Address = "user@example.com"
            }
        }
    }
};

await graphClient.Me.SendMail.PostAsync(new SendMailPostRequestBody
{
    Message = message
});

// List users (requires app permissions)
var users = await graphClient.Users
    .GetAsync(requestConfiguration =>
    {
        requestConfiguration.QueryParameters.Top = 10;
        requestConfiguration.QueryParameters.Filter = "startsWith(displayName, 'John')";
    });
```

### C# - Application Insights
```csharp
using Microsoft.ApplicationInsights;
using Microsoft.ApplicationInsights.DataContracts;

// Initialize TelemetryClient
var telemetryClient = new TelemetryClient();

// Track custom event
telemetryClient.TrackEvent("OrderPlaced",
    properties: new Dictionary<string, string>
    {
        { "ProductId", "P123" },
        { "UserId", "U456" },
        { "Category", "Electronics" }
    },
    metrics: new Dictionary<string, double>
    {
        { "OrderValue", 299.99 },
        { "ItemCount", 3 }
    });

// Track metric
telemetryClient.TrackMetric("QueueLength", queue.Count);
telemetryClient.TrackMetric(new MetricTelemetry
{
    Name = "ResponseTime",
    Sum = responseTime.TotalMilliseconds,
    Count = 1,
    Properties = { ["Controller"] = "Orders" }
});

// Track dependency
var startTime = DateTime.UtcNow;
var timer = Stopwatch.StartNew();
try
{
    var response = await httpClient.GetAsync(url);
    telemetryClient.TrackDependency(
        dependencyTypeName: "HTTP",
        target: url,
        dependencyName: "GET",
        data: url,
        startTime: startTime,
        duration: timer.Elapsed,
        resultCode: response.StatusCode.ToString(),
        success: response.IsSuccessStatusCode);
}
catch (Exception ex)
{
    telemetryClient.TrackDependency("HTTP", url, "GET", url, 
        startTime, timer.Elapsed, "Error", false);
    telemetryClient.TrackException(ex);
}

// Track exception
try
{
    // Code that might throw
}
catch (Exception ex)
{
    telemetryClient.TrackException(ex,
        properties: new Dictionary<string, string>
        {
            { "OrderId", orderId },
            { "Operation", "ProcessPayment" }
        });
}

// Track request (usually done automatically)
var requestTelemetry = new RequestTelemetry
{
    Name = "GET /api/orders",
    Timestamp = DateTimeOffset.UtcNow,
    Duration = TimeSpan.FromMilliseconds(120),
    ResponseCode = "200",
    Success = true
};
telemetryClient.TrackRequest(requestTelemetry);

// Flush before app exits
telemetryClient.Flush();
await Task.Delay(5000); // Allow time to send
```

---

## Service Decision Trees

### When to Use Which Compute Service?

```
Do you need containerized applications?
├─ Yes
│  ├─ Need Kubernetes orchestration? → AKS
│  ├─ Simple container execution? → ACI
│  └─ Managed container apps with auto-scaling? → Container Apps
└─ No
   ├─ Event-driven, short-running code? → Azure Functions
   ├─ Web application hosting? → App Service
   └─ Long-running background tasks? → WebJobs
```

### When to Use Which Storage Service?

```
What type of data?
├─ Structured/Relational → Azure SQL Database
├─ Semi-structured (JSON documents)
│  ├─ Global distribution needed? → Cosmos DB
│  └─ Simple key-value store? → Table Storage
├─ Files/Blobs
│  ├─ Unstructured (images, videos) → Blob Storage
│  └─ Shared file system (SMB/NFS) → Azure Files
└─ Big Data Analytics → Data Lake Storage Gen2
```

### When to Use Which Messaging Service?

```
What's your messaging pattern?
├─ Discrete events, reactive programming
│  ├─ High throughput streaming? → Event Hubs
│  └─ Lightweight notifications? → Event Grid
└─ Message-based communication
   ├─ Enterprise features (sessions, transactions)? → Service Bus
   └─ Simple async queue? → Queue Storage
```

### Service Bus: Queue vs Topic?

```
How many consumers?
├─ Single consumer → Queue
└─ Multiple consumers
   ├─ All get same message? → Topic (no filters)
   └─ Each gets filtered subset? → Topic (with filters)
```

### Cosmos DB: Which Consistency Level?

```
What are your requirements?
├─ Must read own writes immediately?
│  ├─ Strongest guarantee needed? → Strong
│  └─ Within same session OK? → Session
├─ Bounded staleness acceptable?
│  ├─ Need lag guarantees? → Bounded Staleness
│  └─ Ordered reads important? → Consistent Prefix
└─ Lowest latency, highest availability? → Eventual
```

---

## Common Patterns and Best Practices

### Pattern 1: Secure Configuration Pattern
```csharp
// Best Practice: Store secrets in Key Vault, reference from App Configuration

// 1. Store secret in Key Vault
var secretClient = new SecretClient(vaultUri, new DefaultAzureCredential());
await secretClient.SetSecretAsync("DbConnection", connectionString);

// 2. Reference from App Configuration
var configClient = new ConfigurationClient(configConnectionString);
await configClient.SetConfigurationSettingAsync(
    "ConnectionStrings:Default",
    $"{{\"uri\":\"https://myvault.vault.azure.net/secrets/DbConnection\"}}"
);

// 3. Load in application
var builder = new ConfigurationBuilder();
builder.AddAzureAppConfiguration(options =>
{
    options.Connect(configConnectionString)
           .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()));
});
```

### Pattern 2: Retry with Exponential Backoff
```csharp
// Using Polly library
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: retryAttempt => 
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
        onRetry: (exception, timeSpan, retryCount, context) =>
        {
            Console.WriteLine($"Retry {retryCount} after {timeSpan.TotalSeconds}s");
        });

await retryPolicy.ExecuteAsync(async () =>
{
    var response = await httpClient.GetAsync(url);
    response.EnsureSuccessStatusCode();
});
```

### Pattern 3: Circuit Breaker
```csharp
var circuitBreakerPolicy = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 3,
        durationOfBreak: TimeSpan.FromSeconds(30),
        onBreak: (exception, duration) =>
        {
            Console.WriteLine($"Circuit broken for {duration.TotalSeconds}s");
        },
        onReset: () =>
        {
            Console.WriteLine("Circuit reset");
        });
```

### Pattern 4: Correlation in Distributed Tracing
```csharp
// Propagate correlation ID across services
public class CorrelationIdMiddleware
{
    private readonly RequestDelegate _next;
    
    public async Task InvokeAsync(HttpContext context)
    {
        var correlationId = context.Request.Headers["X-Correlation-ID"].FirstOrDefault()
            ?? Guid.NewGuid().ToString();
        
        context.Items["CorrelationId"] = correlationId;
        context.Response.Headers.Add("X-Correlation-ID", correlationId);
        
        // Add to all outgoing HTTP calls
        using (var scope = new ActivityScope(correlationId))
        {
            await _next(context);
        }
    }
}
```

---

## Troubleshooting Commands

### Check App Service Logs
```bash
# Stream logs in real-time
az webapp log tail --name myWebApp --resource-group myRG

# Download logs
az webapp log download --name myWebApp --resource-group myRG

# Configure logging
az webapp log config \
  --name myWebApp \
  --resource-group myRG \
  --application-logging filesystem \
  --level verbose
```

### Query Application Insights
```kql
// Failed requests
requests
| where timestamp > ago(1h)
| where success == false
| project timestamp, name, resultCode, duration
| order by timestamp desc

// Slow requests
requests
| where timestamp > ago(1h)
| where duration > 1000
| summarize avg(duration), count() by name
| order by avg_duration desc

// Exceptions
exceptions
| where timestamp > ago(24h)
| summarize count() by type, outerMessage
| order by count_ desc

// Custom events
customEvents
| where name == "OrderPlaced"
| extend orderId = tostring(customDimensions.OrderId)
| extend total = todouble(customMeasurements.OrderValue)
| summarize sum(total), count() by bin(timestamp, 1h)
```

### Check Function App Logs
```bash
# Stream logs
func azure functionapp logstream myFunctionApp

# Get function runtime version
az functionapp config show \
  --name myFunctionApp \
  --resource-group myRG \
  --query linuxFxVersion
```

### Debug Cosmos DB Performance
```bash
# Check RU consumption
az cosmosdb sql container show \
  --account-name mycosmosacct \
  --database-name mydb \
  --name mycontainer \
  --resource-group myRG \
  --query provisionedThroughput

# View metrics
az monitor metrics list \
  --resource /subscriptions/.../Microsoft.DocumentDB/databaseAccounts/mycosmosacct \
  --metric TotalRequests \
  --interval PT1M
```

---

## Quick Reference Tables

### App Service Plan SKU Comparison
| Tier | SKU | SLA | Deployment Slots | Auto-scale | Use Case |
|------|-----|-----|------------------|------------|----------|
| Free | F1 | None | No | No | Development/Testing |
| Shared | D1 | None | No | No | Small websites |
| Basic | B1-B3 | 99.95% | No | No | Low traffic apps |
| Standard | S1-S3 | 99.95% | Yes (5) | Yes | Production apps |
| Premium | P1v2-P3v2 | 99.95% | Yes (20) | Yes | High performance |

### Cosmos DB Consistency Levels
| Level | Staleness | Latency | Throughput | Availability |
|-------|-----------|---------|------------|--------------|
| Strong | None | High | Low | Lower |
| Bounded | Configurable | Medium | Medium | Medium |
| Session | None (same session) | Low | High | Higher |
| Consistent Prefix | Prefix consistent | Low | High | Higher |
| Eventual | Possible | Lowest | Highest | Highest |

### CRON Expression Examples
| Expression | Meaning |
|-----------|---------|
| `0 */5 * * * *` | Every 5 minutes |
| `0 0 * * * *` | Every hour |
| `0 0 9 * * *` | Daily at 9 AM |
| `0 0 9 * * 1-5` | Weekdays at 9 AM |
| `0 0 0 * * 0` | Sundays at midnight |
| `0 30 */2 * * *` | Every 2 hours at :30 |

---

*This quick reference guide is designed to be a companion to your hands-on practice. Keep it handy while working through labs and building projects!*
