
# Azure Functions

Think of Azure Functions as **serverless, event-driven compute**. You write a small, focused piece of code that does one thing, and Azure runs it in response to a trigger — an HTTP request, a message on a queue, a timer, a file upload, a Cosmos DB change — without you ever thinking about servers, OS patches, or scaling infrastructure.

---
https://learn.microsoft.com/en-us/training/modules/explore-azure-functions/2-azure-functions-overview
## The Core Concept

The fundamental shift with Functions versus App Service is the **execution model**. App Service runs continuously waiting for requests. Functions are **dormant until triggered** — they wake up, do their work, and go back to sleep. You pay only for the time your code actually runs.

This makes Functions perfect for:

- Workloads with unpredictable or spiky traffic
- Event-driven processing pipelines
- Background tasks and scheduled jobs
- Lightweight APIs and webhooks
- Glue code connecting Azure services together

---
## Durable Functions
https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview


## Hosting Plans

This is heavily tested. The plan determines how your function scales, how it's billed, and what features are available.
https://learn.microsoft.com/en-us/training/modules/explore-azure-functions/3-compare-azure-functions-hosting-options

### Consumption Plan

The true serverless model. Scale from zero to thousands of instances automatically. You pay per execution and per GB-second of memory used. Cold starts are the trade-off — when a function hasn't run recently, the first invocation takes longer while Azure spins up an instance.

```
Billing:
- First 1 million executions per month: FREE
- After that: $0.20 per million executions
- Memory: $0.000016 per GB-second
```

Key characteristics:

- Maximum execution timeout: **10 minutes** (default 5 minutes)
- Scale to zero when idle — you pay nothing when not running
- Cold starts can be noticeable (typically 1-3 seconds for .NET)
- No VNet integration support

### Premium Plan

Eliminates cold starts by keeping **pre-warmed instances** always running. Supports VNet integration, longer execution timeouts, and more powerful VMs. You pay for the pre-warmed instances continuously regardless of load, plus any additional instances that scale out.

Key characteristics:

- **No cold starts** — pre-warmed workers always ready
- Maximum execution timeout: **unlimited** (default 30 minutes)
- VNet integration supported
- Supports larger instance sizes
- Scales out automatically like Consumption

### Dedicated Plan (App Service Plan)

Runs your functions on the same App Service Plan as a web app. Makes sense when you already have an App Service Plan running at less than full capacity — functions are essentially free since you're already paying for the plan. No automatic scaling beyond what you configure for the plan.

Key characteristics:

- **Always-on** — no cold starts, no scale to zero
- Manual or auto-scale (configured at the plan level, same as App Service)
- Maximum execution timeout: **unlimited**
- Predictable cost, predictable performance

### Containers (Flex Consumption / Container Apps)

You can host functions in a container for full control over the runtime environment. Runs on Azure Container Apps infrastructure. Useful when your function has unusual dependencies that don't fit the standard runtimes.

---
#### host.json
https://learn.microsoft.com/en-us/azure/azure-functions/functions-host-json


## Triggers and Bindings

This is the heart of Azure Functions and the most tested area on the exam. Instead of writing boilerplate connection code, you declare what your function responds to and what it reads/writes via **binding attributes**, and the Functions runtime handles all the connection and serialization plumbing.

**Trigger** — what causes the function to run. Every function has exactly one trigger.

**Input binding** — additional data sources your function reads from (besides the trigger).

**Output binding** — destinations your function writes to automatically when it returns.

The beauty of bindings is that your function code never needs to instantiate a `CosmosClient`, `BlobServiceClient`, or `ServiceBusClient` — the runtime injects the data directly.

---

## HTTP Trigger

The most common trigger. Turns your function into an HTTP endpoint.

```csharp
// HttpTriggerFunction.cs
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Net;

public class OrderFunctions
{
    private readonly ILogger<OrderFunctions> _logger;
    private readonly OrderRepository _orderRepo;

    // Dependency injection works just like ASP.NET Core
    public OrderFunctions(ILogger<OrderFunctions> logger, OrderRepository orderRepo)
    {
        _logger = logger;
        _orderRepo = orderRepo;
    }

    [Function("GetOrder")]
    public async Task<HttpResponseData> GetOrderAsync(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "orders/{orderId}")]
        HttpRequestData req,
        string orderId,          // route parameter injected automatically
        FunctionContext context)
    {
        _logger.LogInformation("GetOrder triggered for {OrderId}", orderId);

        var order = await _orderRepo.GetOrderAsync(orderId);

        if (order == null)
        {
            var notFound = req.CreateResponse(HttpStatusCode.NotFound);
            await notFound.WriteAsJsonAsync(new { error = "Order not found" });
            return notFound;
        }

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(order);
        return response;
    }

    [Function("CreateOrder")]
    public async Task<HttpResponseData> CreateOrderAsync(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders")]
        HttpRequestData req,
        FunctionContext context)
    {
        var order = await req.ReadFromJsonAsync<Order>();

        if (order == null)
        {
            var badRequest = req.CreateResponse(HttpStatusCode.BadRequest);
            await badRequest.WriteAsJsonAsync(new { error = "Invalid order payload" });
            return badRequest;
        }

        var created = await _orderRepo.CreateOrderAsync(order);

        var response = req.CreateResponse(HttpStatusCode.Created);
        response.Headers.Add("Location", $"/api/orders/{created.Id}");
        await response.WriteAsJsonAsync(created);
        return response;
    }
}
```

### Authorization Levels

**Anonymous** — no key required. Anyone can call the endpoint.

**Function** — requires a function-specific key passed as `?code=<key>` in the query string or `x-functions-key` header. Default for most triggers.

**Admin** — requires the master host key. Rarely used for individual functions.

For production APIs, you'd typically put **API Management** in front of Functions and use Anonymous authorization — APIM handles auth at its layer.

---

## Timer Trigger

Runs on a CRON schedule. The CRON format in Functions uses **6 fields** (includes seconds), unlike standard 5-field CRON.

```csharp
public class ScheduledFunctions
{
    private readonly ILogger<ScheduledFunctions> _logger;

    public ScheduledFunctions(ILogger<ScheduledFunctions> logger)
    {
        _logger = logger;
    }

    // Runs every day at 2:00 AM UTC
    // Format: {second} {minute} {hour} {day} {month} {day-of-week}
    [Function("DailyOrderReport")]
    public async Task RunDailyReportAsync(
        [TimerTrigger("0 0 2 * * *")] TimerInfo timer,
        FunctionContext context)
    {
        _logger.LogInformation("Daily report triggered at {Time}", DateTime.UtcNow);

        // timer.IsPastDue is true if the function should have run
        // earlier but was missed (e.g., app was down during scheduled time)
        if (timer.IsPastDue)
        {
            _logger.LogWarning("Timer is running late — was past due");
        }

        // timer.ScheduleStatus has info about last/next run times
        _logger.LogInformation("Next run scheduled: {Next}",
            timer.ScheduleStatus?.Next);

        await GenerateAndSendReportAsync();
    }

    // Every 5 minutes
    [Function("HealthCheck")]
    public void RunHealthCheck(
        [TimerTrigger("0 */5 * * * *")] TimerInfo timer,
        FunctionContext context)
    {
        _logger.LogInformation("Health check at {Time}", DateTime.UtcNow);
    }

    // Every weekday at 8 AM
    [Function("WeekdayMorningJob")]
    public void RunWeekdayJob(
        [TimerTrigger("0 0 8 * * 1-5")] TimerInfo timer,
        FunctionContext context)
    {
        _logger.LogInformation("Weekday morning job running");
    }

    private Task GenerateAndSendReportAsync() => Task.CompletedTask;
}
```

---

## Queue Trigger + Output Binding

Shows the power of bindings — no queue client code needed.

```csharp
public class QueueFunctions
{
    private readonly ILogger<QueueFunctions> _logger;

    public QueueFunctions(ILogger<QueueFunctions> logger)
    {
        _logger = logger;
    }

    // Trigger: reads from "orders-queue"
    // Output binding: writes to "processed-orders-queue" automatically
    [Function("ProcessOrder")]
    [QueueOutput("processed-orders-queue",    // output binding declared here
        Connection = "AzureWebJobsStorage")]
    public async Task<string> ProcessOrderFromQueueAsync(
        [QueueTrigger("orders-queue",
            Connection = "AzureWebJobsStorage")]
        string orderJson,                      // message deserialized automatically
        FunctionContext context)
    {
        _logger.LogInformation("Processing order from queue: {Order}", orderJson);

        var order = JsonSerializer.Deserialize<Order>(orderJson);

        // ... do processing work ...
        order.Status = "processed";

        // Return value is automatically sent to the output binding queue
        return JsonSerializer.Serialize(order);
    }

    // Trigger reads a strongly-typed object directly
    [Function("SendOrderNotification")]
    public async Task SendNotificationAsync(
        [QueueTrigger("processed-orders-queue",
            Connection = "AzureWebJobsStorage")]
        Order order,                           // SDK deserializes JSON automatically
        FunctionContext context)
    {
        _logger.LogInformation("Sending notification for order {Id}", order.Id);
        // ... send email, SMS, push notification ...
    }
}
```

---

## Cosmos DB Trigger + Multiple Output Bindings

Demonstrates Change Feed integration and writing to multiple destinations.

```csharp
public class CosmosDbFunctions
{
    private readonly ILogger<CosmosDbFunctions> _logger;

    public CosmosDbFunctions(ILogger<CosmosDbFunctions> logger)
    {
        _logger = logger;
    }

    // Triggered by Cosmos DB Change Feed
    // Output: sends a message to Service Bus + writes a blob
    [Function("OnOrderChanged")]
    public async Task<MultiOutput> HandleOrderChangeAsync(
        [CosmosDBTrigger(
            databaseName: "ecommerce",
            containerName: "orders",
            Connection = "CosmosDBConnection",
            LeaseContainerName = "leases",
            CreateLeaseContainerIfNotExists = true)]
        IReadOnlyList<Order> changedOrders,
        FunctionContext context)
    {
        _logger.LogInformation("{Count} orders changed", changedOrders.Count);

        var notifications = new List<string>();
        string auditBlob = null;

        foreach (var order in changedOrders)
        {
            _logger.LogInformation("Order {Id} changed to status: {Status}",
                order.Id, order.Status);

            if (order.Status == "shipped")
            {
                notifications.Add(JsonSerializer.Serialize(new
                {
                    orderId = order.Id,
                    customerId = order.CustomerId,
                    message = "Your order has shipped!"
                }));
            }
        }

        // Build an audit log blob content
        auditBlob = JsonSerializer.Serialize(changedOrders);

        // Return multiple outputs using a return object
        return new MultiOutput
        {
            ServiceBusMessages = notifications.ToArray(),
            AuditBlobContent = auditBlob
        };
    }
}

// Multiple output bindings via a return type
public class MultiOutput
{
    // Each property maps to an output binding declared on the class
    [ServiceBusOutput("order-notifications",
        Connection = "ServiceBusConnection")]
    public string[] ServiceBusMessages { get; set; }

    [BlobOutput("audit-logs/{DateTime.UtcNow:yyyy/MM/dd}/orders.json",
        Connection = "AzureWebJobsStorage")]
    public string AuditBlobContent { get; set; }
}
```

---

## Blob Trigger + Blob Input + Blob Output

```csharp
public class BlobFunctions
{
    private readonly ILogger<BlobFunctions> _logger;

    public BlobFunctions(ILogger<BlobFunctions> logger)
    {
        _logger = logger;
    }

    // Triggered when a file is uploaded to "uploads" container
    // Reads a config file from "configs" container (input binding)
    // Writes processed result to "processed" container (output binding)
    [Function("ProcessUploadedFile")]
    [BlobOutput("processed/{name}",              // output binding
        Connection = "AzureWebJobsStorage")]
    public async Task<byte[]> ProcessFileAsync(
        [BlobTrigger("uploads/{name}",           // trigger — fires on new blob
            Connection = "AzureWebJobsStorage")]
        Stream uploadedFile,                      // trigger data as Stream

        [BlobInput("configs/processing-config.json",  // input binding
            Connection = "AzureWebJobsStorage")]
        string configJson,                        // read a separate blob as input

        string name,                              // blob name from trigger path
        FunctionContext context)
    {
        _logger.LogInformation("Processing uploaded file: {Name}", name);

        var config = JsonSerializer.Deserialize<ProcessingConfig>(configJson);

        // Read the uploaded file
        using var memStream = new MemoryStream();
        await uploadedFile.CopyToAsync(memStream);
        var fileBytes = memStream.ToArray();

        // ... process the file according to config ...
        var processedBytes = ApplyProcessing(fileBytes, config);

        // Return value is automatically written to the output blob
        return processedBytes;
    }

    private byte[] ApplyProcessing(byte[] input, ProcessingConfig config) => input;
}

public class ProcessingConfig
{
    public string Format { get; set; }
    public int MaxSizeKb { get; set; }
}
```

---

## Service Bus Trigger

```csharp
public class ServiceBusFunctions
{
    private readonly ILogger<ServiceBusFunctions> _logger;

    public ServiceBusFunctions(ILogger<ServiceBusFunctions> logger)
    {
        _logger = logger;
    }

    // Processes messages from a Service Bus queue
    [Function("ProcessPayment")]
    public async Task ProcessPaymentAsync(
        [ServiceBusTrigger("payment-queue",
            Connection = "ServiceBusConnection")]
        ServiceBusReceivedMessage message,        // full message object with metadata
        ServiceBusMessageActions messageActions,  // for settling the message
        FunctionContext context)
    {
        _logger.LogInformation("Processing payment message {MessageId}",
            message.MessageId);

        try
        {
            var payment = message.Body.ToObjectFromJson<PaymentRequest>();

            // ... process payment ...
            await ProcessPaymentAsync(payment);

            // Explicitly complete the message — removes it from the queue
            await messageActions.CompleteMessageAsync(message);
        }
        catch (InvalidOperationException ex)
        {
            _logger.LogError(ex, "Payment processing failed — dead lettering message");

            // Dead letter — moves to dead letter queue for investigation
            await messageActions.DeadLetterMessageAsync(message,
                deadLetterReason: "ProcessingFailed",
                deadLetterErrorDescription: ex.Message);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Transient error — abandoning for retry");

            // Abandon — message goes back to queue for retry
            // Service Bus will try up to MaxDeliveryCount times before dead lettering
            await messageActions.AbandonMessageAsync(message);
        }
    }

    // Topic subscription trigger
    [Function("HandleOrderNotification")]
    public void HandleTopicMessageAsync(
        [ServiceBusTrigger("orders-topic",
            "notification-subscription",          // subscription name
            Connection = "ServiceBusConnection")]
        string messageBody,
        FunctionContext context)
    {
        _logger.LogInformation("Received topic message: {Body}", messageBody);
    }

    private Task ProcessPaymentAsync(PaymentRequest payment) => Task.CompletedTask;
}

public class PaymentRequest
{
    public string OrderId { get; set; }
    public decimal Amount { get; set; }
    public string CustomerId { get; set; }
}
```

---

## Event Hub Trigger

```csharp
public class EventHubFunctions
{
    private readonly ILogger<EventHubFunctions> _logger;

    public EventHubFunctions(ILogger<EventHubFunctions> logger)
    {
        _logger = logger;
    }

    // Processes batches of events from Event Hub
    // Functions always receives events in BATCHES for efficiency
    [Function("ProcessTelemetry")]
    public async Task ProcessTelemetryAsync(
        [EventHubTrigger("telemetry-hub",
            Connection = "EventHubConnection",
            ConsumerGroup = "functions-consumer")]
        string[] eventBatch,                      // batch of event bodies
        PartitionContext partitionContext,         // partition metadata
        FunctionContext context)
    {
        _logger.LogInformation(
            "Processing {Count} events from partition {Partition}",
            eventBatch.Length,
            partitionContext.PartitionId);

        foreach (var eventData in eventBatch)
        {
            var telemetry = JsonSerializer.Deserialize<TelemetryEvent>(eventData);
            await ProcessTelemetryEventAsync(telemetry);
        }
    }

    // With full EventData objects for access to metadata
    [Function("ProcessTelemetryWithMetadata")]
    public async Task ProcessWithMetadataAsync(
        [EventHubTrigger("telemetry-hub",
            Connection = "EventHubConnection")]
        EventData[] events,                       // full EventData with properties
        FunctionContext context)
    {
        foreach (var evt in events)
        {
            var body = evt.EventBody.ToObjectFromJson<TelemetryEvent>();

            _logger.LogInformation(
                "Event from partition {Partition}, offset {Offset}, enqueued {EnqueuedTime}",
                evt.PartitionKey,
                evt.Offset,
                evt.EnqueuedTime);
        }
    }

    private Task ProcessTelemetryEventAsync(TelemetryEvent evt) => Task.CompletedTask;
}

public class TelemetryEvent
{
    public string DeviceId { get; set; }
    public double Temperature { get; set; }
    public DateTime Timestamp { get; set; }
}
```

---

## Dependency Injection and Configuration

Functions uses the same DI system as ASP.NET Core. Configuration comes from environment variables / app settings.

```csharp
// Program.cs — the host configuration entry point (Isolated Worker model)
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices((context, services) =>
    {
        // Register services exactly like ASP.NET Core
        services.AddSingleton<OrderRepository>();
        services.AddSingleton<CosmosClient>(sp =>
            new CosmosClient(
                context.Configuration["CosmosDBEndpoint"],
                new DefaultAzureCredential()));

        // HttpClient with typed client pattern
        services.AddHttpClient<PaymentGatewayClient>(client =>
        {
            client.BaseAddress = new Uri(context.Configuration["PaymentGatewayUrl"]);
        });

        // Application Insights integration
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();
    })
    .Build();

await host.RunAsync();
```

---

## Durable Functions

Durable Functions extends Azure Functions with **stateful, long-running workflows**. Regular functions are stateless and short-lived. Durable Functions lets you orchestrate sequences of function calls, fan out to parallel work, wait for external events, and handle timeouts — all without managing state yourself.

Three core function types:

**Orchestrator** — defines the workflow. Written with a special `IDurableOrchestrationContext` that looks sequential but actually checkpoints state after every `await`. Must be deterministic — no random numbers, no `DateTime.Now`, no direct I/O.

**Activity** — the actual work units. Called by the orchestrator. These can do I/O, call APIs, hit databases — anything. Each one is a regular function under the hood.

**Entity** — stateful actors, like tiny persistent objects. Less common but powerful for scenarios like counters, locks, or per-user state.

```csharp
// OrderProcessingOrchestration.cs
public class OrderOrchestration
{
    // -------------------------------------------------------
    // ORCHESTRATOR — defines the workflow
    // Must be deterministic, no direct I/O
    // -------------------------------------------------------
    [Function("ProcessOrderOrchestrator")]
    public static async Task<OrderResult> RunOrchestratorAsync(
        [OrchestrationTrigger] TaskOrchestrationContext context)
    {
        var order = context.GetInput<Order>();
        var logger = context.CreateReplaySafeLogger<OrderOrchestration>();

        logger.LogInformation("Starting order orchestration for {OrderId}", order.Id);

        try
        {
            // Step 1: Validate inventory (sequential)
            var inventoryResult = await context.CallActivityAsync<InventoryResult>(
                "CheckInventory", order);

            if (!inventoryResult.IsAvailable)
                return new OrderResult { Success = false, Reason = "Out of stock" };

            // Step 2: Fan out — charge payment AND send confirmation in parallel
            var paymentTask = context.CallActivityAsync<PaymentResult>(
                "ChargePayment", order);
            var notificationTask = context.CallActivityAsync<bool>(
                "SendOrderConfirmation", order);

            // Wait for BOTH to complete
            await Task.WhenAll(paymentTask, notificationTask);

            var payment = await paymentTask;
            if (!payment.Success)
                return new OrderResult { Success = false, Reason = "Payment failed" };

            // Step 3: Wait for an external event (e.g., warehouse confirmation)
            // With a timeout — if warehouse doesn't respond in 24 hours, cancel
            using var timeoutCts = new CancellationTokenSource();
            var warehouseEvent = context.WaitForExternalEvent<string>("WarehouseConfirmed");
            var timeout = context.CreateTimer(
                context.CurrentUtcDateTime.AddHours(24),
                timeoutCts.Token);

            var winner = await Task.WhenAny(warehouseEvent, timeout);

            if (winner == timeout)
            {
                await context.CallActivityAsync("CancelOrder", order);
                return new OrderResult { Success = false, Reason = "Warehouse timeout" };
            }

            timeoutCts.Cancel();  // cancel the timer since warehouse responded

            // Step 4: Ship the order
            await context.CallActivityAsync("ShipOrder", order);

            return new OrderResult { Success = true, OrderId = order.Id };
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Orchestration failed for order {OrderId}", order.Id);

            // Call a compensation activity to undo partial work
            await context.CallActivityAsync("CompensateOrder", order);
            throw;
        }
    }

    // -------------------------------------------------------
    // ACTIVITIES — the actual work, called by the orchestrator
    // These CAN do I/O, call APIs, etc.
    // -------------------------------------------------------
    [Function("CheckInventory")]
    public static async Task<InventoryResult> CheckInventoryAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Call real inventory service
        return new InventoryResult { IsAvailable = true, Quantity = 50 };
    }

    [Function("ChargePayment")]
    public static async Task<PaymentResult> ChargePaymentAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Call payment gateway
        return new PaymentResult { Success = true, TransactionId = Guid.NewGuid().ToString() };
    }

    [Function("SendOrderConfirmation")]
    public static async Task<bool> SendConfirmationAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Send email/SMS
        return true;
    }

    [Function("ShipOrder")]
    public static async Task ShipOrderAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Trigger shipping
    }

    [Function("CancelOrder")]
    public static async Task CancelOrderAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Reverse charges, update status
    }

    [Function("CompensateOrder")]
    public static async Task CompensateOrderAsync(
        [ActivityTrigger] Order order,
        FunctionContext context)
    {
        // Undo partial work
    }

    // -------------------------------------------------------
    // HTTP STARTER — kicks off the orchestration
    // Returns a management URL so client can poll for status
    // -------------------------------------------------------
    [Function("StartOrderProcessing")]
    public static async Task<HttpResponseData> StartAsync(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "orders/process")]
        HttpRequestData req,
        [DurableClient] DurableTaskClient client,
        FunctionContext context)
    {
        var order = await req.ReadFromJsonAsync<Order>();

        // Start the orchestration — returns an instance ID
        string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
            "ProcessOrderOrchestrator", order);

        // CreateCheckStatusResponse returns a payload with URLs the client
        // can use to poll status, send events, or terminate the orchestration
        return await client.CreateCheckStatusResponseAsync(req, instanceId);
    }

    // -------------------------------------------------------
    // RAISING EXTERNAL EVENTS — e.g., warehouse sends confirmation
    // -------------------------------------------------------
    [Function("WarehouseConfirm")]
    public static async Task<HttpResponseData> WarehouseConfirmAsync(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "warehouse/confirm/{instanceId}")]
        HttpRequestData req,
        string instanceId,
        [DurableClient] DurableTaskClient client,
        FunctionContext context)
    {
        // Send an event to a waiting orchestration instance
        await client.RaiseEventAsync(instanceId, "WarehouseConfirmed", "CONFIRMED");

        var response = req.CreateResponse(System.Net.HttpStatusCode.OK);
        await response.WriteAsJsonAsync(new { message = "Event raised" });
        return response;
    }
}

public class InventoryResult { public bool IsAvailable { get; set; } public int Quantity { get; set; } }
public class PaymentResult { public bool Success { get; set; } public string TransactionId { get; set; } }
public class OrderResult { public bool Success { get; set; } public string OrderId { get; set; } public string Reason { get; set; } }
```

### Durable Patterns to Know for the Exam

```csharp
// Pattern 1: Function Chaining (sequential steps)
var step1Result = await context.CallActivityAsync<string>("Step1", input);
var step2Result = await context.CallActivityAsync<string>("Step2", step1Result);
var step3Result = await context.CallActivityAsync<string>("Step3", step2Result);

// Pattern 2: Fan-Out / Fan-In (parallel work, then aggregate)
var tasks = Enumerable.Range(0, 10)
    .Select(i => context.CallActivityAsync<int>("ProcessChunk", i))
    .ToList();
var results = await Task.WhenAll(tasks);
var total = results.Sum();

// Pattern 3: Async HTTP (long-running job with polling)
// The HTTP starter + CreateCheckStatusResponse pattern above demonstrates this

// Pattern 4: Monitor (polling loop until condition met)
while (true)
{
    var status = await context.CallActivityAsync<string>("CheckJobStatus", jobId);
    if (status == "complete") break;

    // Wait before checking again — uses durable timers (not Thread.Sleep)
    var nextCheck = context.CurrentUtcDateTime.AddMinutes(5);
    await context.CreateTimer(nextCheck, CancellationToken.None);
}

// Pattern 5: Human Interaction (wait for approval with timeout)
var approvalTask = context.WaitForExternalEvent<bool>("ApprovalReceived");
var timeout = context.CreateTimer(context.CurrentUtcDateTime.AddDays(3), CancellationToken.None);
var winner = await Task.WhenAny(approvalTask, timeout);
bool approved = winner == approvalTask && await approvalTask;
```

---

## The Isolated Worker Model vs In-Process Model

For the exam know that there are two execution models for .NET functions:

**In-Process** — function runs in the same process as the Functions host. Tighter integration, slightly less overhead, but you're tied to the host's .NET version. Being phased out.

**Isolated Worker** (current standard) — function runs in a separate worker process. You control the .NET version independently of the host. Better for dependency isolation and future-proofing. This is what all the examples above use and what you should focus on.

---

## local.settings.json

For local development, connection strings and app settings go here. **Never commit this file to source control** — it contains real secrets locally.

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "CosmosDBConnection": "AccountEndpoint=https://...;AccountKey=...",
    "ServiceBusConnection": "Endpoint=sb://...;SharedAccessKeyName=...",
    "EventHubConnection": "Endpoint=sb://...;EntityPath=...",
    "CosmosDBEndpoint": "https://myaccount.documents.azure.com",
    "PaymentGatewayUrl": "https://payments.example.com"
  }
}
```

In production, these values come from **App Settings** on the Function App, or ideally from **Key Vault references** using managed identity — exactly the same pattern as App Service.

---

## Deployment

```bash
# Create a Function App
az functionapp create \
  --resource-group myRG \
  --consumption-plan-location eastus \
  --runtime dotnet-isolated \
  --runtime-version 8 \
  --functions-version 4 \
  --name myfunctionapp \
  --storage-account mystorageaccount

# Deploy using Azure Functions Core Tools
func azure functionapp publish myfunctionapp

# Or deploy a ZIP package via CLI
az functionapp deployment source config-zip \
  --resource-group myRG \
  --name myfunctionapp \
  --src ./publish.zip

# Enable managed identity on the Function App
az functionapp identity assign \
  --resource-group myRG \
  --name myfunctionapp

# Configure an app setting pointing to Key Vault
az functionapp config appsettings set \
  --resource-group myRG \
  --name myfunctionapp \
  --settings "CosmosDBConnection=@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/cosmos-connection/)"
```

---

## AZ-204 Exam Summary

The heaviest areas for Functions on the exam are the **three hosting plans and their differences** (Consumption/cold starts, Premium/pre-warmed, Dedicated/always-on), **triggers and bindings** and how they eliminate boilerplate connection code, the **authorization levels** for HTTP triggers (Anonymous, Function, Admin), how **Durable Functions** work and the five orchestration patterns (chaining, fan-out/fan-in, async HTTP, monitor, human interaction), the difference between **orchestrators and activities** (orchestrators must be deterministic, activities can do I/O), the **Isolated Worker vs In-Process** model distinction, and how **managed identity** integrates with Function App configuration via Key Vault references.

