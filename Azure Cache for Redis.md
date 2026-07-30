# Azure Cache for Redis

Think of Azure Cache for Redis as a **superfast, in-memory data store** that sits between your application and your slower data sources (databases, APIs, heavy computations). Instead of going to Cosmos DB or SQL Server every time a user requests the same data, your app checks Redis first. If the data is there, it comes back in microseconds. If not, you fetch it from the source, store it in Redis, and return it — so the next request is instant.

---

## The Core Problem It Solves

Every application has data that is:

- **Expensive to fetch** — requires a complex database query or an external API call
- **Read frequently** — the same data requested over and over
- **Doesn't change often** — product catalog, user profiles, configuration

Without caching, every request hits your database:

```
1000 users request the same product page
        │
        ▼ (1000 times)
Cosmos DB query — 20ms each
= 20 seconds of database work for data that didn't change
```

With Redis:

```
First request: Redis miss → fetch from Cosmos DB → store in Redis (20ms)
Requests 2-1000: Redis hit → return cached data (<1ms each)
= 999 requests served from memory at microsecond speed
```

This reduces database load, reduces latency, and dramatically improves throughput.

---

## What Redis Actually Is

Redis (Remote Dictionary Server) is an **in-memory key-value store**. Everything lives in RAM, which is why it's so fast. It supports several data structures beyond simple strings — which is what makes it useful for more than just basic caching.

Azure Cache for Redis is Microsoft's fully managed Redis service — you get Redis without managing servers, patching, or replication.

---

## Service Tiers

**Basic** — single node, no replication, no SLA. Dev/test only. Data lost if node restarts.

**Standard** — two nodes (primary + replica), automatic failover, SLA. Entry point for production.

**Premium** — Standard plus persistence (data survives restarts), clustering (shard across multiple nodes for scale), VNet integration, geo-replication. For high-scale production.

**Enterprise** — runs actual Redis Enterprise (not open-source Redis). Active geo-replication, higher performance, RediSearch and RedisBloom modules.

**Enterprise Flash** — same as Enterprise but uses NVMe SSD in addition to RAM for larger datasets at lower cost.

The exam focuses on **Basic, Standard, and Premium** — know that persistence and clustering are Premium-only, and that VNet integration requires Premium.

---

## Key Redis Data Structures

Redis isn't just a key-value store for strings — and the exam tests this. Each data structure has specific use cases.

**String** — the basic type. Stores any value up to 512MB. Used for simple caching, counters, session tokens.

**Hash** — a map of field-value pairs stored under one key. Perfect for representing an object (user profile, product) without serializing the entire thing to JSON.

**List** — ordered list of strings. Supports push/pop from both ends. Used for queues, activity feeds, recent items.

**Set** — unordered collection of unique strings. Used for tags, unique visitor tracking, "users who liked this."

**Sorted Set** — like a set but each member has a score. Members returned in score order. Perfect for leaderboards, priority queues, rate limiting.

**Bitmap** — compact bit array. Used for tracking boolean states per user at massive scale (did user X complete action Y?).

**HyperLogLog** — probabilistic cardinality estimation. "Approximately how many unique visitors have we had?" Uses minimal memory.

---

## .NET SDK — Core Operations

```bash
dotnet add package StackExchange.Redis
dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
```

### Connecting

```csharp
// RedisService.cs
using StackExchange.Redis;
using System.Text.Json;

public class RedisService : IDisposable
{
    private readonly ConnectionMultiplexer _connection;
    private readonly IDatabase _db;

    public RedisService(string connectionString)
    {
        // ConnectionMultiplexer is expensive to create — make it a singleton
        // Connection string format: hostname:port,password=...,ssl=true,abortConnect=false
        _connection = ConnectionMultiplexer.Connect(connectionString);
        _db = _connection.GetDatabase();
    }

    public void Dispose() => _connection.Dispose();
}
```

```csharp
// Program.cs — register as singleton in DI
builder.Services.AddSingleton<IConnectionMultiplexer>(sp =>
    ConnectionMultiplexer.Connect(
        builder.Configuration["RedisConnectionString"]));

// Or use the built-in IDistributedCache abstraction (simpler)
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration["RedisConnectionString"];
    options.InstanceName = "myapp:";   // prefix for all keys — prevents collisions
});
```

---

### String Operations — Basic Caching Pattern

```csharp
public class CacheService
{
    private readonly IDatabase _db;

    public CacheService(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // ─────────────────────────────────────
    // The Cache-Aside Pattern
    // The most common caching pattern — check cache, miss = load and store
    // ─────────────────────────────────────
    public async Task<Order> GetOrderAsync(string orderId, Func<Task<Order>> fetchFromDb)
    {
        string cacheKey = $"order:{orderId}";

        // 1. Check cache first
        RedisValue cached = await _db.StringGetAsync(cacheKey);

        if (cached.HasValue)
        {
            Console.WriteLine($"Cache HIT for {cacheKey}");
            return JsonSerializer.Deserialize<Order>(cached);
        }

        // 2. Cache miss — fetch from source
        Console.WriteLine($"Cache MISS for {cacheKey} — fetching from DB");
        var order = await fetchFromDb();

        if (order != null)
        {
            // 3. Store in cache with expiry
            // expiry prevents stale data from living forever
            await _db.StringSetAsync(
                cacheKey,
                JsonSerializer.Serialize(order),
                expiry: TimeSpan.FromMinutes(15));
        }

        return order;
    }

    // Simple set with expiry
    public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
    {
        var serialized = JsonSerializer.Serialize(value);
        await _db.StringSetAsync(key, serialized, expiry);
    }

    // Simple get
    public async Task<T> GetAsync<T>(string key)
    {
        var cached = await _db.StringGetAsync(key);
        if (!cached.HasValue) return default;
        return JsonSerializer.Deserialize<T>(cached);
    }

    // Delete a key (invalidate cache when data changes)
    public async Task InvalidateAsync(string key)
    {
        await _db.KeyDeleteAsync(key);
        Console.WriteLine($"Cache invalidated: {key}");
    }

    // Check existence
    public async Task<bool> ExistsAsync(string key)
        => await _db.KeyExistsAsync(key);

    // Get remaining TTL
    public async Task<TimeSpan?> GetTtlAsync(string key)
        => await _db.KeyTimeToLiveAsync(key);

    // ─────────────────────────────────────
    // Atomic counter — increment/decrement
    // Thread-safe — Redis is single-threaded internally
    // ─────────────────────────────────────
    public async Task<long> IncrementAsync(string key, long amount = 1)
        => await _db.StringIncrementAsync(key, amount);

    public async Task<long> DecrementAsync(string key, long amount = 1)
        => await _db.StringDecrementAsync(key, amount);

    // Example: track API call count per user
    public async Task<bool> CheckRateLimitAsync(string userId, int maxCallsPerMinute)
    {
        string key = $"ratelimit:{userId}:{DateTime.UtcNow:yyyyMMddHHmm}";

        // Increment and check atomically
        long count = await _db.StringIncrementAsync(key);

        if (count == 1)
        {
            // First call this minute — set expiry
            await _db.KeyExpireAsync(key, TimeSpan.FromMinutes(2));
        }

        return count <= maxCallsPerMinute;
    }
}
```

---

### Hash Operations — Storing Objects

```csharp
public class UserCacheService
{
    private readonly IDatabase _db;

    public UserCacheService(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // Hash stores individual fields — you can read/update one field
    // without deserializing the entire object
    public async Task SetUserAsync(User user)
    {
        string key = $"user:{user.Id}";

        // Store each property as a separate hash field
        await _db.HashSetAsync(key, new HashEntry[]
        {
            new("id",        user.Id),
            new("name",      user.Name),
            new("email",     user.Email),
            new("tier",      user.Tier),
            new("loginCount", user.LoginCount.ToString())
        });

        await _db.KeyExpireAsync(key, TimeSpan.FromHours(1));
    }

    public async Task<User> GetUserAsync(string userId)
    {
        string key = $"user:{userId}";
        var fields = await _db.HashGetAllAsync(key);

        if (fields.Length == 0) return null;

        var dict = fields.ToDictionary(
            f => f.Name.ToString(),
            f => f.Value.ToString());

        return new User
        {
            Id = dict["id"],
            Name = dict["name"],
            Email = dict["email"],
            Tier = dict["tier"],
            LoginCount = int.Parse(dict["loginCount"])
        };
    }

    // Read a single field — more efficient than reading the whole object
    public async Task<string> GetUserEmailAsync(string userId)
    {
        return await _db.HashGetAsync($"user:{userId}", "email");
    }

    // Update a single field without touching the rest
    public async Task UpdateUserTierAsync(string userId, string newTier)
    {
        await _db.HashSetAsync($"user:{userId}", "tier", newTier);
    }

    // Atomically increment a hash field
    public async Task<long> IncrementLoginCountAsync(string userId)
    {
        return await _db.HashIncrementAsync($"user:{userId}", "loginCount");
    }
}
```

---

### List Operations — Queues and Recent Items

```csharp
public class ActivityFeedService
{
    private readonly IDatabase _db;

    public ActivityFeedService(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // Recent activity feed — add to front, keep last 100
    public async Task AddActivityAsync(string userId, string activity)
    {
        string key = $"activity:{userId}";

        // LPUSH adds to the LEFT (front) of the list
        await _db.ListLeftPushAsync(key, activity);

        // Trim to keep only the 100 most recent items
        await _db.ListTrimAsync(key, 0, 99);

        await _db.KeyExpireAsync(key, TimeSpan.FromDays(7));
    }

    // Get recent activities (0 = first, -1 = last)
    public async Task<List<string>> GetRecentActivitiesAsync(
        string userId, int count = 20)
    {
        string key = $"activity:{userId}";
        var items = await _db.ListRangeAsync(key, 0, count - 1);
        return items.Select(i => i.ToString()).ToList();
    }

    // Use as a simple queue — push to right, pop from left (FIFO)
    public async Task EnqueueTaskAsync(string task)
    {
        await _db.ListRightPushAsync("task-queue", task);
    }

    public async Task<string> DequeueTaskAsync()
    {
        // LPOP removes and returns from the left
        RedisValue task = await _db.ListLeftPopAsync("task-queue");
        return task.HasValue ? task.ToString() : null;
    }

    // Blocking pop — waits up to timeout for a message (great for workers)
    public async Task<string> BlockingDequeueAsync(TimeSpan timeout)
    {
        var result = await _db.ListLeftPopAsync("task-queue");
        return result.HasValue ? result.ToString() : null;
    }
}
```

---

### Sorted Set — Leaderboards and Rate Limiting

```csharp
public class LeaderboardService
{
    private readonly IDatabase _db;
    private const string LeaderboardKey = "game:leaderboard";

    public LeaderboardService(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // Add or update a player's score
    public async Task SetScoreAsync(string playerId, double score)
    {
        await _db.SortedSetAddAsync(LeaderboardKey, playerId, score);
    }

    // Increment score (for games where you accumulate points)
    public async Task<double> AddScoreAsync(string playerId, double points)
    {
        return await _db.SortedSetIncrementAsync(LeaderboardKey, playerId, points);
    }

    // Get top N players (highest score first — descending order)
    public async Task<List<LeaderboardEntry>> GetTopPlayersAsync(int count = 10)
    {
        // WithScores returns both member and score
        var entries = await _db.SortedSetRangeByRankWithScoresAsync(
            LeaderboardKey,
            start: 0,
            stop: count - 1,
            order: Order.Descending);

        return entries.Select((e, index) => new LeaderboardEntry
        {
            Rank = index + 1,
            PlayerId = e.Element.ToString(),
            Score = e.Score
        }).ToList();
    }

    // Get a specific player's rank (0-based, so add 1 for display)
    public async Task<long?> GetPlayerRankAsync(string playerId)
    {
        long? rank = await _db.SortedSetRankAsync(
            LeaderboardKey, playerId, Order.Descending);

        return rank.HasValue ? rank + 1 : null;
    }

    // Get a player's score
    public async Task<double?> GetPlayerScoreAsync(string playerId)
    {
        return await _db.SortedSetScoreAsync(LeaderboardKey, playerId);
    }
}

public class LeaderboardEntry
{
    public int Rank { get; set; }
    public string PlayerId { get; set; }
    public double Score { get; set; }
}
```

---

### Set Operations — Unique Tracking

```csharp
public class UniqueTrackingService
{
    private readonly IDatabase _db;

    public UniqueTrackingService(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // Track unique visitors per page per day
    public async Task TrackVisitAsync(string pageId, string userId)
    {
        string key = $"visitors:{pageId}:{DateTime.UtcNow:yyyyMMdd}";
        await _db.SetAddAsync(key, userId);
        await _db.KeyExpireAsync(key, TimeSpan.FromDays(7));
    }

    // Count unique visitors
    public async Task<long> GetUniqueVisitorCountAsync(string pageId)
    {
        string key = $"visitors:{pageId}:{DateTime.UtcNow:yyyyMMdd}";
        return await _db.SetLengthAsync(key);
    }

    // Did a specific user visit?
    public async Task<bool> HasUserVisitedAsync(string pageId, string userId)
    {
        string key = $"visitors:{pageId}:{DateTime.UtcNow:yyyyMMdd}";
        return await _db.SetContainsAsync(key, userId);
    }

    // Tags — find products with multiple tags (intersection)
    public async Task TagProductAsync(string productId, params string[] tags)
    {
        foreach (var tag in tags)
            await _db.SetAddAsync($"tag:{tag}", productId);
    }

    // Products that have ALL specified tags
    public async Task<List<string>> GetProductsByTagsAsync(params string[] tags)
    {
        var tagKeys = tags.Select(t => new RedisKey($"tag:{t}")).ToArray();
        var intersection = await _db.SetCombineAsync(SetOperation.Intersect, tagKeys);
        return intersection.Select(v => v.ToString()).ToList();
    }
}
```

---

## IDistributedCache — The ASP.NET Core Abstraction

For simpler caching scenarios in ASP.NET Core, you don't need the full StackExchange.Redis API. The built-in `IDistributedCache` abstraction works with Redis and can be swapped for other backends (SQL Server, in-memory) without changing your code.

```csharp
// Using IDistributedCache — simpler but less feature-rich
public class ProductService
{
    private readonly IDistributedCache _cache;
    private readonly CosmosClient _cosmosClient;

    public ProductService(IDistributedCache cache, CosmosClient cosmosClient)
    {
        _cache = cache;
        _cosmosClient = cosmosClient;
    }

    public async Task<Product> GetProductAsync(string productId)
    {
        string cacheKey = $"product:{productId}";

        // Try cache first
        byte[] cachedBytes = await _cache.GetAsync(cacheKey);

        if (cachedBytes != null)
        {
            return JsonSerializer.Deserialize<Product>(cachedBytes);
        }

        // Cache miss — fetch from Cosmos DB
        var container = _cosmosClient.GetDatabase("catalog").GetContainer("products");
        var response = await container.ReadItemAsync<Product>(
            productId, new PartitionKey(productId));
        var product = response.Resource;

        // Store in cache
        var cacheOptions = new DistributedCacheEntryOptions
        {
            // AbsoluteExpirationRelativeToNow — cache for exactly this long
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(30),

            // SlidingExpiration — reset timer on each access
            // If nobody reads it for 10 minutes, expire it
            // Use one or the other, not both typically
            SlidingExpiration = TimeSpan.FromMinutes(10)
        };

        await _cache.SetAsync(
            cacheKey,
            JsonSerializer.SerializeToUtf8Bytes(product),
            cacheOptions);

        return product;
    }

    public async Task InvalidateProductAsync(string productId)
    {
        await _cache.RemoveAsync($"product:{productId}");
    }
}
```

---

## Transactions and Atomic Operations

Redis is single-threaded internally so individual commands are atomic. For multi-command atomicity, Redis provides transactions via `MULTI/EXEC` — in StackExchange.Redis, this is done via batches or the `CreateTransaction()` method.

```csharp
public class TransactionDemo
{
    private readonly IDatabase _db;

    public TransactionDemo(IConnectionMultiplexer redis)
    {
        _db = redis.GetDatabase();
    }

    // Transfer points between users atomically
    public async Task<bool> TransferPointsAsync(
        string fromUserId, string toUserId, int points)
    {
        string fromKey = $"points:{fromUserId}";
        string toKey = $"points:{toUserId}";

        // Check sender has enough points first
        var currentPoints = (int)await _db.StringGetAsync(fromKey);
        if (currentPoints < points) return false;

        // Create a transaction
        var transaction = _db.CreateTransaction();

        // Add condition — transaction aborts if fromKey changes
        // between the check above and the execution below (optimistic concurrency)
        transaction.AddCondition(Condition.StringEqual(fromKey, currentPoints.ToString()));

        // Queue the operations — not executed yet
        _ = transaction.StringDecrementAsync(fromKey, points);
        _ = transaction.StringIncrementAsync(toKey, points);

        // Execute atomically — returns false if condition failed
        bool committed = await transaction.ExecuteAsync();
        Console.WriteLine(committed ? "Transfer succeeded" : "Transfer failed — retry");
        return committed;
    }

    // Using a Lua script for complex atomic operations
    // Lua scripts run atomically in Redis
    public async Task<bool> AtomicCheckAndSetAsync(
        string key, string expectedValue, string newValue)
    {
        const string luaScript = @"
            if redis.call('GET', KEYS[1]) == ARGV[1] then
                redis.call('SET', KEYS[1], ARGV[2])
                return 1
            else
                return 0
            end";

        var result = await _db.ScriptEvaluateAsync(
            luaScript,
            new RedisKey[] { key },
            new RedisValue[] { expectedValue, newValue });

        return (int)result == 1;
    }
}
```

---

## Pub/Sub — Messaging with Redis

Redis has a built-in publish/subscribe system — lightweight, not persistent (unlike Service Bus), but very fast for real-time notifications.

```csharp
public class RedisPubSubDemo
{
    private readonly IConnectionMultiplexer _redis;

    public RedisPubSubDemo(IConnectionMultiplexer redis)
    {
        _redis = redis;
    }

    // Publisher — broadcast a message to all subscribers on a channel
    public async Task PublishAsync(string channel, string message)
    {
        var subscriber = _redis.GetSubscriber();
        long receivers = await subscriber.PublishAsync(channel, message);
        Console.WriteLine($"Published to {receivers} subscribers on '{channel}'");
    }

    // Subscriber — listen for messages on a channel
    public async Task SubscribeAsync(string channel)
    {
        var subscriber = _redis.GetSubscriber();

        await subscriber.SubscribeAsync(channel, (ch, message) =>
        {
            Console.WriteLine($"[{ch}] Received: {message}");
            // Handle the message — update UI, trigger processing, etc.
        });

        Console.WriteLine($"Subscribed to '{channel}'");
    }

    // Pattern subscription — subscribe to multiple channels matching a pattern
    public async Task SubscribeToPatternAsync()
    {
        var subscriber = _redis.GetSubscriber();

        // Matches order:created, order:shipped, order:delivered
        await subscriber.SubscribeAsync("order:*", (channel, message) =>
        {
            Console.WriteLine($"Order event on [{channel}]: {message}");
        });
    }
}
```

---

## Persistence — Premium Tier Feature

By default Redis is purely in-memory — restart the server and data is gone. Premium tier adds two persistence options:

**RDB (Redis Database Backup)** — periodic snapshots of the dataset to disk. On restart, loads the last snapshot. Some data loss possible (since last snapshot).

**AOF (Append Only File)** — logs every write operation. On restart, replays the log. Less data loss but slower and larger files.

```bash
# Enable RDB persistence when creating cache
az redis create \
  --resource-group myRG \
  --name myrediscache \
  --sku Premium \
  --vm-size P1 \
  --redis-configuration '{"rdb-backup-enabled": "true",
                          "rdb-backup-frequency": "60",
                          "rdb-storage-connection-string": "<storage-connection-string>"}'
```

---

## Eviction Policies

When Redis runs out of memory it needs to decide what to evict. The policy you choose matters for your use case.

**noeviction** — return error when memory is full. Never evict. Use when data loss is unacceptable.

**allkeys-lru** — evict the least recently used key from all keys. Good general-purpose choice for caches.

**volatile-lru** — evict least recently used keys that have an expiry set. Protects keys without expiry.

**allkeys-lfu** — evict least frequently used keys. Better than LRU for skewed access patterns.

**volatile-ttl** — evict keys with the shortest remaining TTL first.

**allkeys-random** — evict random keys. Rarely the right choice.

For most caching scenarios `allkeys-lru` is the right default — when full, Redis evicts whatever was used least recently, which is the data least likely to be needed again.

```bash
az redis update \
  --resource-group myRG \
  --name myrediscache \
  --redis-configuration '{"maxmemory-policy": "allkeys-lru"}'
```

---

## Key Design — Naming Conventions

Redis keys are just strings but naming them well is critical for maintainability and avoiding collisions.

```
Convention: object-type:id:field
Examples:
  user:123                    → user object
  user:123:orders             → orders for user 123
  order:456                   → order object
  order:456:items             → items in order 456
  product:789:inventory       → inventory for product
  session:abc123xyz           → session token
  ratelimit:user:123:2024031510  → rate limit for user per hour
  leaderboard:game:weekly     → weekly leaderboard
```

Always prefix keys when using `IDistributedCache` with `InstanceName` to prevent collisions if multiple apps share a Redis instance.

---

## Connecting App Service / Functions to Redis

```bash
# Create the cache
az redis create \
  --resource-group myRG \
  --name myrediscache \
  --location eastus \
  --sku Standard \
  --vm-size C1

# Get the connection string
az redis list-keys \
  --resource-group myRG \
  --name myrediscache

# Store in Key Vault (never in app settings directly)
az keyvault secret set \
  --vault-name mykeyvault \
  --name "RedisConnectionString" \
  --value "myrediscache.redis.cache.windows.net:6380,password=<key>,ssl=True,abortConnect=False"

# Reference from App Service via Key Vault reference
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings "RedisConnectionString=@Microsoft.KeyVault(VaultName=mykeyvault;SecretName=RedisConnectionString)"
```

---

## Common Caching Patterns — Summary

The exam may present scenarios and ask you to identify the right pattern:

**Cache-Aside (Lazy Loading)** — application checks cache first, loads from DB on miss and populates cache. Most common pattern. Data only cached when actually needed.

**Write-Through** — write to cache and database simultaneously on every update. Cache always current but slower writes. No stale data.

**Write-Behind (Write-Back)** — write to cache immediately, write to database asynchronously later. Fast writes but risk of data loss if cache fails before async write completes.

**Read-Through** — cache sits in front of database and handles loading itself. App only ever talks to cache. Simpler application code.

**Pub/Sub** — use Redis messaging for lightweight real-time notifications between services.

---

## AZ-204 Exam Summary

The exam focuses on **when to use Redis** (caching frequently accessed data, session storage, leaderboards, rate limiting, pub/sub), the **service tiers** and what's exclusive to Premium (persistence, clustering, VNet integration), the **data structures** and their use cases (String for caching, Hash for objects, List for feeds/queues, Sorted Set for leaderboards, Set for unique tracking), the **cache-aside pattern** and how to implement it in .NET using both the StackExchange.Redis SDK and `IDistributedCache`, the difference between **AbsoluteExpiration and SlidingExpiration**, **eviction policies** especially `allkeys-lru`, and how to **securely store the Redis connection string** using Key Vault references.

Want practice questions on Redis, or shall we move on to the last topic — Azure CDN & Front Door?