# AZ-204: Connect to and Consume Azure Services & Third-Party Services

## Study Guide — Exam Weight: 15–20%

---

## 1. Azure API Management (APIM)

### Core Concepts

APIM sits between your API consumers (frontend apps, partners, developers) and your backend services. It acts as a **facade** — you can reshape requests/responses, enforce throttling, require subscriptions, and add caching without changing backend code.

**Three components:**
- **Gateway** — the runtime proxy that routes calls, enforces policies, and collects telemetry.
- **Management plane** — Azure portal / ARM API where you define APIs, products, policies.
- **Developer portal** — auto-generated site where consumers discover APIs, get keys, and test endpoints.

### Products & Subscriptions

A **Product** groups one or more APIs and has visibility rules (Open vs. Protected). Protected products require a **subscription key** sent via `Ocp-Apim-Subscription-Key` header (or query param). Know that subscription keys can be scoped to: All APIs, a single Product, or a single API.

### Policies — Exam Critical

Policies are XML fragments applied at four scopes: **Global → Product → API → Operation**. The `<base />` element controls where the parent scope's policies execute.

```xml
<policies>
  <inbound>
    <!-- Runs BEFORE backend call -->
    <base />
    <rate-limit calls="5" renewal-period="60" />
    <set-header name="X-Custom" exists-action="override">
      <value>hello</value>
    </set-header>
    <rewrite-uri template="/v2/{path}" />
  </inbound>
  <backend>
    <base />
    <!-- Can forward-request, set-backend-service, etc. -->
  </backend>
  <outbound>
    <!-- Runs AFTER backend responds -->
    <base />
    <set-header name="X-Powered-By" exists-action="delete" />
    <cache-store duration="3600" />
  </outbound>
  <on-error>
    <base />
    <!-- Runs if any policy or backend throws -->
  </on-error>
</policies>
```

**Must-know policies for the exam:**
- `rate-limit` / `rate-limit-by-key` — throttle by calls per period (returns 429)
- `quota` / `quota-by-key` — hard cap over longer period
- `cache-lookup` (inbound) / `cache-store` (outbound) — built-in response caching
- `validate-jwt` — validate OAuth 2.0 tokens (inbound)
- `set-backend-service` — dynamically route to different backends
- `retry` — retry backend calls on failure
- `send-request` — make a side call to another service from within a policy
- `return-response` — short-circuit and return immediately
- `set-body` — transform request/response body with Liquid templates or C# expressions
- `ip-filter` — allow/deny by IP range

**Policy expressions** use `@(context.Request.Headers.GetValueOrDefault("key",""))` C#-style syntax inside `@()`. The `context` object gives you access to Request, Response, User, Subscription, Operation, etc.

### Revisions vs. Versions

- **Revision** = non-breaking safe edit. Consumers still hit the current revision unless you swap. Good for testing changes before making them live.
- **Version** = breaking change. Exposes a new URL path (e.g., `/v2/`), header, or query param to differentiate.

### APIM Tiers to Know

| Tier | Gateway | Key Difference |
|------|---------|----------------|
| Consumption | Serverless | No dedicated infra, pay-per-call, cold start possible |
| Developer | Single unit | No SLA, for testing |
| Basic/Standard | Dedicated | Production, scaling units |
| Premium | Multi-region | VNet integration, multi-region |

**Exam trap:** Consumption tier does NOT support VNet integration or the built-in developer portal customization fully.

---

## 2. Event-Based Solutions

### Azure Event Grid

Event Grid is a **reactive, event-routing** service — ideal when you need to react to state changes. Think "something happened, react to it."

**Key model:**
- **Event Sources** — Azure services (Blob Storage, Resource Groups, Event Hubs, IoT Hub, custom apps)
- **Topics** — endpoints where events are sent
  - **System topics** — built-in for Azure services (e.g., Storage account blob created)
  - **Custom topics** — your own applications publish here
- **Event Subscriptions** — route events from a topic to a handler with optional filters
- **Event Handlers** — Azure Functions, Logic Apps, Webhooks, Event Hubs, Service Bus, Storage Queues

**Event Schema (CloudEvents 1.0 is the modern standard):**
```json
{
  "specversion": "1.0",
  "type": "com.myapp.order.created",
  "source": "/myapp/orders",
  "id": "unique-id",
  "time": "2025-01-15T10:00:00Z",
  "data": { "orderId": 123, "amount": 49.99 }
}
```

The older "Event Grid schema" is also still supported — know both exist.

**Filtering — exam favorite:**
- **Event type filtering** — subscribe only to `Microsoft.Storage.BlobCreated`
- **Subject filtering** — `subjectBeginsWith: "/blobServices/default/containers/images"` and `subjectEndsWith: ".jpg"`
- **Advanced filtering** — operators on data fields: `NumberGreaterThan`, `StringContains`, `IsNullOrUndefined`, etc.

**Delivery & Retry:**
- Default retry: 30 attempts over 24 hours with exponential backoff.
- **Dead-letter** destination (Blob Storage) for events that fail all retries.
- Event subscriptions require **endpoint validation** — for webhooks, Event Grid sends a validation event with a `validationCode`; your endpoint must echo it back (synchronous handshake) or follow the `validationUrl` (manual/async handshake).

**Batching:** Event Grid delivers events in arrays. Your handler should expect `[]` even for single events.

### Azure Event Hubs

Event Hubs is a **high-throughput event streaming** platform — think "big data ingestion pipeline." It is NOT a message queue; it's an append-only log.

**Core architecture:**
- **Namespace** → contains one or more Event Hubs
- **Event Hub** → has 1–32 partitions (Standard) or up to 2000 (Dedicated)
- **Partitions** → ordered, immutable sequences of events
- **Consumer Groups** → independent read views of the stream (like Kafka consumer groups)
- **Producers** → send events via AMQP 1.0, HTTPS, or Kafka protocol
- **Consumers** → read events via EventProcessorClient (SDK), AMQP, or Kafka

**Partition keys:** If you set a partition key on an event, Event Hubs hashes it to always route to the same partition. This guarantees ordering for events with the same key. Without a key, events round-robin across partitions.

**Capture:** Automatically writes raw events to Azure Blob Storage or Data Lake in Avro format. No code required — configure time window and size window.

**EventProcessorClient (exam critical):**
```python
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstorageblob import BlobCheckpointStore

checkpoint_store = BlobCheckpointStore.from_connection_string(
    blob_conn_str, container_name="checkpoints"
)
client = EventHubConsumerClient.from_connection_string(
    conn_str,
    consumer_group="$Default",
    eventhub_name="my-hub",
    checkpoint_store=checkpoint_store
)

async def on_event(partition_context, event):
    # Process the event
    print(event.body_as_str())
    # Checkpoint so we don't re-read on restart
    await partition_context.update_checkpoint(event)

client.receive(on_event=on_event, starting_position="-1")  # "-1" = beginning
```

**Key points:**
- Checkpointing stores the offset in Blob Storage — this is how consumers track progress and resume after failure.
- `$Default` consumer group always exists; create custom groups for independent consumers.
- Retention: default 1 day, up to 7 days (Standard) or 90 days (Dedicated).

### Event Grid vs. Event Hubs — Exam Comparison

| Dimension | Event Grid | Event Hubs |
|-----------|------------|------------|
| Pattern | Reactive (event notification) | Streaming (high-throughput ingestion) |
| Throughput | Millions of events/sec but small payloads | Millions of events/sec, large data volumes |
| Ordering | No guaranteed order | Ordered within a partition |
| Consumer model | Push to handlers | Pull (consumers read at own pace) |
| Retention | None (fire-and-forget + retry) | Time-based (1–90 days) |
| Use case | "Blob uploaded → trigger Function" | "Ingest 1M telemetry events/sec for analytics" |

---

## 3. Message-Based Solutions

### Azure Service Bus

Service Bus is an **enterprise message broker** with full queuing and pub/sub semantics. Think "guaranteed, ordered, transactional message delivery."

**Two models:**
- **Queues** — point-to-point. One sender, one receiver. First-In-First-Out (with sessions).
- **Topics & Subscriptions** — pub/sub. One sender, multiple independent subscribers each get a copy.

**Key features to know for exam:**

**Peek-Lock vs. Receive-and-Delete:**
- **Peek-Lock (default):** Message becomes invisible to other receivers. Receiver must call `Complete()`, `Abandon()`, `Defer()`, or `DeadLetter()`. If lock expires, message reappears.
- **Receive-and-Delete:** Message removed immediately on read. Simpler but no retry safety.

**Sessions (FIFO guarantee):**
Sessions group related messages with a `SessionId`. Only one receiver can hold a session lock at a time, guaranteeing ordered processing within that session. Exam loves this — if the question says "process in order," the answer usually involves sessions.

**Dead-Letter Queue (DLQ):**
Every queue/subscription has a DLQ. Messages land here after exceeding `MaxDeliveryCount`, TTL expiration, or explicit dead-lettering. You must read from the DLQ separately to inspect/fix failed messages.

**Duplicate Detection:**
Enable on queue creation. Uses `MessageId` within a configurable time window to silently discard duplicates.

**Scheduled Messages & Deferral:**
- `ScheduledEnqueueTimeUtc` — message won't appear until that time.
- `Defer()` — parks message; must be retrieved by sequence number later.

**Auto-forwarding:** Chain queues/subscriptions — messages automatically forward from one to another. Useful for fan-out patterns.

**Subscription filters (for Topics):**
- **SQL Filter:** `StoreId = 'Store1' AND Amount > 100`
- **Correlation Filter:** match on system or custom properties (more efficient than SQL)
- **Boolean Filter (TrueFilter/FalseFilter):** select all or none

**Code pattern — sending:**
```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage

with ServiceBusClient.from_connection_string(conn_str) as client:
    with client.get_queue_sender(queue_name="orders") as sender:
        message = ServiceBusMessage(
            body="Order data",
            session_id="customer-123",        # For session-enabled queues
            application_properties={"priority": "high"},
            subject="OrderCreated"
        )
        sender.send_messages(message)
```

**Code pattern — receiving with sessions:**
```python
with client.get_queue_receiver(queue_name="orders", session_id="customer-123") as receiver:
    for msg in receiver:
        print(str(msg))
        receiver.complete_message(msg)
```

### Azure Queue Storage

Queue Storage is the simpler, cheaper option — part of an Azure Storage account.

| Feature | Queue Storage | Service Bus |
|---------|--------------|-------------|
| Max message size | 64 KB | 256 KB (Standard) / 100 MB (Premium) |
| Max queue size | 500 TB | 1–80 GB |
| Ordering | No guarantee | FIFO (with sessions) |
| Duplicate detection | No | Yes |
| Transactions | No | Yes |
| Dead-lettering | No | Yes |
| Peek-lock | No (visibility timeout) | Yes |
| Protocol | REST/HTTP | AMQP, HTTP |

**When to choose Queue Storage:** Simple, high-volume, cost-sensitive workloads where you don't need ordering, transactions, or advanced routing. Also when you need > 80 GB queue.

**When to choose Service Bus:** Enterprise messaging, FIFO ordering, duplicate detection, transactions, pub/sub (topics), or integration with workflows.

### Choosing the Right Messaging Service — Decision Framework

```
Need to react to state changes (event-driven)?
  → Event Grid

Need high-throughput streaming / analytics pipeline?
  → Event Hubs

Need reliable message queue with ordering/transactions?
  → Service Bus

Need simple, cheap, high-volume queue?
  → Queue Storage
```

---

## 4. Microsoft Graph

Microsoft Graph is the unified REST API for Microsoft 365 data — users, mail, calendar, files, Teams, and more.

**Base URL:** `https://graph.microsoft.com/{version}/{resource}`
- `v1.0` — GA, stable
- `beta` — preview features, may change

**Authentication:** Always OAuth 2.0 via Microsoft Identity Platform.
- **Delegated permissions** — app acts on behalf of signed-in user.
- **Application permissions** — app acts as itself (daemon/background service). Requires admin consent.

**Common endpoints:**
```
GET /me                           → current user profile
GET /me/messages                  → current user's mail
GET /users/{id}/events            → user's calendar events
GET /groups/{id}/members          → group membership
POST /me/sendMail                 → send email
GET /me/drive/root/children       → OneDrive files
PATCH /me                         → update profile properties
```

**Query parameters (OData):**
- `$select=displayName,mail` — choose fields
- `$filter=department eq 'Engineering'` — filter
- `$orderby=displayName` — sort
- `$top=10` — limit results
- `$skip=10` — pagination offset
- `$expand=members` — include related entities inline
- `$count=true` — get total count
- `$search="displayName:Albert"` — search

**Pagination:** Large result sets return `@odata.nextLink` with a URL to get the next page. Keep following it until no more `nextLink`.

**Change notifications (webhooks):**
Subscribe to changes on a resource — e.g., get notified when a user's mail changes.

```json
POST /subscriptions
{
  "changeType": "created,updated",
  "notificationUrl": "https://myapp.com/api/notifications",
  "resource": "/me/messages",
  "expirationDateTime": "2025-01-20T00:00:00Z",
  "clientState": "my-secret-state"
}
```

Your webhook must respond with the `validationToken` on creation (similar to Event Grid). Subscriptions expire and must be renewed.

**Delta queries:** Instead of polling for all data, use `delta()` to get only changes since last call:
```
GET /users/delta
```
Returns a `@odata.deltaLink` — store and use it next time to get only changes.

**Batching:** Combine up to 20 requests in one HTTP call:
```json
POST /$batch
{
  "requests": [
    { "id": "1", "method": "GET", "url": "/me" },
    { "id": "2", "method": "GET", "url": "/me/messages?$top=5" }
  ]
}
```

**SDKs:** Microsoft Graph SDK (available for .NET, Python, JS) handles auth, retries, pagination. The exam tests awareness of the SDK pattern:
```csharp
var graphClient = new GraphServiceClient(credential);
var user = await graphClient.Me.GetAsync();
```

---

## 5. Exam-Critical Scenarios & Traps

### Scenario 1: "Events must be processed in order"
**Answer:** Service Bus with **Sessions** enabled. Set `SessionId` on messages. Event Hubs guarantees order within a partition (use partition key), but Service Bus Sessions is the typical exam answer for message queues.

### Scenario 2: "React when a blob is uploaded to storage"
**Answer:** Event Grid with a system topic for the Storage account, filtered to `BlobCreated` event type with subject filtering for the container/extension.

### Scenario 3: "Ingest millions of IoT telemetry events per second"
**Answer:** Event Hubs. Use partition keys for device-level ordering. Enable Capture to archive to Blob/Data Lake.

### Scenario 4: "Expose multiple backend microservices as a single API"
**Answer:** API Management. Import each service as an API, group under a Product, use policies for routing, auth, and transformation.

### Scenario 5: "Prevent duplicate message processing"
**Answer:** Service Bus with **duplicate detection** enabled (uses `MessageId`). For idempotent consumers, also consider implementing your own dedup logic.

### Scenario 6: "Need to rate-limit API calls by subscription"
**Answer:** APIM `rate-limit-by-key` policy in inbound, keyed on `context.Subscription.Id`.

### Scenario 7: "Validate JWT tokens before requests reach backend"
**Answer:** APIM `validate-jwt` policy in inbound. Specify issuer, audience, and required claims.

### Scenario 8: "Application needs to read all users' calendars without a signed-in user"
**Answer:** Microsoft Graph with **application permissions** (`Calendars.Read`), admin-consented, using client credentials flow.

### Scenario 9: "Get notified when a SharePoint list item changes"
**Answer:** Microsoft Graph **change notifications** (webhook subscription) on the list resource.

### Scenario 10: "Messages that fail processing should be isolated for investigation"
**Answer:** Service Bus **Dead-Letter Queue**. Messages exceeding `MaxDeliveryCount` auto-move to DLQ. Read from `{queue}/$deadletterqueue`.

---

## 6. Quick-Reference Cheat Sheet

| Service | Protocol | Max Message/Event Size | Ordering | Pattern |
|---------|----------|----------------------|----------|---------|
| Event Grid | HTTPS | 1 MB (per event), 1 MB batch | No | Push, reactive |
| Event Hubs | AMQP, HTTPS, Kafka | 1 MB (Standard), 1 MB (Dedicated batch) | Per partition | Stream, pull |
| Service Bus | AMQP, HTTPS | 256 KB (Std) / 100 MB (Premium) | FIFO with sessions | Queue / Pub-Sub |
| Queue Storage | REST/HTTPS | 64 KB | No | Simple queue |
| APIM | HTTPS | Depends on tier | N/A | API gateway |
| Microsoft Graph | HTTPS (REST) | N/A | N/A | Unified M365 API |

---

## 7. Hands-On Lab Ideas

1. **APIM + Function App:** Create an HTTP-triggered Azure Function, front it with APIM, add a `rate-limit` and `validate-jwt` policy. Test with Postman.

2. **Event Grid + Blob Storage:** Upload a blob → Event Grid fires → Azure Function logs the event. Add subject filtering for `.png` files only.

3. **Event Hubs + Checkpoint:** Send 100 events with partition keys, consume with `EventProcessorClient`, checkpoint every 10 events. Kill and restart the consumer to verify it resumes correctly.

4. **Service Bus Sessions:** Create a session-enabled queue. Send 3 messages with `SessionId="order-1"`. Receive in order using session receiver.

5. **Graph API Explorer:** Use [Graph Explorer](https://developer.microsoft.com/graph/graph-explorer) to query `/me`, `/me/messages`, and try `$filter`, `$select`, and `$top` parameters. Create a webhook subscription to your mail.

---

*Tip: Many exam questions in this section are scenario-based. The key differentiator is usually: Event Grid (react to state change) vs. Event Hubs (stream high-volume data) vs. Service Bus (enterprise queue with guarantees) vs. Queue Storage (simple & cheap). Know the policies for APIM cold and the Graph permission model (delegated vs. application).*
