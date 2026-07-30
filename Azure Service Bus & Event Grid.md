# Azure Service Bus & Event Grid

These two services are often confused because they both move data between services — but they solve fundamentally different problems. Understanding when to use which is one of the most tested concepts in this space.

---

## The Core Distinction

Before diving into either service, nail this mental model:

**Service Bus** is a **message broker** — it's about reliable delivery of commands and data between services. The message has a specific intended recipient. The sender cares that the message was processed. Think "do this thing."

**Event Grid** is an **event router** — it's about notifying interested parties that something happened. The publisher doesn't know or care who's listening. Think "this thing happened."

```
Service Bus:  OrderService ──[process this payment]──► PaymentService
              (one sender, one receiver, reliable delivery, ordering matters)

Event Grid:   BlobStorage ──[file was uploaded]──► [Function A, Function B, Logic App]
              (one publisher, many subscribers, fire-and-forget notification)
```

---

## Part 1: Azure Service Bus

### Core Concept

Service Bus is a **fully managed enterprise message broker** with queues and topics. It guarantees message delivery, supports ordering, dead lettering, transactions, and sessions. It's the right tool when losing a message is unacceptable — financial transactions, order processing, inventory updates.

---

### Key Components

**Namespace** — the top-level container. Has a globally unique hostname like `mybus.servicebus.windows.net`. You create queues and topics inside it.

az servicebus namespace create \ --resource-group $resourceGroup \ --name $namespaceName \ --location $location

**Queue** — point-to-point messaging. One sender, one receiver (or competing receivers). Messages are stored until a consumer picks them up and explicitly completes them.

az servicebus queue create --resource-group $resourceGroup \ --namespace-name $namespaceName \ --name myqueue

**Topic** — publish/subscribe messaging. One sender, multiple receivers. Publishers send to the topic, subscribers each get their own independent copy via **subscriptions**.

**Subscription** — a named consumer of a topic. Each subscription gets a full copy of every message published to the topic. You can add **filters** so a subscription only receives messages matching certain criteria.

**Message** — the unit of data. Has a body (byte array, typically JSON) plus system properties (MessageId, CorrelationId, SessionId, TTL) and user-defined custom properties.


##### Run the following command to create and assign the **Azure Service Bus Data Owner** role.
az role assignment create --assignee $userPrincipal \ --role "Azure Service Bus Data Owner" \ --scope $resourceID
## Create a .NET console app to send and receive messages
mkdir svcbus cd svcbus
dotnet new console
dotnet add package Azure.Messaging.ServiceBus dotnet add package Azure.Identity
code Program.cs

using Azure.Messaging.ServiceBus;

using Azure.Identity;

using System.Timers;

  
  

// TODO: Replace <YOUR-NAMESPACE> with your Service Bus namespace

string svcbusNameSpace = "**svcbusns3106**.servicebus.windows.net";

string queueName = "myQueue";

  
  

// ADD CODE TO CREATE A SERVICE BUS CLIENT

// Create a DefaultAzureCredentialOptions object to configure the DefaultAzureCredential

DefaultAzureCredentialOptions options = new()

{

ExcludeEnvironmentCredential = true,

ExcludeManagedIdentityCredential = true

};

  

// Create a Service Bus client using the namespace and DefaultAzureCredential

// The DefaultAzureCredential will use the Azure CLI credentials, so ensure you are logged in

ServiceBusClient client = new(svcbusNameSpace, new DefaultAzureCredential(options));

  
  

// ADD CODE TO SEND MESSAGES TO THE QUEUE

// Create a sender for the specified queue

ServiceBusSender sender = client.CreateSender(queueName);

  

// create a batch

using ServiceBusMessageBatch messageBatch = await sender.CreateMessageBatchAsync();

  

// number of messages to be sent to the queue

const int numOfMessages = 3;

  

for (int i = 1; i <= numOfMessages; i++)

{

// try adding a message to the batch

if (!messageBatch.TryAddMessage(new ServiceBusMessage($"Message {i}")))

{

// if it is too large for the batch

throw new Exception($"The message {i} is too large to fit in the batch.");

}

}

  

try

{

// Use the producer client to send the batch of messages to the Service Bus queue

await sender.SendMessagesAsync(messageBatch);

Console.WriteLine($"A batch of {numOfMessages} messages has been published to the queue.");

}

finally

{

// Calling DisposeAsync on client types is required to ensure that network

// resources and other unmanaged objects are properly cleaned up.

await sender.DisposeAsync();

}

  

Console.WriteLine("Press any key to continue");

Console.ReadKey();

  
  

// ADD CODE TO PROCESS MESSAGES FROM THE QUEUE

  

// Create a processor that we can use to process the messages in the queue

ServiceBusProcessor processor = client.CreateProcessor(queueName, new ServiceBusProcessorOptions());

  

// Idle timeout in milliseconds, the idle timer will stop the processor if there are no more

// messages in the queue to process

const int idleTimeoutMs = 3000;

System.Timers.Timer idleTimer = new(idleTimeoutMs);

idleTimer.Elapsed += async (s, e) =>

{

Console.WriteLine($"No messages received for {idleTimeoutMs / 1000} seconds. Stopping processor...");

await processor.StopProcessingAsync();

};

  

try

{

// add handler to process messages

processor.ProcessMessageAsync += MessageHandler;

  

// add handler to process any errors

processor.ProcessErrorAsync += ErrorHandler;

  

// start processing

idleTimer.Start();

await processor.StartProcessingAsync();

  

Console.WriteLine($"Processor started. Will stop after {idleTimeoutMs / 1000} seconds of inactivity.");

// Wait for the processor to stop

while (processor.IsProcessing)

{

await Task.Delay(500);

}

idleTimer.Stop();

Console.WriteLine("Stopped receiving messages");

}

finally

{

// Dispose processor after use

await processor.DisposeAsync();

}

  

// handle received messages

async Task MessageHandler(ProcessMessageEventArgs args)

{

string body = args.Message.Body.ToString();

Console.WriteLine($"Received: {body}");

  

// Reset the idle timer on each message

idleTimer.Stop();

idleTimer.Start();

  

// complete the message. message is deleted from the queue.

await args.CompleteMessageAsync(args.Message);

}

  

// handle any errors when receiving messages

Task ErrorHandler(ProcessErrorEventArgs args)

{

Console.WriteLine(args.Exception.ToString());

return Task.CompletedTask;

}

  

// Dispose client after use

await client.DisposeAsync();
### Service Tiers

**Basic** — queues only. No topics, no sessions, no transactions, no dead lettering. 256KB message size. Dev/test only.

**Standard** — queues and topics, sessions, dead lettering, scheduled messages, 256KB message size. Variable throughput.

**Premium** — dedicated capacity (Messaging Units), 100MB message size, VNet integration, Geo-disaster recovery, zone redundancy. For production enterprise workloads.

The exam expects you to know that **topics require Standard or Premium** — they're not available in Basic.

---

### Queues — Point-to-Point

```csharp
// ServiceBusDemo.cs
using Azure.Messaging.ServiceBus;
using Azure.Identity;

public class ServiceBusQueueDemo
{
    private readonly ServiceBusClient _client;
    private const string QueueName = "orders";

    public ServiceBusQueueDemo(string fullyQualifiedNamespace)
    {
        // Use managed identity — no connection string
        _client = new ServiceBusClient(fullyQualifiedNamespace,
            new DefaultAzureCredential());
    }

    // ─────────────────────────────────────
    // SENDING MESSAGES
    // ─────────────────────────────────────

    public async Task SendSingleMessageAsync(Order order)
    {
        await using var sender = _client.CreateSender(QueueName);

        var message = new ServiceBusMessage(
            BinaryData.FromObjectAsJson(order))
        {
            // MessageId for deduplication — if same ID sent twice, second is discarded
            // (requires duplicate detection enabled on the queue)
            MessageId = order.Id,

            // CorrelationId for linking related messages (e.g., request/response)
            CorrelationId = Guid.NewGuid().ToString(),

            // ContentType hint for the receiver
            ContentType = "application/json",

            // TTL — message expires after 1 hour if not processed
            TimeToLive = TimeSpan.FromHours(1),

            // Custom user properties — queryable, usable in filters
            ApplicationProperties =
            {
                { "customerId", order.CustomerId },
                { "region", order.CustomerRegion },
                { "priority", order.Amount > 1000 ? "high" : "normal" }
            }
        };

        await sender.SendMessageAsync(message);
        Console.WriteLine($"Sent order {order.Id}");
    }

    public async Task SendBatchAsync(List<Order> orders)
    {
        await using var sender = _client.CreateSender(QueueName);

        // CreateMessageBatchAsync creates a batch that respects the max size limit
        // Messages are added until the batch is full, then a new batch is created
        using ServiceBusMessageBatch batch = await sender.CreateMessageBatchAsync();

        foreach (var order in orders)
        {
            var message = new ServiceBusMessage(BinaryData.FromObjectAsJson(order));

            if (!batch.TryAddMessage(message))
            {
                // Batch is full — send current batch and start a new one
                await sender.SendMessagesAsync(batch);
                Console.WriteLine($"Sent batch of {batch.Count} messages");
            }
        }

        // Send any remaining messages
        if (batch.Count > 0)
            await sender.SendMessagesAsync(batch);
    }

    // Scheduled message — appears in queue at a specific time
    public async Task ScheduleMessageAsync(Order order, DateTimeOffset enqueueAt)
    {
        await using var sender = _client.CreateSender(QueueName);

        var message = new ServiceBusMessage(BinaryData.FromObjectAsJson(order));

        // Returns a sequence number you can use to cancel the scheduled message
        long sequenceNumber = await sender.ScheduleMessageAsync(message, enqueueAt);
        Console.WriteLine($"Scheduled message with sequence number: {sequenceNumber}");

        // Cancel it later if needed
        // await sender.CancelScheduledMessageAsync(sequenceNumber);
    }

    // ─────────────────────────────────────
    // RECEIVING MESSAGES — two patterns
    // ─────────────────────────────────────

    // Pattern 1: Processor (recommended for production)
    // Handles concurrency, error handling, and renewal automatically
    public async Task StartProcessorAsync()
    {
        var processorOptions = new ServiceBusProcessorOptions
        {
            MaxConcurrentCalls = 5,       // process up to 5 messages simultaneously
            AutoCompleteMessages = false,  // we'll manually complete/abandon
            MaxAutoLockRenewalDuration = TimeSpan.FromMinutes(5)
            // Auto-renews the message lock so long-running processing doesn't time out
        };

        await using var processor = _client.CreateProcessor(QueueName, processorOptions);

        processor.ProcessMessageAsync += HandleMessageAsync;
        processor.ProcessErrorAsync += HandleErrorAsync;

        await processor.StartProcessingAsync();
        Console.WriteLine("Processor started. Press any key to stop.");
        Console.ReadKey();
        await processor.StopProcessingAsync();
    }

    private async Task HandleMessageAsync(ProcessMessageEventArgs args)
    {
        var order = args.Message.Body.ToObjectFromJson<Order>();
        Console.WriteLine($"Processing order: {order.Id}");

        try
        {
            await ProcessOrderAsync(order);

            // Complete — removes message from queue permanently
            await args.CompleteMessageAsync(args.Message);
            Console.WriteLine($"Order {order.Id} completed");
        }
        catch (InvalidOperationException ex)
        {
            // Business logic failure — dead letter with reason
            // Message moves to $deadletterqueue — investigate and replay manually
            await args.DeadLetterMessageAsync(args.Message,
                deadLetterReason: "BusinessRuleViolation",
                deadLetterErrorDescription: ex.Message);
            Console.WriteLine($"Dead lettered order {order.Id}: {ex.Message}");
        }
        catch (Exception ex)
        {
            // Transient failure — abandon so another consumer can retry
            // After MaxDeliveryCount retries, Service Bus auto-dead-letters it
            await args.AbandonMessageAsync(args.Message);
            Console.WriteLine($"Abandoned order {order.Id} for retry: {ex.Message}");
        }
    }

    private Task HandleErrorAsync(ProcessErrorEventArgs args)
    {
        Console.WriteLine($"Service Bus error: {args.Exception.Message}");
        Console.WriteLine($"Source: {args.ErrorSource}");
        return Task.CompletedTask;
    }

    // Pattern 2: Manual receive — for more control or batch processing
    public async Task ReceiveManuallyAsync()
    {
        await using var receiver = _client.CreateReceiver(QueueName,
            new ServiceBusReceiverOptions
            {
                // PeekLock (default): message is locked while you process it
                // If you don't complete/abandon within lock timeout, it becomes
                // visible again for another consumer
                ReceiveMode = ServiceBusReceiveMode.PeekLock

                // ReceiveAndDelete: message is immediately removed on receipt
                // Faster but if your processing fails, message is gone
                // ReceiveMode = ServiceBusReceiveMode.ReceiveAndDelete
            });

        // Receive up to 10 messages, wait up to 5 seconds
        var messages = await receiver.ReceiveMessagesAsync(
            maxMessages: 10,
            maxWaitTime: TimeSpan.FromSeconds(5));

        foreach (var message in messages)
        {
            var order = message.Body.ToObjectFromJson<Order>();
            Console.WriteLine($"Received: {order.Id}, DeliveryCount: {message.DeliveryCount}");

            // Peek at dead letter queue without removing
            // await receiver.PeekMessageAsync(); for non-destructive look

            await receiver.CompleteMessageAsync(message);
        }
    }

    // Peek — look at messages without locking or removing them
    public async Task PeekMessagesAsync()
    {
        await using var receiver = _client.CreateReceiver(QueueName);

        var peekedMessages = await receiver.PeekMessagesAsync(maxMessages: 5);
        foreach (var msg in peekedMessages)
        {
            Console.WriteLine($"Peeked: {msg.MessageId}, " +
                              $"EnqueuedAt: {msg.EnqueuedTime}");
        }
    }

    private Task ProcessOrderAsync(Order order) => Task.CompletedTask;
}
```

---

### Topics and Subscriptions — Publish/Subscribe

```csharp
public class ServiceBusTopicDemo
{
    private readonly ServiceBusClient _client;
    private const string TopicName = "order-events";

    public ServiceBusTopicDemo(string fullyQualifiedNamespace)
    {
        _client = new ServiceBusClient(fullyQualifiedNamespace,
            new DefaultAzureCredential());
    }

    // Publisher — sends to topic, doesn't know who's listening
    public async Task PublishOrderEventAsync(Order order, string eventType)
    {
        await using var sender = _client.CreateSender(TopicName);

        var message = new ServiceBusMessage(BinaryData.FromObjectAsJson(order))
        {
            Subject = eventType,   // e.g. "OrderCreated", "OrderShipped"
            ApplicationProperties =
            {
                { "eventType", eventType },
                { "region", order.CustomerRegion },
                { "amount", order.Amount }
            }
        };

        await sender.SendMessageAsync(message);
        Console.WriteLine($"Published {eventType} for order {order.Id}");
    }

    // Each subscription independently receives all messages
    // (or filtered subset based on subscription rules)
    public async Task ConsumeFromSubscriptionAsync(string subscriptionName)
    {
        await using var processor = _client.CreateProcessor(
            TopicName,
            subscriptionName);

        processor.ProcessMessageAsync += async args =>
        {
            var order = args.Message.Body.ToObjectFromJson<Order>();
            var eventType = args.Message.ApplicationProperties["eventType"].ToString();

            Console.WriteLine($"[{subscriptionName}] Received {eventType} " +
                              $"for order {order.Id}");

            await args.CompleteMessageAsync(args.Message);
        };

        processor.ProcessErrorAsync += args =>
        {
            Console.WriteLine($"Error: {args.Exception.Message}");
            return Task.CompletedTask;
        };

        await processor.StartProcessingAsync();
        await Task.Delay(TimeSpan.FromSeconds(30));
        await processor.StopProcessingAsync();
    }
}
```

### Setting Up Subscription Filters via CLI

This is important for the exam — filters determine which messages a subscription receives.

```bash
# Create namespace, topic, and subscriptions
az servicebus namespace create \
  --resource-group myRG \
  --name myservicebus \
  --sku Standard

az servicebus topic create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --name order-events

# Subscription 1: all order events (no filter = receives everything)
az servicebus topic subscription create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --name all-orders

# Subscription 2: only high-value orders (SQL filter on user properties)
az servicebus topic subscription create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --name high-value-orders

az servicebus topic subscription rule create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --subscription-name high-value-orders \
  --name highValueFilter \
  --filter-sql-expression "amount > 1000"

# Subscription 3: only EU region orders
az servicebus topic subscription create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --name eu-orders

az servicebus topic subscription rule create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --subscription-name eu-orders \
  --name euFilter \
  --filter-sql-expression "region = 'EU'"

# Correlation filter (faster/cheaper than SQL filter for exact matches)
az servicebus topic subscription rule create \
  --resource-group myRG \
  --namespace-name myservicebus \
  --topic-name order-events \
  --subscription-name shipped-only \
  --name shippedFilter \
  --action-sql-expression "SET sys.label = 'processed'" \
  --filter-correlation-id "OrderShipped"
```

Three filter types to know for the exam:

**SQL Filter** — evaluates a SQL-like expression against message properties. Most flexible. `"amount > 1000 AND region = 'US'"`. Slightly more expensive to evaluate.

**Correlation Filter** — exact match on system or user properties. Much faster and cheaper than SQL filters. Use whenever you just need equality checks.

**Boolean Filter** — `TrueFilter` (receives all messages) or `FalseFilter` (receives none). Used to enable/disable subscriptions.

---

### Sessions — Ordered, Grouped Processing

Sessions are a powerful feature for scenarios where **message ordering matters within a group** — like processing all events for a specific order in sequence, or handling all messages for a specific user in order.

```csharp
public class SessionDemo
{
    private readonly ServiceBusClient _client;

    public SessionDemo(string fullyQualifiedNamespace)
    {
        _client = new ServiceBusClient(fullyQualifiedNamespace,
            new DefaultAzureCredential());
    }

    // Send messages with a session ID
    // All messages with the same SessionId are delivered in order
    // to the same consumer (exclusive lock on the session)
    public async Task SendOrderEventsAsync(string orderId)
    {
        await using var sender = _client.CreateSender("order-events-session");

        // These three messages will always be processed IN ORDER
        // by the SAME consumer because they share a SessionId
        string[] events = { "OrderCreated", "PaymentProcessed", "OrderShipped" };

        foreach (var evt in events)
        {
            var message = new ServiceBusMessage(evt)
            {
                SessionId = orderId    // groups messages and enforces ordering
            };
            await sender.SendMessageAsync(message);
        }
    }

    // Receive with session processor
    public async Task ProcessSessionsAsync()
    {
        await using var processor = _client.CreateSessionProcessor(
            "order-events-session",
            new ServiceBusSessionProcessorOptions
            {
                MaxConcurrentSessions = 3,     // process 3 different sessions in parallel
                MaxConcurrentCallsPerSession = 1  // but only 1 message at a time per session
            });

        processor.ProcessMessageAsync += async args =>
        {
            // args.SessionId tells you which group this message belongs to
            Console.WriteLine($"Session: {args.Message.SessionId}, " +
                              $"Message: {args.Message.Body}");

            // You can store state per session
            var sessionState = await args.GetSessionStateAsync();
            // ... update state ...
            await args.SetSessionStateAsync(BinaryData.FromString("new state"));

            await args.CompleteMessageAsync(args.Message);
        };

        processor.ProcessErrorAsync += args =>
        {
            Console.WriteLine($"Error: {args.Exception.Message}");
            return Task.CompletedTask;
        };

        await processor.StartProcessingAsync();
        await Task.Delay(TimeSpan.FromMinutes(1));
        await processor.StopProcessingAsync();
    }
}
```

---

### Dead Letter Queue

Every queue and subscription automatically has a **Dead Letter Queue (DLQ)** — a sub-queue at `queuename/$deadletterqueue`. Messages end up here when they exceed `MaxDeliveryCount`, when you explicitly dead-letter them, or when they expire.

```csharp
public async Task ProcessDeadLetterQueueAsync()
{
    // Access the DLQ by appending /$deadletterqueue to the queue name
    await using var receiver = _client.CreateReceiver(
        "orders",
        new ServiceBusReceiverOptions
        {
            SubQueue = SubQueue.DeadLetter    // this is the key setting
        });

    var deadLettered = await receiver.ReceiveMessagesAsync(maxMessages: 10);

    foreach (var msg in deadLettered)
    {
        Console.WriteLine($"Dead letter reason: {msg.DeadLetterReason}");
        Console.WriteLine($"Dead letter description: {msg.DeadLetterErrorDescription}");
        Console.WriteLine($"Delivery count: {msg.DeliveryCount}");
        Console.WriteLine($"Body: {msg.Body}");

        // Investigate, fix the issue, then either:
        // 1. Resubmit to original queue
        // 2. Complete (discard) if truly invalid
        await receiver.CompleteMessageAsync(msg);
    }
}
```

---

### Transactions

Service Bus supports **atomic transactions** — multiple operations succeed or fail together. Scoped to a single entity (queue or topic).

```csharp
public async Task TransactionalSendAsync(Order order)
{
    await using var sender1 = _client.CreateSender("orders");
    await using var sender2 = _client.CreateSender("audit-log");

    // Both messages are sent atomically or neither is
    using var transaction = new ServiceBusTransactionScope();

    await sender1.SendMessageAsync(
        new ServiceBusMessage(BinaryData.FromObjectAsJson(order)));

    await sender2.SendMessageAsync(
        new ServiceBusMessage($"Order {order.Id} created at {DateTime.UtcNow}"));

    // Commit both sends atomically
    await transaction.CompleteAsync();
}
```

---

## Part 2: Event Grid

### Core Concept

Event Grid is a **fully managed event routing service** that connects event publishers to event subscribers using a pub/sub model. It's built for reactive, event-driven architectures — when something happens in Azure (or in your app), interested parties are notified immediately.

The key difference from Service Bus: Event Grid **doesn't store messages** waiting for consumers. It delivers events and moves on. It's not a queue — if nobody's listening when an event fires, the event is gone (subject to retry policy). It's optimized for fan-out notification, not reliable command delivery.

---

### Key Components

**Event Source** — what generates events. Azure services (Blob Storage, Resource Groups, Key Vault, Service Bus, etc.) or your own custom topics.

**Topic** — the endpoint where events are published. Two types: **system topics** (created automatically for Azure services) and **custom topics** (for your own application events).

**Event Subscription** — connects a topic to a handler. Defines which events to deliver and where to send them. Can include filters.

**Event Handler** — where events are delivered. Azure Functions, Logic Apps, Event Hubs, Service Bus queues/topics, Webhooks, Storage Queues, Relay Hybrid Connections.

**Event Domain** — a management tool for organizing large numbers of topics (thousands of topics under one endpoint). Used for multi-tenant scenarios.

---

### Event Schema

Event Grid delivers events in a standard schema. Know this for the exam.

```json
[
  {
    "id": "abc123",
    "topic": "/subscriptions/{sub}/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/mystorage",
    "subject": "/blobServices/default/containers/uploads/blobs/myfile.csv",
    "eventType": "Microsoft.Storage.BlobCreated",
    "eventTime": "2024-03-15T10:30:00.000Z",
    "dataVersion": "1.0",
    "metadataVersion": "1",
    "data": {
      "api": "PutBlob",
      "clientRequestId": "xyz789",
      "requestId": "def456",
      "eTag": "0x8D4BCC2E4835CD0",
      "contentType": "text/csv",
      "contentLength": 524288,
      "blobType": "BlockBlob",
      "url": "https://mystorage.blob.core.windows.net/uploads/myfile.csv",
      "sequencer": "00000000000004420000000000028963"
    }
  }
]
```

Event Grid also supports the **CloudEvents 1.0 schema** — an open standard. For new workloads, CloudEvents is recommended.

```json
{
  "specversion": "1.0",
  "type": "Microsoft.Storage.BlobCreated",
  "source": "/subscriptions/{sub}/resourceGroups/myRG/providers/Microsoft.Storage/storageAccounts/mystorage",
  "id": "abc123",
  "time": "2024-03-15T10:30:00Z",
  "subject": "/blobServices/default/containers/uploads/blobs/myfile.csv",
  "datacontenttype": "application/json",
  "data": {
    "api": "PutBlob",
    "url": "https://mystorage.blob.core.windows.net/uploads/myfile.csv"
  }
}
```

---

### System Topics — Built-in Azure Service Events

Many Azure services publish events automatically. You just subscribe.

```bash
# Subscribe to Blob Storage events — trigger a Function when a blob is created
az eventgrid system-topic create \
  --resource-group myRG \
  --name storageTopic \
  --location eastus \
  --topic-type Microsoft.Storage.StorageAccounts \
  --source $(az storage account show \
      --name mystorageaccount \
      --resource-group myRG \
      --query id --output tsv)

# Create a subscription pointing to a Function
az eventgrid system-topic event-subscription create \
  --resource-group myRG \
  --system-topic-name storageTopic \
  --name blobCreatedSub \
  --endpoint $(az functionapp function show \
      --resource-group myRG \
      --name myfunctionapp \
      --function-name ProcessBlob \
      --query invokeUrlTemplate --output tsv) \
  --endpoint-type azurefunction \
  --included-event-types Microsoft.Storage.BlobCreated \
  --subject-begins-with /blobServices/default/containers/uploads/
```

Built-in event sources to know for the exam:

|Source|Common Event Types|
|---|---|
|Blob Storage|BlobCreated, BlobDeleted|
|Resource Groups|ResourceWriteSuccess, ResourceDeleteSuccess|
|Key Vault|SecretNearExpiry, SecretExpired, CertificateNearExpiry|
|Service Bus|ActiveMessagesAvailableWithNoListeners|
|Container Registry|ImagePushed, ImageDeleted|
|App Service|BackupOperationCompleted, RestoreOperationCompleted|
|Azure Maps|Geofence.Entered, Geofence.Exited|

---

### Custom Topics — Your Own Application Events

```bash
# Create a custom topic
az eventgrid topic create \
  --resource-group myRG \
  --name order-events-topic \
  --location eastus \
  --input-schema cloudeventschemav1_0   # use CloudEvents schema

# Get the endpoint and key
TOPIC_ENDPOINT=$(az eventgrid topic show \
  --name order-events-topic \
  --resource-group myRG \
  --query endpoint \
  --output tsv)

# Subscribe a webhook (any HTTPS endpoint)
az eventgrid event-subscription create \
  --source-resource-id $(az eventgrid topic show \
      --name order-events-topic \
      --resource-group myRG \
      --query id --output tsv) \
  --name orderCreatedSub \
  --endpoint https://myapp.azurewebsites.net/api/events/orders \
  --endpoint-type webhook \
  --included-event-types OrderCreated OrderShipped \
  --subject-begins-with /orders/
```

---

### Publishing Events from .NET

```csharp
// EventGridPublisher.cs
using Azure.Messaging.EventGrid;
using Azure.Messaging;   // for CloudEvents
using Azure.Identity;

public class EventGridPublisher
{
    private readonly EventGridPublisherClient _client;

    public EventGridPublisher(string topicEndpoint)
    {
        // Authenticate with managed identity
        _client = new EventGridPublisherClient(
            new Uri(topicEndpoint),
            new DefaultAzureCredential());
    }

    // ─────────────────────────────────────
    // Publishing using CloudEvents schema (recommended)
    // ─────────────────────────────────────
    public async Task PublishOrderCreatedAsync(Order order)
    {
        var cloudEvent = new CloudEvent(
            source: "/orders/service",           // who published this
            type: "com.mycompany.orders.created", // event type (reverse DNS convention)
            jsonSerializableData: order)          // payload
        {
            Subject = $"/orders/{order.Id}",
            Id = Guid.NewGuid().ToString(),
            Time = DateTimeOffset.UtcNow
        };

        await _client.SendEventAsync(cloudEvent);
        Console.WriteLine($"Published OrderCreated for {order.Id}");
    }

    // Publish a batch of events (more efficient than one at a time)
    public async Task PublishOrderEventsAsync(List<Order> orders)
    {
        var events = orders.Select(order => new CloudEvent(
            source: "/orders/service",
            type: "com.mycompany.orders.created",
            jsonSerializableData: order)
        {
            Subject = $"/orders/{order.Id}"
        }).ToList();

        await _client.SendEventsAsync(events);
        Console.WriteLine($"Published {events.Count} order events");
    }

    // ─────────────────────────────────────
    // Publishing using EventGrid schema
    // ─────────────────────────────────────
    public async Task PublishUsingEventGridSchemaAsync(Order order)
    {
        var gridEvent = new EventGridEvent(
            subject: $"/orders/{order.Id}",
            eventType: "OrderCreated",
            dataVersion: "1.0",
            data: BinaryData.FromObjectAsJson(order));

        await _client.SendEventAsync(gridEvent);
    }
}
```

---

### Receiving Events — Azure Function Handler

```csharp
// EventGridFunction.cs
using Azure.Messaging.EventGrid;
using Azure.Messaging;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

public class EventGridFunction
{
    private readonly ILogger<EventGridFunction> _logger;

    public EventGridFunction(ILogger<EventGridFunction> logger)
    {
        _logger = logger;
    }

    // ─────────────────────────────────────
    // Option 1: EventGrid trigger (simplest — no webhook validation needed)
    // ─────────────────────────────────────
    [Function("HandleOrderEvent")]
    public async Task HandleOrderEventAsync(
        [EventGridTrigger] CloudEvent cloudEvent,
        FunctionContext context)
    {
        _logger.LogInformation("Event received: Type={Type}, Subject={Subject}",
            cloudEvent.Type, cloudEvent.Subject);

        switch (cloudEvent.Type)
        {
            case "com.mycompany.orders.created":
                var order = cloudEvent.Data.ToObjectFromJson<Order>();
                await HandleOrderCreatedAsync(order);
                break;

            case "com.mycompany.orders.shipped":
                var shipped = cloudEvent.Data.ToObjectFromJson<Order>();
                await HandleOrderShippedAsync(shipped);
                break;

            default:
                _logger.LogWarning("Unknown event type: {Type}", cloudEvent.Type);
                break;
        }
    }

    // ─────────────────────────────────────
    // Option 2: HTTP trigger with manual Event Grid handling
    // Requires handling the subscription validation handshake
    // ─────────────────────────────────────
    [Function("HandleOrderEventWebhook")]
    public async Task<HttpResponseData> HandleWebhookAsync(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post")] HttpRequestData req,
        FunctionContext context)
    {
        var body = await req.ReadAsStringAsync();

        // Event Grid sends a validation event when you first create a subscription
        // Your webhook MUST respond correctly or the subscription won't be created
        if (req.Headers.TryGetValues("aeg-event-type", out var eventTypeHeader)
            && eventTypeHeader.First() == "SubscriptionValidation")
        {
            // Parse the validation event
            var validationEvent = EventGridEvent.ParseMany(BinaryData.FromString(body)).First();
            var validationData = validationEvent.Data.ToObjectFromJson<SubscriptionValidationData>();

            _logger.LogInformation("Subscription validation received. " +
                                   "ValidationCode: {Code}", validationData.ValidationCode);

            // Respond with the validation code to confirm the subscription
            var validationResponse = req.CreateResponse(System.Net.HttpStatusCode.OK);
            await validationResponse.WriteAsJsonAsync(new
            {
                validationResponse = validationData.ValidationCode
            });
            return validationResponse;
        }

        // Normal event processing
        var events = EventGridEvent.ParseMany(BinaryData.FromString(body));
        foreach (var evt in events)
        {
            _logger.LogInformation("Processing event: {Type}", evt.EventType);
            var order = evt.Data.ToObjectFromJson<Order>();
            await HandleOrderCreatedAsync(order);
        }

        return req.CreateResponse(System.Net.HttpStatusCode.OK);
    }

    private Task HandleOrderCreatedAsync(Order order)
    {
        _logger.LogInformation("Handling order created: {Id}", order.Id);
        return Task.CompletedTask;
    }

    private Task HandleOrderShippedAsync(Order order)
    {
        _logger.LogInformation("Handling order shipped: {Id}", order.Id);
        return Task.CompletedTask;
    }
}

// Required for webhook validation
public class SubscriptionValidationData
{
    public string ValidationCode { get; set; }
    public string ValidationUrl { get; set; }
}
```

---

### Event Grid Filtering

You can filter which events a subscription receives — by event type and by subject prefix/suffix.

```bash
# Only BlobCreated events (not BlobDeleted)
--included-event-types Microsoft.Storage.BlobCreated

# Only blobs in a specific container (subject filter)
--subject-begins-with /blobServices/default/containers/uploads/

# Only .csv files (suffix filter)
--subject-ends-with .csv

# Advanced filter on event data properties
az eventgrid event-subscription create \
  --source-resource-id $TOPIC_ID \
  --name filteredSub \
  --endpoint $ENDPOINT \
  --endpoint-type azurefunction \
  --advanced-filter data.amount NumberGreaterThan 1000 \
  --advanced-filter data.region StringIn US EU
```

---

### Delivery and Retry

Event Grid retries failed deliveries with exponential backoff for up to **24 hours** (configurable). If all retries are exhausted the event is dropped — unless you configure a **dead-letter destination**.

```bash
# Configure dead lettering to a Storage blob container
az eventgrid event-subscription create \
  --source-resource-id $TOPIC_ID \
  --name mySubscription \
  --endpoint $ENDPOINT \
  --endpoint-type azurefunction \
  --deadletter-endpoint $(az storage account show \
      --name mystorageaccount \
      --resource-group myRG \
      --query id --output tsv)/blobServices/default/containers/deadletter
```

Retry schedule (approximate):

```
Attempt 1:  immediate
Attempt 2:  10 seconds
Attempt 3:  30 seconds
Attempt 4:  1 minute
Attempt 5:  5 minutes
Attempt 6:  10 minutes
...continuing with exponential backoff up to 24 hours
```

---

## Service Bus vs Event Grid vs Event Hubs — The Full Comparison

This is one of the most tested decision points in the exam. Here it is as clearly as possible:

||**Service Bus**|**Event Grid**|**Event Hubs**|
|---|---|---|---|
|Purpose|Reliable command delivery|Event notification/routing|High-volume data streaming|
|Pattern|Queue / Pub-Sub|Pub-Sub|Streaming log|
|Message retained?|Yes, until consumed|No (delivered and gone)|Yes, for retention period|
|Ordering|Yes (sessions)|No|Yes (within partition)|
|Max message size|256KB (Standard) / 100MB (Premium)|1MB|1MB|
|Throughput|Moderate|High|Massive|
|Consumers|One (queue) / Many (topic)|Many|Many (consumer groups)|
|Use case|Order processing, payments, workflows|React to Azure resource events, trigger functions|IoT telemetry, logs, clickstreams|

**The decision framework:**

- Need to process a command reliably, with retries, ordering, and exactly-once delivery? → **Service Bus**
- Need to react to something that happened in Azure (blob created, resource deleted) or fan-out a notification to many handlers? → **Event Grid**
- Need to ingest millions of events per second and process them as a stream? → **Event Hubs**

---

## AZ-204 Exam Summary

For **Service Bus** the exam focuses on **queues vs topics/subscriptions** and when to use each, the **three filter types** (SQL, Correlation, Boolean) for subscriptions, **dead letter queues** and what causes messages to end up there, **sessions** for ordered grouped processing, the **three settlement methods** (Complete, Abandon, DeadLetter), **PeekLock vs ReceiveAndDelete** receive modes, and the **tier differences** (Basic has no topics).

For **Event Grid** the exam focuses on **system topics vs custom topics**, the **event schema** (Event Grid schema vs CloudEvents), the **webhook validation handshake** and why it exists, **event filtering** (type, subject prefix/suffix, advanced filters), **delivery retry behavior and dead lettering**, and how Event Grid integrates with **Azure Functions** via the EventGrid trigger.

The biggest exam trap is choosing between Service Bus, Event Grid, and Event Hubs for a given scenario — internalize the decision framework above and you'll handle those questions confidently.

