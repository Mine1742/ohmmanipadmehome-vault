## Azure Storage Queues

### Core Concept

Azure Storage Queues is a **simple, durable message queue** built into every storage account. It's lighter and cheaper than Service Bus, but with fewer features. Think of it as the right tool when you need basic queue functionality without the enterprise features.

---

### Queue vs Service Bus — When to Use Which

||**Storage Queue**|**Service Bus Queue**|
|---|---|---|
|Message size|64KB max|256KB (Standard) / 100MB (Premium)|
|Retention|7 days max|14 days max|
|Ordering (FIFO)|Best effort|Guaranteed (with sessions)|
|Dead letter queue|No|Yes|
|Transactions|No|Yes|
|Topics/Subscriptions|No|Yes|
|Max queue size|500TB|80GB|
|Price|Very cheap|More expensive|
|At-least-once delivery|Yes|Yes|
|Exactly-once delivery|No|Yes (with sessions)|

**Use Storage Queue when:**

- Simple task offloading with no complex routing
- Very high volume at minimal cost
- Queue size could exceed 80GB
- You need audit logs (Storage Queue integrates with Storage logging)
- Loose coupling between components with basic requirements

**Use Service Bus when:**

- Message ordering matters
- Dead letter queue needed
- Transactions required
- Topics and subscriptions needed
- Messages larger than 64KB

---

### .NET SDK — Storage Queue Operations

```bash
dotnet add package Azure.Storage.Queues
```

```csharp
// StorageQueueService.cs
using Azure.Storage.Queues;
using Azure.Storage.Queues.Models;
using Azure.Identity;

public class StorageQueueService
{
    private readonly QueueClient _queueClient;

    public StorageQueueService(string accountName, string queueName)
    {
        var serviceClient = new QueueServiceClient(
            new Uri($"https://{accountName}.queue.core.windows.net"),
            new DefaultAzureCredential());

        _queueClient = serviceClient.GetQueueClient(queueName);
    }

    public async Task InitializeAsync()
    {
        // Create queue if it doesn't exist
        await _queueClient.CreateIfNotExistsAsync();
    }

    // ─────────────────────────────────────
    // SENDING MESSAGES
    // ─────────────────────────────────────

    public async Task SendMessageAsync(string message)
    {
        // Messages are automatically Base64-encoded by the SDK
        // Storage Queue messages must be Base64 or plain text
        await _queueClient.SendMessageAsync(message);
        Console.WriteLine($"Sent: {message}");
    }

    public async Task SendObjectAsync<T>(T obj)
    {
        var json = JsonSerializer.Serialize(obj);
        await _queueClient.SendMessageAsync(json);
    }

    // Send with visibility delay — message not visible until delay expires
    // Useful for scheduling future work
    public async Task SendDelayedMessageAsync(string message, TimeSpan delay)
    {
        await _queueClient.SendMessageAsync(
            message,
            visibilityTimeout: delay,          // hidden for this long after send
            timeToLive: TimeSpan.FromDays(7)); // max retention (7 days is max)

        Console.WriteLine($"Scheduled message in {delay.TotalMinutes} minutes");
    }

    // ─────────────────────────────────────
    // RECEIVING MESSAGES
    // ─────────────────────────────────────

    // Receive and process — the standard consume pattern
    public async Task ProcessMessagesAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            // ReceiveMessages dequeues up to 32 messages
            // Messages are hidden from other consumers for visibilityTimeout
            // (default 30 seconds — you must delete within this window)
            QueueMessage[] messages = await _queueClient.ReceiveMessagesAsync(
                maxMessages: 32,
                visibilityTimeout: TimeSpan.FromSeconds(60));

            if (messages.Length == 0)
            {
                // No messages — wait before polling again
                await Task.Delay(TimeSpan.FromSeconds(5), ct);
                continue;
            }

            foreach (var message in messages)
            {
                Console.WriteLine($"Received: {message.Body}, " +
                                  $"DequeueCount: {message.DequeueCount}, " +
                                  $"MessageId: {message.MessageId}");

                try
                {
                    await ProcessMessageAsync(message.Body.ToString());

                    // Delete after successful processing
                    // Must provide BOTH messageId AND popReceipt
                    await _queueClient.DeleteMessageAsync(
                        message.MessageId,
                        message.PopReceipt);  // proves you received this message

                    Console.WriteLine($"Deleted message {message.MessageId}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Processing failed: {ex.Message}");

                    // Don't delete — message becomes visible again after
                    // visibility timeout expires, allowing retry
                    // After too many retries, consider moving to a poison queue manually

                    // Or update the message to extend visibility timeout
                    // if processing will take longer than expected
                    await _queueClient.UpdateMessageAsync(
                        message.MessageId,
                        message.PopReceipt,
                        message.Body,
                        TimeSpan.FromSeconds(60));  // extend by another 60 seconds
                }
            }
        }
    }

    // Peek — look at messages without making them invisible
    // Useful for monitoring queue depth
    public async Task PeekMessagesAsync()
    {
        // PeekMessages returns up to 32 messages without dequeuing
        PeekedMessage[] peeked = await _queueClient.PeekMessagesAsync(maxMessages: 10);

        foreach (var message in peeked)
        {
            Console.WriteLine($"Peeked: {message.Body}, " +
                              $"InsertedOn: {message.InsertedOn}");
        }
    }

    // Get approximate queue length (useful for autoscale decisions)
    public async Task<int> GetApproximateMessageCountAsync()
    {
        QueueProperties props = await _queueClient.GetPropertiesAsync();
        Console.WriteLine($"Approximate message count: {props.ApproximateMessagesCount}");
        return props.ApproximateMessagesCount;
    }

    // Clear all messages
    public async Task ClearQueueAsync()
    {
        await _queueClient.ClearMessagesAsync();
        Console.WriteLine("Queue cleared");
    }

    private Task ProcessMessageAsync(string message)
    {
        Console.WriteLine($"Processing: {message}");
        return Task.CompletedTask;
    }
}
```

---

### Poison Message Handling

Storage Queues don't have a built-in dead letter queue — you implement it yourself using the `DequeueCount` property.

```csharp
public async Task ProcessWithPoisonHandlingAsync()
{
    QueueMessage[] messages = await _queueClient.ReceiveMessagesAsync(maxMessages: 1);

    foreach (var message in messages)
    {
        // DequeueCount tells you how many times this message has been received
        if (message.DequeueCount > 5)
        {
            Console.WriteLine($"Poison message detected: {message.MessageId}");

            // Move to a poison/dead-letter queue manually
            var poisonQueue = new QueueClient(
                new Uri($"https://myaccount.queue.core.windows.net/orders-poison"),
                new DefaultAzureCredential());

            await poisonQueue.CreateIfNotExistsAsync();
            await poisonQueue.SendMessageAsync(message.Body);

            // Delete from original queue
            await _queueClient.DeleteMessageAsync(
                message.MessageId, message.PopReceipt);

            Console.WriteLine("Moved to poison queue");
            continue;
        }

        try
        {
            await ProcessMessageAsync(message.Body.ToString());
            await _queueClient.DeleteMessageAsync(message.MessageId, message.PopReceipt);
        }
        catch
        {
            // Don't delete — will retry up to dequeueCount limit
            Console.WriteLine($"Failed, will retry. Count: {message.DequeueCount}");
        }
    }
}
```

---

### Storage Queue as Azure Functions Trigger

```csharp
// Simpler than writing a polling loop yourself
[Function("ProcessOrderQueue")]
public async Task ProcessQueueMessageAsync(
    [QueueTrigger("orders",
        Connection = "AzureWebJobsStorage")]
    Order order,                        // SDK deserializes JSON automatically
    FunctionContext context)
{
    _logger.LogInformation("Processing order from queue: {Id}", order.Id);
    // Functions handles polling, visibility timeout renewal, and deletion
    // If the function throws, the message becomes visible again for retry
    // After maxDequeueCount, message moves to orders-poison queue automatically
}
```

---

## Putting It All Together — Common Patterns

### Pattern 1: Image Processing Pipeline

```
User uploads image via web app
        │
        ▼
Blob Storage (uploads container) ──► Event Grid (BlobCreated event)
                                              │
                                              ▼
                                     Azure Function (triggered by event)
                                              │
                                    ├── Resize image
                                    ├── Generate thumbnail
                                    └── Write to processed container
                                              │
                                              ▼
                                     Storage Queue message
                                     ("image ready for CDN")
```

### Pattern 2: Cost-Optimized Log Archive

```
Application writes logs to Append Blob (Hot tier)
        │
        ▼ After 30 days (Lifecycle Policy)
Cool tier
        │
        ▼ After 90 days
Archive tier
        │
        ▼ After 365 days
Deleted automatically
```

---