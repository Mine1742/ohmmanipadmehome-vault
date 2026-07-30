
![[Pasted image 20260203085127.png]]

# Azure Table Storage & Cosmos DB

These two are closely related — Azure Table Storage is actually one of the APIs that Cosmos DB supports. Understanding both together, and how they relate, is important for the exam.

---

## Part 1: Azure Table Storage

### The Core Concept

Azure Table Storage is a **NoSQL key-value store** for structured, non-relational data. Think of it as a massive spreadsheet in the cloud — rows of data organized by keys, extremely cheap, infinitely scalable, but with very limited query capability compared to a relational database.

It's not a replacement for SQL. It's the right tool when you have huge volumes of simple structured data, you always know your keys, and you don't need complex joins or relationships.

---

### Data Model

Understanding the data model is critical because the entire performance and design story flows from it.

**Storage Account** — the top level container. Everything lives inside a storage account.

**Table** — a collection of entities. No schema enforced — different entities in the same table can have completely different properties.

**Entity** — equivalent to a row. Maximum 1 MB per entity. Can have up to 252 custom properties plus the 3 system properties below.

Every entity has exactly three system properties that together form its identity:

**PartitionKey** — groups entities into partitions. Entities with the same PartitionKey are stored together on the same storage node. This is your primary scaling and query optimization lever. Choose it carefully.

**RowKey** — uniquely identifies an entity within a partition. The combination of PartitionKey + RowKey must be globally unique within a table.

**Timestamp** — automatically maintained by Azure, records the last update time. You don't set this.

The combination of PartitionKey + RowKey is the **primary key**. The fastest possible query is a **point query** — looking up a single entity by both keys. The second fastest is a **range query** — filtering by PartitionKey and a range of RowKeys. The slowest is a **full table scan** — filtering only by properties other than the keys, which requires scanning all partitions.

This means **partition key design is everything** in Table Storage. Bad partition key design leads to hot partitions (all traffic hitting one node) and slow queries.

---

### Partition Key Design Patterns

**Good partition key choices:**

- Something you always filter by — user ID, device ID, tenant ID
- Something that distributes load evenly — avoid keys where one value dominates all traffic (e.g. if 90% of your data is for one customer, that customer's partition becomes a hot spot)

**Common patterns:**

- Store user events with `PartitionKey = userId`, `RowKey = timestamp` — lets you efficiently query all events for a user
- Store time-series data with `PartitionKey = deviceId`, `RowKey = DateTime.MaxValue.Ticks - DateTime.UtcNow.Ticks` — this reverse tick trick puts the newest data first in RowKey order, making "get latest N records" fast

---

### Working with Table Storage in .NET

```csharp
using Azure.Data.Tables;

// Connect to the table
var serviceClient = new TableServiceClient(
    new Uri("https://mystorageaccount.table.core.windows.net"),
    new DefaultAzureCredential());

var tableClient = serviceClient.GetTableClient("customers");
await tableClient.CreateIfNotExistsAsync();

// Define an entity
public class CustomerEntity : ITableEntity
{
    public string PartitionKey { get; set; }   // e.g. country code
    public string RowKey { get; set; }         // e.g. customer ID
    public DateTimeOffset? Timestamp { get; set; }
    public ETag ETag { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}

// Insert an entity
var customer = new CustomerEntity
{
    PartitionKey = "US",
    RowKey = "customer-001",
    Name = "John Smith",
    Email = "john@example.com"
};
await tableClient.AddEntityAsync(customer);

// Point query (fastest) - single entity by PK + RK
var result = await tableClient.GetEntityAsync<CustomerEntity>("US", "customer-001");

// Range query - all US customers
var usCustomers = tableClient.QueryAsync<CustomerEntity>(
    filter: TableClient.CreateQueryFilter($"PartitionKey eq 'US'"));

// Filter query (slower - scans within partition)
var filtered = tableClient.QueryAsync<CustomerEntity>(
    filter: TableClient.CreateQueryFilter($"PartitionKey eq 'US' and Name eq 'John Smith'"));
```

---

### Optimistic Concurrency with ETags

Table Storage uses **ETags** for optimistic concurrency. Every entity has an ETag that changes whenever the entity is updated. If you read an entity, then try to update it, but someone else updated it between your read and write, the ETag won't match and Azure will reject your update with a 412 Precondition Failed.

```csharp
// Read entity (captures current ETag)
var response = await tableClient.GetEntityAsync<CustomerEntity>("US", "customer-001");
var entity = response.Value;

// Modify it
entity.Email = "newemail@example.com";

// Update with ETag check - will fail if entity was modified since we read it
await tableClient.UpdateEntityAsync(entity, entity.ETag, TableUpdateMode.Replace);

// To skip concurrency check (last write wins), pass ETag.All
await tableClient.UpdateEntityAsync(entity, ETag.All, TableUpdateMode.Replace);
```

This is important for the exam — know what an ETag is, why it exists, and what happens when there's a conflict.

---

## Part 2: Cosmos DB

### The Core Concept

Cosmos DB is **Azure's globally distributed, multi-model NoSQL database**. It's the enterprise, planet-scale evolution of the same ideas behind Table Storage, but with dramatically more capability — multiple APIs, global distribution, multiple consistency models, and guaranteed SLAs on latency, throughput, and availability.

The headline promise: **single-digit millisecond reads and writes, globally, at any scale**.

---

### The API Models

This is one of the first things to understand about Cosmos DB — it's not one database, it's one engine that speaks **multiple database protocols**. You choose your API when you create your database, and that choice is permanent.

**NoSQL API (formerly Core/SQL API)** — the native Cosmos DB API. Stores JSON documents, queryable with a SQL-like syntax. This is what most new projects use and what AZ-204 focuses on most heavily.

**MongoDB API** — wire-compatible with MongoDB. Existing MongoDB applications can point at Cosmos DB with minimal code changes.

**Cassandra API** — wire-compatible with Apache Cassandra. Uses CQL (Cassandra Query Language).

**Table API** — wire-compatible with Azure Table Storage. Existing Table Storage apps can migrate to Cosmos DB for better performance, global distribution, and SLAs with minimal code changes. This is the bridge between the two halves of this topic.

**Gremlin API** — graph database API for modeling and traversing connected data (relationships, social networks, recommendation engines).

**PostgreSQL API** — distributed PostgreSQL using Citus for horizontally scaled relational workloads.

For AZ-204, the **NoSQL API** is the primary focus with awareness of the others.

---

### Core Concepts (NoSQL API)

**Account** — the top-level resource. Has a globally unique endpoint like `myaccount.documents.azure.com`.

**Database** — logical grouping of containers inside an account.

**Container** — where your data actually lives. Equivalent to a table in relational terms or a collection in MongoDB terms. This is also where you define your partition key and configure throughput.

**Item** — a single JSON document inside a container. No schema enforced — items in the same container can have different fields.

**Partition Key** — a field on your documents that Cosmos DB uses to physically distribute data across partitions. Just like Table Storage, this is the most important design decision you make.

---

### Throughput: RUs (Request Units)

Cosmos DB doesn't scale in terms of CPU or memory — it scales in **Request Units per second (RU/s)**. Every operation costs a certain number of RUs:

- A point read of a 1 KB item = **1 RU**
- A write = typically **5 RUs** (writes cost more than reads)
- A query = varies based on complexity, indexes, and data scanned

You provision RU/s at the database or container level and Cosmos DB guarantees you can sustain that throughput continuously. If you exceed your provisioned RU/s, requests get rate-limited (HTTP 429).

There are two throughput modes:

**Provisioned Throughput** — you specify RU/s and pay for them whether you use them or not. Predictable performance, predictable cost. Good for steady workloads.

**Serverless** — you pay only for the RUs you actually consume. No provisioning. Good for dev/test or spiky, unpredictable workloads.

**Autoscale** — you set a maximum RU/s and Cosmos DB scales between 10% of that max and the max automatically based on demand. You pay for the peak sustained in each hour. Good for variable but predictable production workloads.

---

### Partitioning in Cosmos DB

Cosmos DB automatically distributes your data across **physical partitions** behind the scenes. Each physical partition can hold up to 50 GB and 10,000 RU/s. As your data grows, Cosmos DB splits partitions automatically — you never manage this directly.

What you do manage is the **logical partition key** — the field in your documents that determines which logical partition an item belongs to. All items with the same partition key value live in the same logical partition, and a logical partition always stays on one physical partition.

```json
// Example: container partitioned by /customerId
{
  "id": "order-001",
  "customerId": "customer-123",   // <-- partition key
  "product": "Widget",
  "amount": 49.99,
  "status": "shipped"
}
```

**Good partition key characteristics:**

- High cardinality — many distinct values (userId, orderId, deviceId)
- Evenly distributed access — no single value dominates reads and writes
- Often included in your queries — so Cosmos DB can route to the right partition

**Synthetic partition keys** — when no single field makes a good key, you can combine fields: `"partitionKey": "US_2024-01"` (country + year-month). This creates a more distributed key from multiple lower-cardinality fields.

---

### Indexing

By default, Cosmos DB **indexes every property on every item automatically**. This means any field is queryable without you doing anything. The trade-off is that writes cost slightly more RUs because the index must be updated.

You can customize the indexing policy to exclude paths (reducing write cost for fields you never query) or include specific paths only.

```json
{
  "indexingMode": "consistent",
  "includedPaths": [
    { "path": "/customerId/?" },
    { "path": "/status/?" }
  ],
  "excludedPaths": [
    { "path": "/largePayload/*" },
    { "path": "/*" }
  ]
}
```

For the exam, know that indexing is automatic by default, that you can tune it, and that excluding high-write paths can significantly reduce RU costs.

---

### Consistency Levels

This is one of the most unique and heavily tested aspects of Cosmos DB. With global distribution comes the question: when you write data in East US and read it in West Europe, how fresh is the data you get back?

Cosmos DB offers **five consistency levels**, from strongest to weakest:

**Strong** — reads always return the most recent committed write. Every read is guaranteed to see the latest data. The trade-off is higher latency and reduced availability — reads must coordinate globally. Not available with multi-region writes.

**Bounded Staleness** — reads might lag behind writes, but only by a defined amount — either a maximum number of versions (K) or a maximum time interval (T) that you configure. Outside that window, it's consistent. Good for globally distributed apps that can tolerate slight staleness with predictable bounds.

**Session** — the default and most widely used. Within a single client session, reads are guaranteed to see your own writes. Different sessions might see slightly stale data. Balances consistency with performance well for most apps — your own writes are always visible to you.

**Consistent Prefix** — reads never see out-of-order writes. If writes happen in order A, B, C, you'll never read B without having read A first. But you might lag behind the latest write. Good for scenarios where order matters more than recency.

**Eventual** — no ordering guarantees. Highest availability and lowest latency. Reads may return stale or out-of-order data. Eventually all replicas converge. Good for non-critical data where performance and availability trump consistency (e.g. like counts, view counts).

A memory framework: think about what you're willing to sacrifice.

```
Strong          →  Never stale, but slower and less available
Bounded Staleness → Stale by a known amount
Session         →  Your own writes always visible (default, usually right choice)
Consistent Prefix → Ordered but potentially stale
Eventual        →  Fastest, highest availability, accept staleness
```

You set the default consistency level at the account level, and can relax it (go weaker) per request in code — but you can never strengthen it beyond the account default per request.

---

### Querying with the NoSQL API

Cosmos DB's NoSQL API uses a SQL-like syntax to query JSON documents.

```sql
-- Basic query
SELECT * FROM orders o WHERE o.status = "shipped"

-- Project specific fields
SELECT o.id, o.customerId, o.amount FROM orders o

-- Filter within partition (most efficient)
SELECT * FROM orders o 
WHERE o.customerId = "customer-123" AND o.status = "shipped"

-- Array operations
SELECT * FROM orders o WHERE ARRAY_CONTAINS(o.tags, "priority")

-- String functions
SELECT * FROM orders o WHERE STARTSWITH(o.customerId, "enterprise-")
```

Cross-partition queries (where you don't filter by partition key) are supported but more expensive — they fan out to all partitions and aggregate results. Always try to include the partition key in queries.

---

### Working with Cosmos DB in .NET

```csharp
using Microsoft.Azure.Cosmos;

// Connect
var client = new CosmosClient(
    accountEndpoint: "https://myaccount.documents.azure.com",
    tokenCredential: new DefaultAzureCredential());

var database = client.GetDatabase("mydb");
var container = database.GetContainer("orders");

// Define a model
public class Order
{
    [JsonProperty("id")]
    public string Id { get; set; }
    
    public string CustomerId { get; set; }   // partition key
    public string Product { get; set; }
    public decimal Amount { get; set; }
    public string Status { get; set; }
}

// Create an item
var order = new Order
{
    Id = Guid.NewGuid().ToString(),
    CustomerId = "customer-123",
    Product = "Widget",
    Amount = 49.99m,
    Status = "pending"
};
await container.CreateItemAsync(order, new PartitionKey(order.CustomerId));

// Point read (cheapest - 1 RU for 1KB item)
// Always provide both id AND partition key for a point read
var response = await container.ReadItemAsync<Order>(
    "order-id-here",
    new PartitionKey("customer-123"));
var fetchedOrder = response.Resource;

// Query
var query = new QueryDefinition(
    "SELECT * FROM orders o WHERE o.customerId = @customerId AND o.status = @status")
    .WithParameter("@customerId", "customer-123")
    .WithParameter("@status", "shipped");

var iterator = container.GetItemQueryIterator<Order>(query);
while (iterator.HasMoreResults)
{
    var page = await iterator.ReadNextAsync();
    foreach (var item in page)
    {
        Console.WriteLine($"Order: {item.Id}, Amount: {item.Amount}");
    }
}

// Upsert (insert or replace)
await container.UpsertItemAsync(order, new PartitionKey(order.CustomerId));

// Delete
await container.DeleteItemAsync<Order>("order-id-here", new PartitionKey("customer-123"));
```

---

### Change Feed

Change Feed is a **persistent, ordered log of every insert and update** to a Cosmos DB container. Deletes are not captured natively (though there's a soft-delete pattern). You can read the change feed to react to data changes in near real-time.

Common patterns:

- Trigger downstream processing when new orders arrive
- Sync data to a secondary store (search index, cache, data warehouse)
- Event sourcing and CQRS architectures
- Real-time analytics

Two ways to consume it:

**Change Feed Processor** — the recommended approach. A library that handles partition distribution, checkpointing, and scaling automatically across multiple consumers. Uses a separate "lease container" to track progress.

```csharp
var processor = container
    .GetChangeFeedProcessorBuilder<Order>("orderProcessor", HandleChangesAsync)
    .WithInstanceName("consumerInstance1")
    .WithLeaseContainer(leaseContainer)
    .Build();

await processor.StartAsync();

static async Task HandleChangesAsync(
    ChangeFeedProcessorContext context,
    IReadOnlyCollection<Order> changes,
    CancellationToken cancellationToken)
{
    foreach (var order in changes)
    {
        Console.WriteLine($"New/updated order: {order.Id}");
        // process the change...
    }
}
```

**Azure Functions Trigger** — there's a built-in Cosmos DB trigger for Azure Functions that fires your function whenever items change. Under the hood it uses the change feed processor. The simplest way to react to Cosmos DB changes without managing infrastructure.

---

### Global Distribution

One of Cosmos DB's flagship features. You can add read regions to your account and Cosmos DB transparently replicates your data to them. Your SDK automatically routes reads to the nearest region.

```bash
# Add a read region
az cosmosdb update \
  --resource-group myRG \
  --name myaccount \
  --locations regionName=eastus failoverPriority=0 isZoneRedundant=true \
                regionName=westeurope failoverPriority=1 isZoneRedundant=false \
                regionName=southeastasia failoverPriority=2 isZoneRedundant=false
```

**Automatic failover** — if your write region goes down, Cosmos DB automatically fails over to the next region in priority order. The SDK handles the reconnection.

**Multi-region writes** — with Premium, you can enable writes in multiple regions simultaneously. Every region accepts writes and Cosmos DB handles conflict resolution (using last-write-wins based on timestamp, or a custom conflict resolution policy you define). Note: Strong consistency is not available with multi-region writes.

---

### Stored Procedures, Triggers, and UDFs

Cosmos DB supports server-side JavaScript execution for cases where you need atomic operations across multiple items.

**Stored Procedures** — JavaScript functions that run atomically within a single partition. Can read and write multiple items in one transaction. The only way to get multi-item ACID transactions in Cosmos DB.

```javascript
// Server-side stored procedure
function createOrderWithInventoryCheck(order, inventory) {
    var context = getContext();
    var container = context.getCollection();
    
    // Check inventory (read)
    container.readDocument(inventoryLink, {}, function(err, inv) {
        if (inv.quantity < order.quantity) {
            throw new Error("Insufficient inventory");
        }
        // Create order and update inventory atomically
        container.createDocument(collLink, order, {}, function(err, doc) {
            // update inventory...
        });
    });
}
```

**Triggers** — pre- and post-triggers that fire before or after create/replace/delete operations. Must be explicitly invoked per request (not automatic).

**UDFs (User Defined Functions)** — custom JavaScript functions usable inside queries.

For the exam, the key point is that stored procedures are the only mechanism for **multi-document transactions** in Cosmos DB, and they are scoped to a **single partition**.

---

### Table Storage vs. Cosmos DB Table API

Since Cosmos DB has a Table API that's wire-compatible with Azure Table Storage, a natural question is: when do you use which?

||**Azure Table Storage**|**Cosmos DB Table API**|
|---|---|---|
|Cost|Much cheaper|More expensive|
|Latency|Variable, typically low|Guaranteed single-digit ms|
|Throughput|Scalable but no SLA|Guaranteed RU/s SLA|
|Global distribution|No|Yes|
|Secondary indexes|No|No|
|Query flexibility|Limited|Same as Table Storage|
|Migration effort|N/A|Minimal — SDK swap|

Choose Table Storage when cost is the primary concern and you don't need global distribution or guaranteed latency SLAs. Choose Cosmos DB Table API when you need those features and are willing to pay for them — especially useful when migrating an existing Table Storage app without rewriting business logic.

---

### When to Use What — Cosmos DB API Choice

|**Scenario**|**API to Choose**|
|---|---|
|New project, document data|NoSQL API|
|Existing MongoDB app|MongoDB API|
|Existing Cassandra app|Cassandra API|
|Existing Table Storage app|Table API|
|Graph / relationship data|Gremlin API|
|Distributed relational data|PostgreSQL API|

---

## AZ-204 Exam Summary

For **Table Storage**: know the data model cold (PartitionKey, RowKey, Timestamp), understand how to do point queries vs. range queries vs. table scans and their performance implications, know the .NET SDK classes (`TableClient`, `TableServiceClient`, `ITableEntity`), and understand ETag-based optimistic concurrency.

For **Cosmos DB**: the exam will focus heavily on the **consistency levels and their trade-offs**, **RU/s and the cost model** (what's a point read vs. a query), **partition key design principles**, the **NoSQL API query syntax**, how to use the **.NET SDK** for CRUD and queries, how **Change Feed** works and how to consume it, and the difference between the **available APIs** and when to use each.

# Azure Cosmos DB — AZ-204 Working Examples & Study Guide

---

## 1. Consistency Levels and Their Trade-Offs

Cosmos DB offers five consistency levels, ordered from strongest to weakest. The exam loves to test whether you understand what you're giving up and gaining at each level.

### The Five Levels

```
STRONG → BOUNDED STALENESS → SESSION → CONSISTENT PREFIX → EVENTUAL
 ←── Higher Latency, Lower Throughput ──→
 ←── Lower Latency, Higher Throughput ──→
```

**Strong** — Reads always return the most recent committed write. Linearizable. Only available in single-region accounts or multi-region accounts with single write region. Highest RU cost for reads.

**Bounded Staleness** — Reads may lag behind writes by at most _K_ versions or _T_ time interval (you configure both). Outside the write region, this behaves like Strong with a controlled delay. Inside the write region, it behaves like Session. Microsoft recommends this for multi-region accounts that need near-strong consistency.

**Session** — The default. Within a single client session (identified by a session token), reads are guaranteed to see that session's own writes, with monotonic reads and writes. Different sessions may see stale data. This is the sweet spot for most applications.

**Consistent Prefix** — Reads never see out-of-order writes. If writes happen in order A → B → C, a reader will see A, A→B, or A→B→C — never A→C without B. But reads can be stale. Think of it as "eventual but never scrambled."

**Eventual** — No ordering or freshness guarantee at all. Cheapest reads. Good for things like "like" counts or telemetry where staleness doesn't matter.

### Setting Consistency in Code

```csharp
// Account-level default (set in Azure portal or ARM/Bicep)
// But you can WEAKEN (never strengthen) per-request:

// Example: Account default is Session, weaken to Eventual for a bulk read
ItemRequestOptions options = new ItemRequestOptions
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};

ItemResponse<Product> response = await container.ReadItemAsync<Product>(
    id: "product-42",
    partitionKey: new PartitionKey("electronics"),
    requestOptions: options
);

// You can also weaken on queries:
QueryRequestOptions queryOptions = new QueryRequestOptions
{
    ConsistencyLevel = ConsistencyLevel.Eventual
};
```

### Exam Traps

- You can only **weaken** consistency per-request, never strengthen it. If the account is set to Session, you cannot request Strong on a single read.
- Strong consistency is **not available** for multi-region write (multi-master) accounts.
- Bounded Staleness in a **single region** behaves identically to Strong.
- Session consistency uses a **session token** — the SDK handles this automatically, but if you're passing requests between services, you need to propagate the token yourself.
- RU cost for reads: Strong and Bounded Staleness cost **2x** the RUs of the other levels (because they require a quorum read).

### Quick Decision Table

|Scenario|Best Consistency|
|---|---|
|Banking / financial transactions (single region)|Strong|
|Multi-region app needing strong-ish consistency|Bounded Staleness|
|Typical web app where users see their own writes|Session (default)|
|Dashboard showing aggregated stats|Consistent Prefix or Eventual|
|IoT telemetry ingestion|Eventual|

---

## 2. RU/s and the Cost Model

### What is an RU?

A **Request Unit (RU)** is a normalized measure of cost. 1 RU = the cost of a **point read** (ReadItemAsync) of a 1 KB document by its `id` and partition key. Everything else is measured relative to this baseline.

### Point Read vs. Query

```csharp
// === POINT READ — Cheapest possible operation ===
// You know the exact id AND partition key.
// Cost: ~1 RU for a 1 KB item. Scales linearly with item size.

ItemResponse<Product> response = await container.ReadItemAsync<Product>(
    id: "product-42",
    partitionKey: new PartitionKey("electronics")
);

// Check the actual RU charge:
Console.WriteLine($"Point read cost: {response.RequestCharge} RUs");
// Output: "Point read cost: 1 RUs" (for a ~1 KB document)


// === QUERY — More expensive, varies widely ===
// You're searching/filtering, Cosmos has to scan an index.

QueryDefinition query = new QueryDefinition(
    "SELECT * FROM products p WHERE p.category = @cat AND p.price > @price"
)
.WithParameter("@cat", "electronics")
.WithParameter("@price", 50);

FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(
    query,
    requestOptions: new QueryRequestOptions
    {
        PartitionKey = new PartitionKey("electronics"), // CRITICAL: scope to partition
        MaxItemCount = 50
    }
);

double totalRUs = 0;
while (iterator.HasMoreResults)
{
    FeedResponse<Product> page = await iterator.ReadNextAsync();
    totalRUs += page.RequestCharge;
    Console.WriteLine($"Page cost: {page.RequestCharge} RUs, Items: {page.Count}");
    foreach (Product p in page)
    {
        // process items
    }
}
Console.WriteLine($"Total query cost: {totalRUs} RUs");
// A targeted single-partition query might be 3-5 RUs
// A cross-partition query could be 50-500+ RUs
```

### What Makes Operations More Expensive?

|Factor|Impact on RU Cost|
|---|---|
|Item size (larger items)|Linear increase|
|Cross-partition query|Multiplied by number of partitions touched|
|Query without partition key|Fan-out to ALL partitions|
|High result count|More pages = more RUs|
|Complex filters (UDFs, etc.)|Higher compute cost|
|Strong / Bounded Staleness reads|2x the RU cost|
|Index-unfriendly queries|Much higher|
|Writes (create/replace/upsert)|~5-6x the cost of a point read for 1 KB|
|Deletes|~5-6x as well|

### Provisioned vs. Serverless vs. Autoscale

```
PROVISIONED (Manual)
├── You set: 400 RU/s (minimum) to unlimited
├── Billed: Per hour for provisioned amount, whether used or not
├── Best for: Predictable, steady workloads
└── Can set at DATABASE or CONTAINER level

AUTOSCALE
├── You set: Max RU/s (e.g., 4000 max)
├── Cosmos scales between 10% of max (400) and max (4000) automatically
├── Billed: Per hour for the HIGHEST RU/s used in that hour
├── Best for: Variable/spiky workloads
└── Minimum max = 1000 RU/s (so minimum floor = 100 RU/s)

SERVERLESS
├── You set: Nothing — purely pay-per-request
├── Billed: Per RU consumed
├── Best for: Dev/test, low-traffic, intermittent workloads
├── Max burst: 5000 RU/s
└── Limitations: Single region only, no geo-replication
```

### Exam Tip: Reading the RU Charge

Every response from the SDK includes the RU charge. The exam may ask you to identify how to capture it:

```csharp
// For single-item operations:
ItemResponse<Product> resp = await container.CreateItemAsync(product, partitionKey);
double cost = resp.RequestCharge;  // e.g., 6.29 RUs

// For queries (accumulate across pages):
double totalCost = 0;
FeedIterator<Product> iter = container.GetItemQueryIterator<Product>(queryDef);
while (iter.HasMoreResults)
{
    FeedResponse<Product> page = await iter.ReadNextAsync();
    totalCost += page.RequestCharge;
}

// For stored procedures:
StoredProcedureExecuteResponse<string> spResp =
    await container.Scripts.ExecuteStoredProcedureAsync<string>("mysproc", pk, params);
double spCost = spResp.RequestCharge;
```

---

## 3. Partition Key Design

### Principles

The partition key determines how your data is physically distributed. A **logical partition** is all items sharing the same partition key value. A **physical partition** is a server node that holds one or more logical partitions.

**The golden rules:**

1. **High cardinality** — Choose a key with many distinct values (thousands+). A key with only 3 values means only 3 logical partitions, creating hotspots.
2. **Even distribution** — Writes and storage should be spread evenly. If 80% of writes go to one partition key value, that partition becomes a bottleneck.
3. **Query alignment** — Your most frequent queries should include the partition key in the WHERE clause. This makes them single-partition queries (cheap and fast).
4. **Logical partition limit** — Each logical partition can hold max **20 GB**. If one partition key value accumulates more than 20 GB, you're stuck.

### Examples

```
SCENARIO: E-commerce orders
├── BAD key:  /country        → Low cardinality, huge US partition
├── BAD key:  /orderId        → Great distribution but every query is cross-partition
├── GOOD key: /customerId     → High cardinality, queries are per-customer
└── GOOD key: /customerId     → But if one customer has millions of orders... use hierarchical

SCENARIO: IoT sensor data
├── BAD key:  /sensorType     → Only a few types, hot partitions
├── GOOD key: /deviceId       → Each device writes to its own partition
└── ALSO OK:  /deviceId       → Combined with time-based containers for archival

SCENARIO: Multi-tenant SaaS
├── GOOD key: /tenantId       → Natural isolation per tenant
└── RISK:     One mega-tenant dominates → Consider synthetic key: /tenantId-shardId
```

### Hierarchical Partition Keys (Preview → GA)

For scenarios where a single key isn't enough:

```csharp
// Define up to 3 levels of partition key hierarchy
ContainerProperties containerProperties = new ContainerProperties
{
    Id = "orders",
    PartitionKeyPaths = new Collection<string> { "/tenantId", "/userId", "/orderDate" }
    // Level 1: tenantId   → groups all data for a tenant
    // Level 2: userId     → within a tenant, groups by user
    // Level 3: orderDate  → within a user, groups by date
};

// Create the container
Database database = cosmosClient.GetDatabase("mydb");
Container container = await database.CreateContainerAsync(containerProperties, throughput: 400);

// Write an item — the SDK extracts the hierarchical key automatically
Order order = new Order
{
    id = "order-001",
    tenantId = "contoso",
    userId = "user-42",
    orderDate = "2025-01-15",
    total = 99.95m
};

await container.CreateItemAsync(order,
    new PartitionKeyBuilder()
        .Add("contoso")
        .Add("user-42")
        .Add("2025-01-15")
        .Build()
);

// Query at any level of the hierarchy:
// Query all orders for a tenant (fans out within tenant's partitions only)
// Query all orders for a specific user within a tenant (even more targeted)
```

### Synthetic Partition Keys

When no single property provides good distribution:

```csharp
// Combine multiple properties into a synthetic key
public class SensorReading
{
    public string id { get; set; }
    public string deviceId { get; set; }
    public string readingType { get; set; }
    public double value { get; set; }

    // Synthetic partition key combines device + type
    public string partitionKey => $"{deviceId}-{readingType}";
}

// Or use a hash suffix to spread a hot key:
public string partitionKey => $"{tenantId}-{Math.Abs(id.GetHashCode()) % 10}";
// This creates 10 "sub-partitions" for each tenant
// Downside: queries for a tenant must fan out to all 10, or you filter client-side
```

---

## 4. NoSQL API Query Syntax

Cosmos DB's SQL-like query language operates on JSON documents. It looks like SQL but has important differences.

### Basic CRUD Queries

```sql
-- Select all properties
SELECT * FROM products p

-- Select specific properties (projection)
SELECT p.name, p.price, p.category FROM products p

-- Aliasing
SELECT p.name AS productName, p.price * 1.1 AS priceWithTax FROM products p

-- Filtering
SELECT * FROM products p
WHERE p.category = "electronics"
  AND p.price > 100
  AND p.inStock = true

-- Note: The alias after FROM (here "p") is arbitrary.
-- "products" doesn't need to match the container name — it's just an alias for the root.
-- These are all equivalent:
SELECT * FROM c WHERE c.price > 50
SELECT * FROM root r WHERE r.price > 50
SELECT * FROM anything a WHERE a.price > 50
```

### Working with Nested Objects and Arrays

```json
// Sample document:
{
    "id": "product-42",
    "name": "Wireless Mouse",
    "category": "electronics",
    "manufacturer": {
        "name": "Logitech",
        "country": "Switzerland"
    },
    "tags": ["wireless", "bluetooth", "ergonomic"],
    "variants": [
        { "color": "black", "price": 29.99, "stock": 150 },
        { "color": "white", "price": 34.99, "stock": 45 }
    ]
}
```

```sql
-- Nested property access (dot notation)
SELECT p.manufacturer.name AS maker, p.manufacturer.country
FROM products p
WHERE p.manufacturer.country = "Switzerland"

-- Check if array CONTAINS a value
SELECT * FROM products p
WHERE ARRAY_CONTAINS(p.tags, "bluetooth")

-- JOIN to "unwind" an array (like CROSS APPLY / UNNEST)
-- This produces one row per variant per product
SELECT p.name, v.color, v.price
FROM products p
JOIN v IN p.variants
WHERE v.price < 35

-- ARRAY_CONTAINS with an object (partial match)
SELECT * FROM products p
WHERE ARRAY_CONTAINS(p.variants, {"color": "black"}, true)
-- The third parameter 'true' enables partial matching

-- Subquery to filter array elements
SELECT p.name,
    ARRAY(SELECT VALUE v FROM v IN p.variants WHERE v.stock > 100) AS availableVariants
FROM products p
```

### Built-in Functions the Exam Tests

```sql
-- String functions
SELECT UPPER(p.name), LOWER(p.category), CONCAT(p.name, " - ", p.category)
FROM products p
WHERE CONTAINS(p.name, "Mouse")          -- case-sensitive substring
-- Also: STARTSWITH(), ENDSWITH(), LENGTH(), REPLACE(), SUBSTRING()

-- Math functions
SELECT p.name, ROUND(p.price * 1.08, 2) AS withTax
FROM products p
-- Also: ABS(), CEILING(), FLOOR(), POWER(), SQRT()

-- Type checking
SELECT * FROM products p
WHERE IS_DEFINED(p.discount)              -- property exists
  AND IS_NUMBER(p.discount)               -- and it's a number
  AND NOT IS_NULL(p.discount)             -- and it's not null
-- Also: IS_BOOL(), IS_STRING(), IS_ARRAY(), IS_OBJECT()

-- Aggregate functions
SELECT COUNT(1) AS total,
       AVG(p.price) AS avgPrice,
       MIN(p.price) AS cheapest,
       MAX(p.price) AS mostExpensive,
       SUM(p.price) AS totalValue
FROM products p
WHERE p.category = "electronics"

-- GROUP BY
SELECT p.category, COUNT(1) AS count, AVG(p.price) AS avgPrice
FROM products p
GROUP BY p.category

-- ORDER BY (requires a composite index if ordering by multiple fields)
SELECT * FROM products p
ORDER BY p.price DESC

-- OFFSET ... LIMIT (pagination)
SELECT * FROM products p
ORDER BY p.price
OFFSET 20 LIMIT 10

-- TOP
SELECT TOP 5 * FROM products p ORDER BY p.price DESC

-- DISTINCT
SELECT DISTINCT VALUE p.category FROM products p

-- VALUE keyword — returns raw values, not wrapped in objects
SELECT VALUE p.name FROM products p
-- Returns: ["Wireless Mouse", "Keyboard", ...] instead of [{"name": "Wireless Mouse"}, ...]

-- Ternary / conditional
SELECT p.name,
    (p.price > 100 ? "premium" : "standard") AS tier
FROM products p
```

### Parameterized Queries (how you SHOULD write them in the SDK)

```csharp
// Always use parameterized queries — never string concatenation
QueryDefinition query = new QueryDefinition(
    "SELECT * FROM products p WHERE p.category = @category AND p.price BETWEEN @min AND @max"
)
.WithParameter("@category", "electronics")
.WithParameter("@min", 10)
.WithParameter("@max", 100);

FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(query);
```

---

## 5. .NET SDK for CRUD and Queries

### Setup and Client Initialization

```csharp
using Microsoft.Azure.Cosmos;

// Recommended: Singleton CosmosClient for the app lifetime
// The SDK manages connections internally
CosmosClient client = new CosmosClient(
    accountEndpoint: "https://myaccount.documents.azure.com:443/",
    authKeyOrResourceToken: "your-primary-key",
    new CosmosClientOptions
    {
        ApplicationRegion = Regions.EastUS,          // Preferred region
        ConnectionMode = ConnectionMode.Direct,       // Direct = faster (default)
        // ConnectionMode = ConnectionMode.Gateway    // Gateway = goes through HTTPS gateway
        ConsistencyLevel = ConsistencyLevel.Session,  // Can weaken from account default
        MaxRetryAttemptsOnRateLimitedRequests = 9,    // Default
        MaxRetryWaitTimeOnRateLimitedRequests = TimeSpan.FromSeconds(30)
    }
);

Database database = client.GetDatabase("mydb");
Container container = database.GetContainer("products");
```

### Model Class

```csharp
using Newtonsoft.Json;  // Cosmos DB SDK v3 uses Newtonsoft by default

public class Product
{
    // "id" is required by Cosmos DB — always lowercase
    [JsonProperty("id")]
    public string Id { get; set; }

    [JsonProperty("category")]
    public string Category { get; set; }  // This is our partition key

    [JsonProperty("name")]
    public string Name { get; set; }

    [JsonProperty("price")]
    public decimal Price { get; set; }

    [JsonProperty("inStock")]
    public bool InStock { get; set; }

    [JsonProperty("tags")]
    public List<string> Tags { get; set; }

    // _etag is auto-managed by Cosmos for optimistic concurrency
    [JsonProperty("_etag")]
    public string ETag { get; set; }
}
```

### CREATE

```csharp
Product newProduct = new Product
{
    Id = Guid.NewGuid().ToString(),
    Category = "electronics",
    Name = "Wireless Keyboard",
    Price = 59.99m,
    InStock = true,
    Tags = new List<string> { "wireless", "bluetooth" }
};

// CreateItemAsync — fails with 409 Conflict if id+partition key already exists
ItemResponse<Product> createResponse = await container.CreateItemAsync(
    item: newProduct,
    partitionKey: new PartitionKey(newProduct.Category)
);

Console.WriteLine($"Created: {createResponse.Resource.Id}");
Console.WriteLine($"RU Cost: {createResponse.RequestCharge}");
Console.WriteLine($"Status:  {createResponse.StatusCode}");  // 201 Created
```

### READ (Point Read)

```csharp
// Point read — cheapest operation, ~1 RU for 1 KB
// Requires BOTH the id AND the partition key
try
{
    ItemResponse<Product> readResponse = await container.ReadItemAsync<Product>(
        id: "product-42",
        partitionKey: new PartitionKey("electronics")
    );

    Product product = readResponse.Resource;
    Console.WriteLine($"Read: {product.Name}, Cost: {readResponse.RequestCharge} RUs");
}
catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
{
    Console.WriteLine("Item not found");
}
```

### UPDATE (Replace with Optimistic Concurrency)

```csharp
// Read the item first to get the ETag
ItemResponse<Product> readResp = await container.ReadItemAsync<Product>(
    "product-42", new PartitionKey("electronics"));

Product product = readResp.Resource;
product.Price = 49.99m;  // Update the price

// Replace with ETag check (optimistic concurrency)
try
{
    ItemResponse<Product> replaceResponse = await container.ReplaceItemAsync(
        item: product,
        id: product.Id,
        partitionKey: new PartitionKey(product.Category),
        requestOptions: new ItemRequestOptions
        {
            IfMatchEtag = product.ETag  // Only succeeds if no one else modified it
        }
    );
    Console.WriteLine($"Updated. New ETag: {replaceResponse.ETag}");
}
catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.PreconditionFailed)
{
    Console.WriteLine("Conflict! Someone else modified the item. Re-read and retry.");
}
```

### UPSERT (Create or Replace)

```csharp
// UpsertItemAsync — creates if doesn't exist, replaces if it does
// No 409 conflict — always succeeds (unless there's a concurrency ETag check)
Product product = new Product
{
    Id = "product-42",
    Category = "electronics",
    Name = "Wireless Keyboard v2",
    Price = 54.99m,
    InStock = true,
    Tags = new List<string> { "wireless", "usb-c" }
};

ItemResponse<Product> upsertResponse = await container.UpsertItemAsync(
    item: product,
    partitionKey: new PartitionKey(product.Category)
);

// StatusCode is 200 (replaced) or 201 (created)
Console.WriteLine($"Upsert status: {upsertResponse.StatusCode}");
```

### DELETE

```csharp
// Delete requires id AND partition key
ItemResponse<Product> deleteResponse = await container.DeleteItemAsync<Product>(
    id: "product-42",
    partitionKey: new PartitionKey("electronics")
);
Console.WriteLine($"Deleted. Cost: {deleteResponse.RequestCharge} RUs");
// Status: 204 No Content
```

### QUERY (Full Pattern)

```csharp
// Parameterized query scoped to a partition
QueryDefinition queryDef = new QueryDefinition(
    "SELECT p.id, p.name, p.price FROM products p WHERE p.price > @minPrice ORDER BY p.price"
)
.WithParameter("@minPrice", 25.00);

FeedIterator<Product> iterator = container.GetItemQueryIterator<Product>(
    queryDef,
    requestOptions: new QueryRequestOptions
    {
        PartitionKey = new PartitionKey("electronics"),  // Single partition = cheaper
        MaxItemCount = 25  // Items per page (not a LIMIT — controls batch size)
    }
);

List<Product> results = new List<Product>();
double totalRUs = 0;

while (iterator.HasMoreResults)
{
    FeedResponse<Product> page = await iterator.ReadNextAsync();
    totalRUs += page.RequestCharge;
    results.AddRange(page);
}

Console.WriteLine($"Found {results.Count} items, total cost: {totalRUs} RUs");
```

### QUERY (Cross-Partition — More Expensive)

```csharp
// Omitting PartitionKey triggers a cross-partition fan-out query
FeedIterator<Product> crossPartIter = container.GetItemQueryIterator<Product>(
    new QueryDefinition("SELECT * FROM p WHERE p.price > 100"),
    requestOptions: new QueryRequestOptions
    {
        // No PartitionKey set — crosses ALL partitions
        MaxConcurrency = -1  // -1 = let the SDK parallelize fully
    }
);
```

### Transactional Batch (All-or-Nothing within a Partition)

```csharp
// TransactionalBatch — atomic operations within ONE logical partition
// All operations must target the SAME partition key
PartitionKey pk = new PartitionKey("electronics");

TransactionalBatch batch = container.CreateTransactionalBatch(pk)
    .CreateItem(new Product { Id = "p1", Category = "electronics", Name = "Mouse", Price = 25 })
    .CreateItem(new Product { Id = "p2", Category = "electronics", Name = "Pad", Price = 15 })
    .ReplaceItem("p3", updatedProduct)
    .DeleteItem("p4");

TransactionalBatchResponse batchResponse = await batch.ExecuteAsync();

if (batchResponse.IsSuccessStatusCode)
{
    Console.WriteLine($"Batch succeeded. Cost: {batchResponse.RequestCharge} RUs");
}
else
{
    Console.WriteLine($"Batch FAILED at operation index {batchResponse.ErrorMessage}");
    // ALL operations are rolled back
}
```

---

## 6. Change Feed

The Change Feed is a persistent, ordered log of all creates and updates (and optionally deletes) to items in a container. It's partition-key-scoped, ordered within each partition, and guaranteed to preserve the order of changes.

### Key Concepts

- Change Feed captures **inserts and updates** by default. With `AllVersionsAndDeletes` mode, it also captures deletes.
- It does NOT capture changes to TTL expirations (items silently vanishing).
- It's **per-partition ordered** — changes within a partition arrive in write order.
- Two consumption models: **Change Feed Processor** (recommended) and **pull model** (manual).

### Change Feed Processor (Recommended Pattern)

```csharp
// You need TWO containers:
// 1. "products" — the monitored container (your data)
// 2. "leases"   — the lease container (tracks progress/checkpoints)

Container monitoredContainer = client.GetContainer("mydb", "products");
Container leaseContainer = client.GetContainer("mydb", "leases");

// Build the processor
ChangeFeedProcessor processor = monitoredContainer
    .GetChangeFeedProcessorBuilder<Product>(
        processorName: "myProcessor",
        onChangesDelegate: HandleChangesAsync)
    .WithInstanceName("instance-1")            // Unique per host/instance
    .WithLeaseContainer(leaseContainer)
    .WithStartTime(DateTime.UtcNow)            // Or DateTime.MinValue for from-beginning
    // .WithMaxItems(100)                       // Optional: max items per batch
    // .WithPollInterval(TimeSpan.FromSeconds(5)) // Optional: polling frequency
    .Build();

// Start processing (runs in background)
await processor.StartAsync();

// ... your application runs ...

// Graceful shutdown
await processor.StopAsync();

// The delegate that handles each batch of changes:
static async Task HandleChangesAsync(
    ChangeFeedProcessorContext context,
    IReadOnlyCollection<Product> changes,
    CancellationToken cancellationToken)
{
    Console.WriteLine($"Partition: {context.LeaseToken}, Changes: {changes.Count}");

    foreach (Product item in changes)
    {
        Console.WriteLine($"  Changed: {item.Id} — {item.Name} — ${item.Price}");

        // Real-world patterns:
        // • Materialize a view in another container
        // • Send to Event Hub or Service Bus
        // • Update a search index
        // • Trigger notifications
        // • Replicate to another database
    }
}
```

### How the Lease Container Works

The lease container holds one document per physical partition of the monitored container. Each lease tracks:

- Which partition it's responsible for
- The continuation token (bookmark of where it left off)
- Which processor instance currently owns it

When you scale out (multiple instances with the same `processorName` but different `instanceName`), the processor automatically distributes partition leases across instances. If one instance goes down, another picks up its leases. This is how you get automatic load balancing and fault tolerance.

### AllVersionsAndDeletes Mode (Captures Deletes)

```csharp
// To also capture deletes, use AllVersionsAndDeletes mode
ChangeFeedProcessor processor = monitoredContainer
    .GetChangeFeedProcessorBuilder(
        processorName: "fullFeedProcessor",
        onChangesDelegate: HandleFullChangesAsync)
    .WithInstanceName("instance-1")
    .WithLeaseContainer(leaseContainer)
    .Build();

static async Task HandleFullChangesAsync(
    ChangeFeedProcessorContext context,
    IReadOnlyCollection<ChangeFeedItem<Product>> changes,
    CancellationToken cancellationToken)
{
    foreach (ChangeFeedItem<Product> change in changes)
    {
        // change.Metadata.OperationType: Created, Replaced, Deleted
        if (change.Metadata.OperationType == ChangeFeedOperationType.Delete)
        {
            Console.WriteLine($"DELETED: {change.Previous.Id}");
            // change.Previous has the item as it was before deletion
        }
        else
        {
            Console.WriteLine($"UPSERTED: {change.Current.Id}");
        }
    }
}
```

### Pull Model (Manual Control)

```csharp
// Pull model gives you manual control — useful for batch jobs or Azure Functions

// Get a feed iterator for a specific partition key range
FeedIterator<Product> feedIterator = container.GetChangeFeedIterator<Product>(
    ChangeFeedStartFrom.Beginning(),  // or .Now() or .ContinuationToken(token)
    ChangeFeedMode.Incremental        // or .AllVersionsAndDeletes
);

string continuationToken = null;

while (feedIterator.HasMoreResults)
{
    FeedResponse<Product> response = await feedIterator.ReadNextAsync();

    if (response.StatusCode == System.Net.HttpStatusCode.NotModified)
    {
        // No new changes — save the token and check back later
        continuationToken = response.ContinuationToken;
        await Task.Delay(TimeSpan.FromSeconds(30));
        continue;
    }

    foreach (Product item in response)
    {
        Console.WriteLine($"Changed: {item.Id}");
    }

    // Save continuation token to resume later
    continuationToken = response.ContinuationToken;
}

// Resume from where you left off:
FeedIterator<Product> resumeIterator = container.GetChangeFeedIterator<Product>(
    ChangeFeedStartFrom.ContinuationToken(continuationToken),
    ChangeFeedMode.Incremental
);
```

### Azure Functions Trigger (Serverless Consumption)

```csharp
// This is the simplest way to consume Change Feed — Azure handles the lease management
// Requires a "leases" container (same as Change Feed Processor)

[FunctionName("CosmosDBChangeFeed")]
public static void Run(
    [CosmosDBTrigger(
        databaseName: "mydb",
        containerName: "products",
        Connection = "CosmosDBConnection",         // App setting with connection string
        LeaseContainerName = "leases",
        CreateLeaseContainerIfNotExists = true)]
    IReadOnlyList<Product> changes,
    ILogger log)
{
    if (changes != null && changes.Count > 0)
    {
        log.LogInformation($"Documents modified: {changes.Count}");
        foreach (Product item in changes)
        {
            log.LogInformation($"Changed item: {item.Id}");
        }
    }
}
```

### Common Change Feed Patterns for the Exam

|Pattern|Description|
|---|---|
|**Materialized View**|Change Feed on Container A writes transformed data to Container B (different partition key, pre-joined, denormalized)|
|**Event Sourcing**|Every change is an event — Change Feed acts as the event stream|
|**Real-time Analytics**|Feed changes to Synapse, Event Hubs, or a data warehouse|
|**Cross-region Replication**|Feed changes to a container in another Cosmos account|
|**Cache Invalidation**|Invalidate Redis/CDN cache when source data changes|

---

## 7. Available APIs and When to Use Each

Cosmos DB is a multi-model database. The **API is chosen at account creation time and cannot be changed.** Each API determines the wire protocol, query language, and data model.

### API Comparison

**NoSQL API (Core API)** — The flagship. Native Cosmos DB API using JSON documents and SQL-like queries. Full access to all Cosmos DB features (Change Feed, stored procedures, triggers, UDFs, etc.). **Use this by default unless you have a specific reason not to.** This is what AZ-204 focuses on.

```
When to use:
• New greenfield applications
• When you want full Cosmos DB feature access
• Document/JSON data models
• When team knows SQL-like query syntax
```

**MongoDB API** — Wire-compatible with MongoDB. Existing MongoDB applications can connect to Cosmos DB by just changing the connection string. Uses BSON documents and MongoDB query syntax (`find()`, aggregation pipeline, etc.).

```
When to use:
• Migrating existing MongoDB applications
• Team has strong MongoDB expertise
• Using MongoDB drivers/tools/ecosystem
• Want MongoDB compatibility but with global distribution
Limitation: Not all MongoDB features are supported (check compatibility)
```

**Apache Cassandra API** — Wire-compatible with Cassandra. Uses CQL (Cassandra Query Language), tables with rows and columns, wide-column store model.

```
When to use:
• Migrating existing Cassandra workloads
• Wide-column data models (time-series, IoT)
• Team knows CQL
• Need Cassandra driver compatibility
```

**Apache Gremlin API** — Graph database API using the Gremlin traversal language. Stores vertices (nodes) and edges (relationships).

```
When to use:
• Social networks, recommendation engines
• Knowledge graphs, fraud detection
• Data with complex many-to-many relationships
• When relationships are as important as the data itself
```

**Table API** — Key-value store, wire-compatible with Azure Table Storage but with Cosmos DB's global distribution and SLAs. Simple key/value or key/attribute-value model.

```
When to use:
• Migrating from Azure Table Storage (drop-in replacement)
• Simple key-value lookups
• When you don't need complex queries
• Legacy apps using the Table Storage SDK
```

**PostgreSQL API (via Citus)** — Distributed PostgreSQL using the Citus engine. Full relational model with SQL, ACID transactions, joins, foreign keys. This is essentially Azure Cosmos DB for PostgreSQL.

```
When to use:
• Relational data that needs global scale
• Existing PostgreSQL applications
• Complex analytical queries (Citus columnar storage)
• Need JOINs and ACID transactions
Note: This runs on a different engine (Citus) — it's not a wire protocol over the core engine
```

### Quick Decision Flowchart for the Exam

```
Is this a new application with no existing database?
  └── YES → NoSQL API (default answer for AZ-204)

Are you migrating an existing application?
  ├── From MongoDB → MongoDB API
  ├── From Cassandra → Cassandra API
  ├── From Azure Table Storage → Table API
  ├── From PostgreSQL → PostgreSQL API
  └── From a graph DB → Gremlin API

Do you need graph traversals?
  └── YES → Gremlin API

Is it simple key-value with no complex queries?
  └── YES → Table API (or NoSQL API)
```

### Exam Traps

- **API is set at account creation** — you cannot switch APIs on an existing account.
- The NoSQL API is the only one with **full feature access** (stored procs, UDFs, pre/post triggers, etc.). Other APIs may have limited feature sets.
- The exam defaults to NoSQL API for all code examples. If they show `container.ReadItemAsync` or SQL-like queries, it's always NoSQL API.
- **PostgreSQL API** is architecturally different (Citus-based) from the other APIs which all run on the core Cosmos DB engine.
- MongoDB API items still have an internal `id` but it maps to MongoDB's `_id`.

---

## Quick Reference: Status Codes You'll See on the Exam

|Code|Meaning|Common Cause|
|---|---|---|
|200|OK|Successful read, replace, or upsert (existing)|
|201|Created|Successful create or upsert (new item)|
|204|No Content|Successful delete|
|400|Bad Request|Malformed query, invalid JSON, exceeds 2 MB item limit|
|403|Forbidden|Firewall rules blocking, or throughput exceeded without retry|
|404|Not Found|Item or container doesn't exist|
|409|Conflict|CreateItemAsync with duplicate id + partition key|
|412|Precondition Failed|ETag mismatch (optimistic concurrency)|
|429|Too Many Requests|RU/s budget exceeded — SDK auto-retries by default|
|449|Retry With|Transient concurrency conflict — SDK auto-retries|

---

## Common Exam Patterns Cheat Sheet

```
"Which consistency level should you use?"
→ If they mention "users see their own writes"          → Session
→ If they mention "multi-region + strong-ish"           → Bounded Staleness
→ If they mention "lowest latency, data can be stale"   → Eventual
→ If they mention "financial, must be latest"            → Strong

"How to reduce RU cost?"
→ Use point reads instead of queries
→ Add partition key to query WHERE clause
→ Reduce item size (remove unused properties)
→ Use Eventual consistency for reads that tolerate staleness
→ Create composite indexes for multi-field ORDER BY

"How to process changes in real-time?"
→ Change Feed Processor (SDK) or Azure Functions CosmosDB Trigger
→ Both require a lease container

"What partition key should you choose?"
→ High cardinality + even distribution + aligns with common queries
→ If they describe a tenant scenario → tenantId
→ If they describe user data → userId

"How to do atomic multi-item operations?"
→ TransactionalBatch (same partition key only)
→ Or stored procedures (same partition, JavaScript)
```


# Cosmos DB — Working Examples

Let me build this around a realistic scenario: an **e-commerce order management system**. This gives us natural data that illustrates every concept cleanly.

---

## Project Setup

First, create a console app and install the SDK:

```bash
dotnet new console -n CosmosDBDemo
cd CosmosDBDemo
dotnet add package Microsoft.Azure.Cosmos
dotnet add package Azure.Identity
```

---

## The Data Models

Everything in this guide uses these models:

```csharp
// Order.cs
using Newtonsoft.Json;

public class Order
{
    [JsonProperty("id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();

    [JsonProperty("customerId")]
    public string CustomerId { get; set; }       // This will be our partition key

    [JsonProperty("customerRegion")]
    public string CustomerRegion { get; set; }   // e.g. "US", "EU", "APAC"

    [JsonProperty("product")]
    public string Product { get; set; }

    [JsonProperty("quantity")]
    public int Quantity { get; set; }

    [JsonProperty("amount")]
    public decimal Amount { get; set; }

    [JsonProperty("status")]
    public string Status { get; set; }           // "pending", "shipped", "delivered"

    [JsonProperty("tags")]
    public List<string> Tags { get; set; } = new();

    [JsonProperty("createdAt")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    [JsonProperty("_etag")]                       // Cosmos DB sets this automatically
    public string ETag { get; set; }
}

public class Customer
{
    [JsonProperty("id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();

    [JsonProperty("customerId")]
    public string CustomerId { get; set; }

    [JsonProperty("name")]
    public string Name { get; set; }

    [JsonProperty("email")]
    public string Email { get; set; }

    [JsonProperty("tier")]
    public string Tier { get; set; }             // "standard", "premium", "enterprise"
}
```

---

## 1. Connecting and Setting Up

```csharp
// CosmosService.cs
using Microsoft.Azure.Cosmos;
using Azure.Identity;

public class CosmosService
{
    private readonly CosmosClient _client;
    private readonly Database _database;
    private Container _ordersContainer;
    private Container _leaseContainer;

    public CosmosService(string accountEndpoint)
    {
        // DefaultAzureCredential uses managed identity in Azure,
        // falls back to az login credentials locally.
        // No connection strings or keys to manage.
        _client = new CosmosClient(accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                // These are the regions to try for reads, in preference order
                ApplicationPreferredRegions = new[] { "East US", "West Europe" },

                // Serialize with camelCase to match our JsonProperty attributes
                SerializerOptions = new CosmosSerializationOptions
                {
                    PropertyNamingPolicy = CosmosPropertyNamingPolicy.CamelCase
                }
            });

        _database = _client.GetDatabase("ecommerce");
    }

    public async Task InitializeAsync()
    {
        // CreateIfNotExistsAsync is idempotent — safe to call every startup
        var dbResponse = await _client.CreateDatabaseIfNotExistsAsync("ecommerce");
        var db = dbResponse.Database;

        // Create orders container partitioned by /customerId
        // 400 RU/s is the minimum — fine for dev/test
        _ordersContainer = await db.CreateContainerIfNotExistsAsync(
            new ContainerProperties
            {
                Id = "orders",
                PartitionKeyPath = "/customerId",

                // Default TTL — set to -1 to enable TTL but not expire by default
                // Individual items can override this with a "ttl" property
                DefaultTimeToLive = -1,

                IndexingPolicy = new IndexingPolicy
                {
                    // Consistent means index is updated synchronously with writes
                    // (vs Lazy, which is async — cheaper but means queries may
                    // not see latest data immediately)
                    IndexingMode = IndexingMode.Consistent,

                    IncludedPaths =
                    {
                        new IncludedPath { Path = "/customerId/?" },
                        new IncludedPath { Path = "/status/?" },
                        new IncludedPath { Path = "/createdAt/?" }
                    },
                    ExcludedPaths =
                    {
                        // Exclude large fields we never query on to save write RUs
                        new ExcludedPath { Path = "/rawPayload/*" },
                        // Exclude everything else not listed above
                        new ExcludedPath { Path = "/*" }
                    }
                }
            },
            throughput: 400);

        // Lease container is required by Change Feed Processor
        _leaseContainer = await db.CreateContainerIfNotExistsAsync(
            new ContainerProperties("leases", "/id"), throughput: 400);

        Console.WriteLine("Cosmos DB initialized.");
    }
}
```

---

## 2. Partition Key Design — Three Scenarios

This is the most important design decision. Let me show you three real scenarios with the reasoning.

```csharp
// PartitionKeyDesign.cs — NOT production code, just illustration

public static class PartitionKeyExamples
{
    // -------------------------------------------------------
    // SCENARIO A: Good partition key — customerId
    // -------------------------------------------------------
    // Cardinality: potentially millions of customers
    // Access pattern: "get all orders for customer X" is the most common query
    // Distribution: as long as no single customer dominates, load is even
    //
    // Documents look like:
    // { "id": "order-001", "customerId": "cust-123", "product": "Widget" }
    // { "id": "order-002", "customerId": "cust-456", "product": "Gadget" }
    // { "id": "order-003", "customerId": "cust-123", "product": "Doohickey" }
    //
    // Query for a customer's orders stays within one partition — FAST, cheap.
    // -------------------------------------------------------


    // -------------------------------------------------------
    // SCENARIO B: Bad partition key — status
    // -------------------------------------------------------
    // Only 3-4 distinct values: "pending", "shipped", "delivered", "cancelled"
    // If you have 10 million orders, almost all go to "delivered"
    // That one partition becomes a HOT PARTITION — performance degrades
    // Azure starts throttling that partition even if others are idle
    //
    // Never use low-cardinality fields as partition keys
    // -------------------------------------------------------


    // -------------------------------------------------------
    // SCENARIO C: Synthetic partition key — when nothing is perfect
    // -------------------------------------------------------
    // Suppose you're storing IoT sensor readings.
    // deviceId alone: if one device is very active, hot partition
    // date alone: only 365 values per year, very low cardinality
    //
    // Solution: combine them into a synthetic key
    public static string BuildSyntheticKey(string deviceId, DateTime timestamp)
    {
        // e.g. "device-001_2024-03"
        // Now you have thousands of distinct values, distributed evenly
        // and queries like "all readings for device X in month Y" are efficient
        return $"{deviceId}_{timestamp:yyyy-MM}";
    }

    // The document would look like:
    // {
    //   "id": "reading-001",
    //   "partitionKey": "device-001_2024-03",   <-- synthetic
    //   "deviceId": "device-001",
    //   "timestamp": "2024-03-15T10:30:00Z",
    //   "temperature": 72.4
    // }
}
```

---

## 3. CRUD Operations with RU Cost Awareness

```csharp
// CrudOperations.cs
public class OrderRepository
{
    private readonly Container _container;

    public OrderRepository(Container container)
    {
        _container = container;
    }

    // -------------------------------------------------------
    // CREATE — costs ~5 RUs for a 1KB item (writes cost more than reads)
    // -------------------------------------------------------
    public async Task<Order> CreateOrderAsync(Order order)
    {
        var response = await _container.CreateItemAsync(
            order,
            new PartitionKey(order.CustomerId));

        // response.RequestCharge tells you exactly how many RUs this cost
        Console.WriteLine($"Create cost: {response.RequestCharge} RUs");
        // Typical output: "Create cost: 5.71 RUs"

        return response.Resource;
    }

    // -------------------------------------------------------
    // POINT READ — the cheapest operation, always 1 RU for a 1KB item
    // Requires BOTH id AND partition key
    // Goes directly to the right partition — no index lookup needed
    // -------------------------------------------------------
    public async Task<Order> GetOrderAsync(string orderId, string customerId)
    {
        try
        {
            var response = await _container.ReadItemAsync<Order>(
                orderId,
                new PartitionKey(customerId));

            Console.WriteLine($"Point read cost: {response.RequestCharge} RUs");
            // Typical output: "Point read cost: 1 RU"

            return response.Resource;
        }
        catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            // Always handle 404 — don't let it bubble up as an unhandled exception
            return null;
        }
    }

    // -------------------------------------------------------
    // QUERY — more expensive than point reads because it uses the index
    // Cost varies based on how many items are scanned and returned
    // -------------------------------------------------------

    // EFFICIENT: includes partition key — stays within one partition
    public async Task<List<Order>> GetOrdersByCustomerAsync(string customerId)
    {
        var query = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.customerId = @customerId")
            .WithParameter("@customerId", customerId);

        // QueryRequestOptions lets you scope the query to a single partition
        var options = new QueryRequestOptions
        {
            PartitionKey = new PartitionKey(customerId),
            MaxItemCount = 100   // controls page size
        };

        return await ExecuteQueryAsync<Order>(query, options);
    }

    // MODERATE: includes partition key + indexed field
    public async Task<List<Order>> GetPendingOrdersForCustomerAsync(string customerId)
    {
        var query = new QueryDefinition(
            @"SELECT o.id, o.product, o.amount, o.createdAt 
              FROM orders o 
              WHERE o.customerId = @customerId 
              AND o.status = @status
              ORDER BY o.createdAt DESC")
            .WithParameter("@customerId", customerId)
            .WithParameter("@status", "pending");

        Console.WriteLine("This query stays in one partition — efficient.");

        return await ExecuteQueryAsync<Order>(query,
            new QueryRequestOptions { PartitionKey = new PartitionKey(customerId) });
    }

    // EXPENSIVE: cross-partition query — fans out to ALL partitions
    // Use sparingly, usually for admin/reporting, not user-facing features
    public async Task<List<Order>> GetAllShippedOrdersAsync()
    {
        var query = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.status = 'shipped'");

        // No PartitionKey specified = cross-partition query
        // Cosmos DB contacts every partition and aggregates results
        Console.WriteLine("WARNING: Cross-partition query — will be expensive at scale.");

        return await ExecuteQueryAsync<Order>(query);
    }

    // -------------------------------------------------------
    // UPDATE — two patterns: Replace and Patch
    // -------------------------------------------------------

    // Replace: send the entire document (overwrites everything)
    // Cost: similar to a write (~5-10 RUs depending on size)
    public async Task<Order> UpdateOrderStatusAsync(string orderId,
        string customerId, string newStatus)
    {
        // First read the current item (1 RU)
        var current = await GetOrderAsync(orderId, customerId);
        if (current == null) return null;

        current.Status = newStatus;

        // Then replace it (5+ RUs)
        // Use the ETag for optimistic concurrency — if someone else updated
        // this item between our read and write, this will throw a 412
        var options = new ItemRequestOptions
        {
            IfMatchEtag = current.ETag
        };

        var response = await _container.ReplaceItemAsync(
            current, orderId, new PartitionKey(customerId), options);

        Console.WriteLine($"Replace cost: {response.RequestCharge} RUs");
        return response.Resource;
    }

    // Patch: send only the fields you want to change (more efficient for large docs)
    public async Task PatchOrderStatusAsync(string orderId, string customerId, string newStatus)
    {
        var patchOperations = new[]
        {
            PatchOperation.Set("/status", newStatus),
            PatchOperation.Set("/updatedAt", DateTime.UtcNow)
        };

        var response = await _container.PatchItemAsync<Order>(
            orderId,
            new PartitionKey(customerId),
            patchOperations);

        Console.WriteLine($"Patch cost: {response.RequestCharge} RUs");
    }

    // -------------------------------------------------------
    // UPSERT — insert if not exists, replace if exists
    // Useful when you don't know if an item exists
    // -------------------------------------------------------
    public async Task<Order> UpsertOrderAsync(Order order)
    {
        var response = await _container.UpsertItemAsync(
            order,
            new PartitionKey(order.CustomerId));

        Console.WriteLine($"Upsert cost: {response.RequestCharge} RUs");
        return response.Resource;
    }

    // -------------------------------------------------------
    // DELETE — typically 5-10 RUs
    // -------------------------------------------------------
    public async Task DeleteOrderAsync(string orderId, string customerId)
    {
        var response = await _container.DeleteItemAsync<Order>(
            orderId,
            new PartitionKey(customerId));

        Console.WriteLine($"Delete cost: {response.RequestCharge} RUs");
    }

    // -------------------------------------------------------
    // BATCH — multiple operations on the SAME partition key atomically
    // All succeed or all fail. Scoped to one partition.
    // -------------------------------------------------------
    public async Task CreateOrdersInBatchAsync(List<Order> orders)
    {
        // All orders MUST have the same CustomerId (same partition)
        var customerId = orders.First().CustomerId;
        if (orders.Any(o => o.CustomerId != customerId))
            throw new InvalidOperationException("Transactional batch requires same partition key.");

        var batch = _container.CreateTransactionalBatch(new PartitionKey(customerId));

        foreach (var order in orders)
            batch.CreateItem(order);

        using var response = await batch.ExecuteAsync();

        if (!response.IsSuccessStatusCode)
            throw new Exception($"Batch failed: {response.StatusCode}");

        Console.WriteLine($"Batch of {orders.Count} items cost: {response.RequestCharge} RUs");
    }

    // Helper for executing queries and collecting paginated results
    private async Task<List<T>> ExecuteQueryAsync<T>(
        QueryDefinition query,
        QueryRequestOptions options = null)
    {
        var results = new List<T>();
        double totalRUs = 0;

        using var iterator = _container.GetItemQueryIterator<T>(query, requestOptions: options);

        while (iterator.HasMoreResults)
        {
            var page = await iterator.ReadNextAsync();
            totalRUs += page.RequestCharge;
            results.AddRange(page);
        }

        Console.WriteLine($"Query returned {results.Count} items, cost: {totalRUs} RUs");
        return results;
    }
}
```

---

## 4. Consistency Levels — Demonstrating the Trade-offs

```csharp
// ConsistencyDemo.cs
public class ConsistencyDemo
{
    private readonly string _accountEndpoint;

    public ConsistencyDemo(string accountEndpoint)
    {
        _accountEndpoint = accountEndpoint;
    }

    // Each method creates a client with a different consistency level
    // to show how you'd set it up and when you'd use each

    // -------------------------------------------------------
    // STRONG — every read sees the latest write, guaranteed
    // Use case: financial transactions, inventory management
    // Trade-off: higher latency, unavailable during region failures,
    //            NOT compatible with multi-region writes
    // -------------------------------------------------------
    public CosmosClient CreateStrongConsistencyClient()
    {
        return new CosmosClient(_accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                ConsistencyLevel = ConsistencyLevel.Strong
            });
    }

    // -------------------------------------------------------
    // BOUNDED STALENESS — reads lag by at most K versions or T seconds
    // Use case: global leaderboards, social feeds where slight lag is ok
    //           but you want predictable bounds
    // Trade-off: slightly higher latency than Session, complex to configure
    // -------------------------------------------------------
    public CosmosClient CreateBoundedStalenessClient()
    {
        // Note: you configure K and T at the account level in the portal/CLI,
        // not in the SDK. The SDK just sets which level to use.
        return new CosmosClient(_accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                ConsistencyLevel = ConsistencyLevel.BoundedStaleness
            });
    }

    // -------------------------------------------------------
    // SESSION — default and most commonly appropriate
    // Your own writes are always visible to you within a session
    // Other users may see stale data briefly
    // Use case: shopping cart, user profile updates, most web apps
    // Trade-off: other sessions may briefly see old data
    // -------------------------------------------------------
    public async Task SessionConsistencyExampleAsync()
    {
        var client = new CosmosClient(_accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                ConsistencyLevel = ConsistencyLevel.Session
            });

        var container = client.GetDatabase("ecommerce").GetContainer("orders");

        // After writing, the session token ensures THIS client always
        // reads its own write, even across regions
        var order = new Order { CustomerId = "cust-123", Product = "Widget", Status = "pending" };
        var createResponse = await container.CreateItemAsync(order, new PartitionKey(order.CustomerId));

        // The session token travels with the client automatically
        // If you need to share it across service instances:
        string sessionToken = createResponse.Headers.Session;

        // Another instance can use this token to read at the same session level
        var readOptions = new ItemRequestOptions { SessionToken = sessionToken };
        var readResponse = await container.ReadItemAsync<Order>(
            order.Id,
            new PartitionKey(order.CustomerId),
            readOptions);

        Console.WriteLine($"Session read saw our write: {readResponse.Resource.Status}");
    }

    // -------------------------------------------------------
    // CONSISTENT PREFIX — reads never see out-of-order writes
    // Use case: event logs, audit trails where order matters more than recency
    // If events happen A→B→C, you'll never read B without having read A first
    // Trade-off: may lag behind latest write
    // -------------------------------------------------------
    public CosmosClient CreateConsistentPrefixClient()
    {
        return new CosmosClient(_accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                ConsistencyLevel = ConsistencyLevel.ConsistentPrefix
            });
    }

    // -------------------------------------------------------
    // EVENTUAL — maximum availability and performance, no ordering guarantee
    // Use case: "likes" counts, view counters, non-critical aggregations
    //           where you can tolerate stale or out-of-order reads
    // Trade-off: can read stale or out-of-order data
    // -------------------------------------------------------
    public CosmosClient CreateEventualConsistencyClient()
    {
        return new CosmosClient(_accountEndpoint, new DefaultAzureCredential(),
            new CosmosClientOptions
            {
                ConsistencyLevel = ConsistencyLevel.Eventual
            });
    }

    // -------------------------------------------------------
    // KEY RULE: you can WEAKEN consistency per-request
    // but never STRENGTHEN beyond the account default
    // -------------------------------------------------------
    public async Task WeakenConsistencyPerRequestAsync(Container container, string orderId, string customerId)
    {
        // Account is set to Session, but this read only needs Eventual
        // (e.g. displaying a non-critical count)
        var options = new ItemRequestOptions
        {
            ConsistencyLevel = ConsistencyLevel.Eventual  // weaker than Session = allowed
        };

        var response = await container.ReadItemAsync<Order>(
            orderId, new PartitionKey(customerId), options);

        // This would THROW — you can't request stronger than account default
        // var strongOptions = new ItemRequestOptions
        // {
        //     ConsistencyLevel = ConsistencyLevel.Strong  // stronger than Session = NOT allowed
        // };
    }
}
```

---

## 5. NoSQL API Query Syntax — Comprehensive Examples

```csharp
// QueryExamples.cs
public class QueryExamples
{
    private readonly Container _container;

    public QueryExamples(Container container)
    {
        _container = container;
    }

    public async Task RunAllExamplesAsync()
    {
        // -------------------------------------------------------
        // Basic SELECT
        // -------------------------------------------------------
        var allOrders = new QueryDefinition("SELECT * FROM orders");

        // Project only specific fields (cheaper — less data transferred = fewer RUs)
        var projected = new QueryDefinition(
            "SELECT o.id, o.customerId, o.status, o.amount FROM orders o");

        // -------------------------------------------------------
        // Filtering
        // -------------------------------------------------------
        var filtered = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.status = 'shipped' AND o.amount > 100");

        // Always use parameterized queries — prevents injection, better caching
        var parameterized = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.customerId = @cid AND o.status = @status")
            .WithParameter("@cid", "cust-123")
            .WithParameter("@status", "pending");

        // -------------------------------------------------------
        // Sorting and pagination
        // -------------------------------------------------------
        // ORDER BY requires a composite index if sorting on a different field
        // than the partition key
        var sorted = new QueryDefinition(
            @"SELECT * FROM orders o 
              WHERE o.customerId = @cid 
              ORDER BY o.createdAt DESC")
            .WithParameter("@cid", "cust-123");

        // For pagination use OFFSET / LIMIT
        var paged = new QueryDefinition(
            @"SELECT * FROM orders o 
              WHERE o.customerId = @cid 
              ORDER BY o.createdAt DESC
              OFFSET 20 LIMIT 10")       // page 3, 10 items per page
            .WithParameter("@cid", "cust-123");

        // -------------------------------------------------------
        // Array operations
        // -------------------------------------------------------
        // ARRAY_CONTAINS — check if array contains a value
        var taggedPriority = new QueryDefinition(
            "SELECT * FROM orders o WHERE ARRAY_CONTAINS(o.tags, 'priority')");

        // ARRAY_LENGTH
        var manyTags = new QueryDefinition(
            "SELECT * FROM orders o WHERE ARRAY_LENGTH(o.tags) > 2");

        // IN — matches any value in a list
        var multiStatus = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.status IN ('shipped', 'delivered')");

        // -------------------------------------------------------
        // String functions
        // -------------------------------------------------------
        var startsWith = new QueryDefinition(
            "SELECT * FROM orders o WHERE STARTSWITH(o.customerId, 'enterprise-')");

        var contains = new QueryDefinition(
            "SELECT * FROM orders o WHERE CONTAINS(o.product, 'Widget')");

        var upper = new QueryDefinition(
            "SELECT UPPER(o.product) AS productUpper FROM orders o WHERE o.customerId = @cid")
            .WithParameter("@cid", "cust-123");

        // -------------------------------------------------------
        // Aggregates — note: aggregates on cross-partition queries
        // are more expensive and require EnableCrossPartitionQuery
        // -------------------------------------------------------
        var count = new QueryDefinition(
            "SELECT VALUE COUNT(1) FROM orders o WHERE o.customerId = @cid")
            .WithParameter("@cid", "cust-123");

        var sum = new QueryDefinition(
            "SELECT VALUE SUM(o.amount) FROM orders o WHERE o.customerId = @cid")
            .WithParameter("@cid", "cust-123");

        var avg = new QueryDefinition(
            "SELECT VALUE AVG(o.amount) FROM orders o WHERE o.customerId = @cid")
            .WithParameter("@cid", "cust-123");

        // -------------------------------------------------------
        // EXISTS / subquery
        // -------------------------------------------------------
        // Find orders that have at least one tag
        var withTags = new QueryDefinition(
            @"SELECT * FROM orders o 
              WHERE EXISTS(
                SELECT VALUE t FROM t IN o.tags
              )");

        // -------------------------------------------------------
        // Type checking — useful when schema varies across items
        // -------------------------------------------------------
        var hasDiscount = new QueryDefinition(
            "SELECT * FROM orders o WHERE IS_DEFINED(o.discountCode) AND NOT IS_NULL(o.discountCode)");

        var numericAmounts = new QueryDefinition(
            "SELECT * FROM orders o WHERE IS_NUMBER(o.amount)");

        // -------------------------------------------------------
        // Date / time — stored as ISO 8601 strings, compared as strings
        // This works because ISO 8601 sorts lexicographically
        // -------------------------------------------------------
        var recentOrders = new QueryDefinition(
            @"SELECT * FROM orders o 
              WHERE o.customerId = @cid 
              AND o.createdAt >= @cutoff")
            .WithParameter("@cid", "cust-123")
            .WithParameter("@cutoff", DateTime.UtcNow.AddDays(-30).ToString("O"));

        // -------------------------------------------------------
        // Executing a query that returns a scalar (COUNT, SUM, etc.)
        // -------------------------------------------------------
        await ExecuteScalarQueryAsync(count, new PartitionKey("cust-123"));

        Console.WriteLine("All query examples compiled successfully.");
    }

    private async Task ExecuteScalarQueryAsync(QueryDefinition query, PartitionKey partitionKey)
    {
        var iterator = _container.GetItemQueryIterator<double>(query,
            requestOptions: new QueryRequestOptions { PartitionKey = partitionKey });

        double result = 0;
        double totalRUs = 0;

        while (iterator.HasMoreResults)
        {
            var page = await iterator.ReadNextAsync();
            totalRUs += page.RequestCharge;
            result = page.FirstOrDefault();
        }

        Console.WriteLine($"Scalar result: {result}, cost: {totalRUs} RUs");
    }
}
```

---

## 6. Change Feed — Two Consumption Patterns

### Pattern A: Change Feed Processor (for long-running services)

```csharp
// ChangeFeedProcessor.cs
public class OrderChangeFeedProcessor
{
    private readonly Container _ordersContainer;
    private readonly Container _leaseContainer;
    private ChangeFeedProcessor _processor;

    public OrderChangeFeedProcessor(Container ordersContainer, Container leaseContainer)
    {
        _ordersContainer = ordersContainer;
        _leaseContainer = leaseContainer;
    }

    public async Task StartAsync()
    {
        _processor = _ordersContainer
            .GetChangeFeedProcessorBuilder<Order>(
                processorName: "orderProcessor",      // unique name for this processor
                onChangesDelegate: HandleChangesAsync)
            .WithInstanceName("instance-1")           // unique per running instance
            .WithLeaseContainer(_leaseContainer)       // tracks progress per partition
            .WithStartTime(DateTime.UtcNow)            // only process changes from now
            // Alternatively: .WithStartTime(DateTime.MinValue) to read ALL history
            .WithPollInterval(TimeSpan.FromSeconds(5)) // how often to check for new changes
            .WithMaxItems(100)                         // max items per batch
            .Build();

        await _processor.StartAsync();
        Console.WriteLine("Change Feed Processor started.");
    }

    public async Task StopAsync()
    {
        await _processor.StopAsync();
        Console.WriteLine("Change Feed Processor stopped.");
    }

    // This is called whenever items change in the container
    // Changes arrive in batches, grouped by lease (logical partition range)
    private async Task HandleChangesAsync(
        ChangeFeedProcessorContext context,
        IReadOnlyCollection<Order> changes,
        CancellationToken cancellationToken)
    {
        Console.WriteLine($"Received {changes.Count} changes on lease {context.LeaseToken}");

        foreach (var order in changes)
        {
            // IMPORTANT: Change Feed does NOT tell you what changed
            // It gives you the full current state of the item
            // You don't know if this was an INSERT or UPDATE — you just get the item
            // You also don't get DELETEs (unless you implement soft delete)

            Console.WriteLine($"Changed order: {order.Id}, Status: {order.Status}");

            // Common patterns:
            switch (order.Status)
            {
                case "shipped":
                    await SendShipmentNotificationAsync(order, cancellationToken);
                    break;

                case "delivered":
                    await UpdateAnalyticsDashboardAsync(order, cancellationToken);
                    break;
            }
        }

        // Progress is automatically checkpointed in the lease container
        // If this instance crashes, another instance picks up from the last checkpoint
    }

    private Task SendShipmentNotificationAsync(Order order, CancellationToken ct)
    {
        Console.WriteLine($"[NOTIFICATION] Order {order.Id} shipped to customer {order.CustomerId}");
        return Task.CompletedTask;
    }

    private Task UpdateAnalyticsDashboardAsync(Order order, CancellationToken ct)
    {
        Console.WriteLine($"[ANALYTICS] Order {order.Id} delivered, amount: {order.Amount}");
        return Task.CompletedTask;
    }
}
```

### Pattern B: Azure Functions Trigger (for event-driven processing)

```csharp
// OrderChangeFeedFunction.cs
// This is in a separate Azure Functions project
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

public class OrderChangeFeedFunction
{
    private readonly ILogger<OrderChangeFeedFunction> _logger;

    public OrderChangeFeedFunction(ILogger<OrderChangeFeedFunction> logger)
    {
        _logger = logger;
    }

    [Function("ProcessOrderChanges")]
    public async Task Run(
        // CosmosDBTrigger fires whenever items change in the container
        [CosmosDBTrigger(
            databaseName: "ecommerce",
            containerName: "orders",
            Connection = "CosmosDBConnection",   // app setting with connection string
            LeaseContainerName = "leases",        // same lease container concept
            CreateLeaseContainerIfNotExists = true,
            FeedPollDelay = 5000)]                // milliseconds between polls
        IReadOnlyList<Order> changes,
        FunctionContext context)
    {
        if (changes == null || changes.Count == 0) return;

        _logger.LogInformation($"Processing {changes.Count} order changes");

        foreach (var order in changes)
        {
            _logger.LogInformation($"Order changed: {order.Id}, Status: {order.Status}");

            // Same pattern as the processor — you get full item state, not a diff
            // Handle accordingly
        }
    }
}
```

### Understanding the Lease Container

```csharp
// This is what the lease container looks like conceptually
// Azure manages this for you — you never write to it directly

// Each lease document tracks progress for one partition range:
// {
//   "id": "0",                           // partition range identifier
//   "LeaseToken": "0",
//   "ContinuationToken": "abc123...",    // where we left off
//   "Timestamp": "2024-03-15T10:30:00Z",
//   "Owner": "instance-1"               // which processor instance owns this lease
// }

// When you run multiple instances of your processor,
// they distribute the leases (partition ranges) among themselves.
// If one instance goes down, the others rebalance and pick up its leases.
// This is how Change Feed Processor scales horizontally.
```

---

## 7. API Comparison — When to Use Each

```csharp
// ApiComparison.cs — shows the same logical operation in different APIs
// to illustrate the differences for the exam

// -------------------------------------------------------
// NOSQL API (native, document-oriented, SQL-like queries)
// Use for: new projects, JSON document data, rich queries needed
// -------------------------------------------------------
public class NoSqlApiExample
{
    public async Task RunAsync(Container container)
    {
        // Rich SQL-like queries, JOIN on arrays, aggregates
        var query = new QueryDefinition(
            "SELECT * FROM orders o WHERE o.amount > @min ORDER BY o.createdAt DESC")
            .WithParameter("@min", 100);

        var iterator = container.GetItemQueryIterator<Order>(query);
        while (iterator.HasMoreResults)
        {
            var page = await iterator.ReadNextAsync();
            foreach (var item in page) Console.WriteLine(item.Id);
        }
    }
}

// -------------------------------------------------------
// TABLE API (wire-compatible with Azure Table Storage)
// Use for: migrating existing Table Storage apps to Cosmos DB
// Same SDK, just a different connection string
// -------------------------------------------------------
public class TableApiExample
{
    public async Task RunAsync()
    {
        // This is the SAME code you'd write for Azure Table Storage
        // Just point it at Cosmos DB's Table API endpoint
        var client = new TableClient(
            new Uri("https://myaccount.table.cosmos.azure.com"),
            "orders",
            new DefaultAzureCredential());

        // Exact same TableEntity model and operations
        // Your existing Table Storage code works here with minimal changes
        await client.CreateIfNotExistsAsync();

        var entity = new TableEntity("US", "customer-001")
        {
            { "Name", "John Smith" },
            { "Amount", 49.99 }
        };

        await client.AddEntityAsync(entity);
    }
}

// -------------------------------------------------------
// MONGODB API (wire-compatible with MongoDB 4.x)
// Use for: existing MongoDB apps moving to Azure
// Your existing MongoDB driver and queries work as-is
// -------------------------------------------------------
public class MongoApiExample
{
    public void Configure()
    {
        // Connection string uses MongoDB protocol but points at Cosmos DB
        // Everything else — queries, documents, indexes — works identically
        var connectionString = "mongodb://myaccount:key@myaccount.mongo.cosmos.azure.com:10255/" +
                               "?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000";

        // var client = new MongoClient(connectionString);
        // var db = client.GetDatabase("ecommerce");
        // var orders = db.GetCollection<Order>("orders");
        // await orders.InsertOneAsync(order);   // standard MongoDB driver code
        Console.WriteLine("MongoDB driver code works unchanged — just swap connection string.");
    }
}

// -------------------------------------------------------
// CASSANDRA API (wire-compatible with Cassandra)
// Use for: existing Cassandra apps, wide-column data patterns
// -------------------------------------------------------
public class CassandraApiExample
{
    public void QueryExample()
    {
        // Cassandra uses CQL (Cassandra Query Language)
        // Your existing CQL queries work against Cosmos DB's Cassandra API
        string cql = "SELECT * FROM ecommerce.orders WHERE customer_id = 'cust-123'";
        Console.WriteLine($"CQL query works as-is: {cql}");
    }
}

// -------------------------------------------------------
// GREMLIN API (graph database, for connected data)
// Use for: social networks, fraud detection, recommendation engines,
//          any data where relationships between entities matter as much as the entities
// -------------------------------------------------------
public class GremlinApiExample
{
    public void QueryExample()
    {
        // Gremlin is a graph traversal language
        // Data model: Vertices (nodes) + Edges (relationships)
        // e.g. Customer --[PURCHASED]--> Product
        //      Customer --[FRIENDS_WITH]--> Customer

        // Find all products purchased by friends of customer-123
        string gremlin = "g.V('customer-123').out('FRIENDS_WITH').out('PURCHASED').dedup()";
        Console.WriteLine($"Gremlin traversal: {gremlin}");

        // This type of query is extremely expensive in SQL (multiple JOINs)
        // but natural and efficient in a graph model
    }
}

// -------------------------------------------------------
// DECISION FRAMEWORK — which API to choose
// -------------------------------------------------------
public static class ApiDecisionGuide
{
    public static string ChooseApi(string scenario) => scenario switch
    {
        "new project"                    => "NoSQL API — native, most feature-rich",
        "existing mongodb app"           => "MongoDB API — minimal code changes",
        "existing cassandra app"         => "Cassandra API — minimal code changes",
        "existing table storage app"     => "Table API — drop-in replacement",
        "social network or graph data"   => "Gremlin API — relationships are first-class",
        "distributed postgresql"         => "PostgreSQL API — familiar SQL with scale",
        _                                => "NoSQL API — default choice for new workloads"
    };
}
```

---

## 8. Putting It All Together — Main Program

```csharp
// Program.cs
var endpoint = "https://myaccount.documents.azure.com";

var service = new CosmosService(endpoint);
await service.InitializeAsync();

var container = new CosmosClient(endpoint, new DefaultAzureCredential())
    .GetDatabase("ecommerce")
    .GetContainer("orders");

var repo = new OrderRepository(container);

// Create some orders
var order1 = await repo.CreateOrderAsync(new Order
{
    CustomerId = "cust-123",
    CustomerRegion = "US",
    Product = "Widget Pro",
    Quantity = 2,
    Amount = 149.99m,
    Status = "pending",
    Tags = new List<string> { "priority", "gift" }
});

var order2 = await repo.CreateOrderAsync(new Order
{
    CustomerId = "cust-123",
    Product = "Gadget Plus",
    Quantity = 1,
    Amount = 79.99m,
    Status = "shipped"
});

// Point read — cheapest
var fetched = await repo.GetOrderAsync(order1.Id, "cust-123");
Console.WriteLine($"Fetched: {fetched.Product}");

// Query within partition — efficient
var customerOrders = await repo.GetOrdersByCustomerAsync("cust-123");
Console.WriteLine($"Customer has {customerOrders.Count} orders");

// Update using patch — efficient for large documents
await repo.PatchOrderStatusAsync(order1.Id, "cust-123", "shipped");

// Start change feed in background
var processor = new OrderChangeFeedProcessor(
    container,
    new CosmosClient(endpoint, new DefaultAzureCredential())
        .GetDatabase("ecommerce").GetContainer("leases"));

await processor.StartAsync();

// Simulate some changes that the feed will pick up
await repo.PatchOrderStatusAsync(order2.Id, "cust-123", "delivered");

await Task.Delay(TimeSpan.FromSeconds(10)); // let the feed processor fire

await processor.StopAsync();
```

---

## RU Cost Cheat Sheet for the Exam

```
Operation                           Approx RU Cost
─────────────────────────────────────────────────
Point read (1KB item)               1 RU
Point read (10KB item)              ~1.3 RUs
Write / Create (1KB item)           ~5 RUs
Write / Create (10KB item)          ~10 RUs
Replace / Upsert                    similar to write
Delete                              ~5-10 RUs
Query (partition-scoped, simple)    ~2.5 RUs + per item
Query (cross-partition)             much higher, scales with partitions
Patch (small change)                less than full replace
```

The key insight for the exam: **reads are cheap, writes are ~5x more expensive, and cross-partition queries are the most costly**. Design your partition keys and queries to stay within a single partition for user-facing operations.
