
# Azure CDN & Front Door

These two services both sit in front of your applications and improve performance and availability — but they solve different problems at different scales.

---

## Start With the Problem

Your web application is hosted in East US. A user in Tokyo requests your homepage. That request travels halfway around the world, your server processes it, and the response travels back. That round trip might take 300-400ms just from network latency — before your app even does any work.

Now multiply that by every asset on your page — images, CSS, JavaScript, videos. Every one of those files makes that same round trip for every user far from your datacenter.

**CDN** solves this by storing copies of your static content closer to users around the world.

**Front Door** solves this and more — it's a global load balancer, WAF, and intelligent traffic router combined.

---

## Part 1: Azure CDN

### The Core Concept

A CDN (Content Delivery Network) is a **globally distributed network of servers called Points of Presence (PoPs)**. When a user requests a file, they get it from the nearest PoP rather than your origin server. The first request might still go to your origin — but the response is cached at the PoP. Every subsequent request from that region gets the cached copy instantly.

```
WITHOUT CDN:
Tokyo user → 300ms → East US origin server → 300ms → Tokyo user
                      (every single request)

WITH CDN:
First request:  Tokyo user → 300ms → East US origin → cached at Tokyo PoP
Later requests: Tokyo user → 5ms → Tokyo PoP (cached copy)
                (fast for everyone in Asia)
```

---

### What CDN Is Good For

CDN is optimized for **static, cacheable content**:

- Images, videos, audio files
- CSS and JavaScript files
- HTML pages that don't change per user
- Software downloads
- Font files

CDN is **not** the right tool for:

- Dynamic API responses that change per user
- Real-time data
- Content that requires authentication per request
- Anything that can't be safely cached and shared

---

### Azure CDN Profiles and Endpoints

```bash
# Create a CDN profile (the container for endpoints)
# Profile tier determines features — Standard_Microsoft is most common
az cdn profile create \
  --resource-group myRG \
  --name mycdnprofile \
  --sku Standard_Microsoft

# Create an endpoint pointing to your origin
az cdn endpoint create \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --name mycdnendpoint \
  --origin myapp.azurewebsites.net \
  --origin-host-header myapp.azurewebsites.net \
  --enable-compression true \
  --content-types-to-compress "text/html" "text/css" \
                               "application/javascript" "image/svg+xml"
```

Once created your endpoint URL is `mycdnendpoint.azureedge.net`. Users request assets from this URL — CDN handles the rest.

You can add a custom domain:

```bash
az cdn custom-domain create \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --endpoint-name mycdnendpoint \
  --name myCustomDomain \
  --hostname cdn.myapp.com
```

---

### Caching Rules and TTL

CDN respects cache headers from your origin server (`Cache-Control`, `Expires`). You can also override them with CDN caching rules.

```bash
# Set a global caching rule — cache everything for 1 day
az cdn endpoint rule add \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --name mycdnendpoint \
  --order 1 \
  --rule-name "GlobalCaching" \
  --match-variable RequestScheme \
  --action-name CacheExpiration \
  --cache-behavior SetIfMissing \
  --cache-duration "1.00:00:00"   # 1 day
```

Three caching behaviors:

- **Bypass** — never cache, always go to origin
- **Override** — always use this TTL regardless of origin headers
- **Set if missing** — use this TTL only if origin didn't set one

---

### Cache Purging

When you update a file at your origin you need to invalidate the cached version at CDN PoPs — otherwise users get stale content for the rest of the TTL.

```bash
# Purge a specific file
az cdn endpoint purge \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --name mycdnendpoint \
  --content-paths "/images/logo.png" "/css/main.css"

# Purge everything (use sparingly — expensive operation)
az cdn endpoint purge \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --name mycdnendpoint \
  --content-paths "/*"
```

A better pattern than manual purging is **versioned file names** — `main.v2.css` instead of `main.css`. When you update the file, the new version has a new name, so CDN automatically fetches it fresh. Old cached versions expire naturally.

---

### CDN in .NET — Generating CDN URLs

```csharp
public class AssetUrlHelper
{
    private readonly string _cdnBaseUrl;
    private readonly string _version;

    public AssetUrlHelper(IConfiguration config)
    {
        _cdnBaseUrl = config["CdnBaseUrl"];      // https://mycdnendpoint.azureedge.net
        _version = config["AssetVersion"];        // e.g. "v2024031501"
    }

    // Generate a versioned CDN URL for a static asset
    public string GetAssetUrl(string assetPath)
    {
        // e.g. /images/logo.png → https://mycdnendpoint.azureedge.net/images/logo.png?v=v2024031501
        return $"{_cdnBaseUrl}{assetPath}?v={_version}";
    }

    // For Azure Blob Storage as CDN origin
    public string GetBlobCdnUrl(string containerName, string blobName)
    {
        return $"{_cdnBaseUrl}/{containerName}/{blobName}";
    }
}
```

---

### CDN with Blob Storage

A very common pattern — store static files in Blob Storage and put CDN in front of it. Users get blazing fast delivery, Blob Storage handles durability and cost, CDN handles global distribution.

```bash
# Point CDN endpoint at a Blob Storage container
az cdn endpoint create \
  --resource-group myRG \
  --profile-name mycdnprofile \
  --name blobcdnendpoint \
  --origin mystorageaccount.blob.core.windows.net \
  --origin-host-header mystorageaccount.blob.core.windows.net \
  --enable-compression true
```

Now `https://blobcdnendpoint.azureedge.net/images/logo.png` serves the blob `logo.png` from the `images` container — cached globally at CDN PoPs.

---

## Part 2: Azure Front Door

### The Core Concept

Front Door is a **global, intelligent entry point** for your web applications. It operates at Layer 7 (HTTP/HTTPS) at the network edge — meaning traffic is handled as close to the user as possible before being routed to your backend.

Think of it as CDN + global load balancing + WAF + intelligent routing combined into one service.

```
Users worldwide
      │
      ▼
Azure Front Door (global edge — 100+ PoPs worldwide)
      │
      ├── WAF — block attacks at the edge
      ├── SSL termination — handle HTTPS close to user
      ├── Caching — serve static content from edge
      ├── Routing — send to best available backend
      │
      ▼
Your backends (multiple regions)
├── East US — Primary
├── West Europe — Secondary
└── Southeast Asia — Tertiary
```

---

### CDN vs Front Door — The Key Distinction

This is the most important exam concept in this section:

**Azure CDN** — optimized for **static content delivery**. Caches files at PoPs. Simple origin configuration. Cheaper. The right tool when you just need fast file delivery.

**Azure Front Door** — optimized for **dynamic web applications and APIs**. Global load balancing, health probes, failover, WAF, URL-based routing, session affinity. More expensive but far more capable. The right tool when you need intelligent traffic management across multiple backends.

||**Azure CDN**|**Azure Front Door**|
|---|---|---|
|Primary use|Static content caching|Global load balancing + routing|
|Dynamic content|Poor fit|Excellent|
|Multi-region failover|No|Yes|
|WAF|Basic (some SKUs)|Full WAF built in|
|URL path routing|Limited|Full path/header based routing|
|Health probes|No|Yes|
|Session affinity|No|Yes|
|SSL offload|Yes|Yes|
|Price|Lower|Higher|

---

### Front Door Components

**Profile** — the top-level resource. Standard or Premium tier.

**Endpoint** — the publicly accessible hostname, like `myapp.z01.azurefd.net`. Your users hit this URL.

**Origin Group** — a set of backend servers that serve the same content. Front Door load balances across them and monitors their health. You might have one origin group for your primary region and another for a secondary.

**Origin** — an individual backend server within an origin group. Could be an App Service, AKS cluster, Storage Account, public IP, or any reachable endpoint.

**Route** — maps incoming URL patterns to origin groups. `/api/*` goes to your API origin group. `/images/*` comes from your storage origin group. `/*` goes to your web app origin group.

**Rule Set** — custom rules for transforming requests and responses — similar to APIM policies but at the network edge.

**WAF Policy** — Web Application Firewall rules that block common attacks (SQL injection, XSS, rate limiting) before requests reach your backends.

---

### Creating Front Door

```bash
# Create a Front Door Standard profile
az afd profile create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --sku Standard_AzureFrontDoor

# Create an endpoint
az afd endpoint create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --enabled-state Enabled

# Create an origin group with health probes
az afd origin-group create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --origin-group-name myOriginGroup \
  --probe-request-type GET \
  --probe-protocol Https \
  --probe-interval-in-seconds 30 \
  --probe-path /health \
  --sample-size 4 \
  --successful-samples-required 3 \
  --additional-latency-in-milliseconds 50

# Add primary backend (East US App Service)
az afd origin create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --origin-group-name myOriginGroup \
  --origin-name eastus-origin \
  --host-name myapp-eastus.azurewebsites.net \
  --origin-host-header myapp-eastus.azurewebsites.net \
  --priority 1 \          # lower = higher priority
  --weight 100 \
  --enabled-state Enabled

# Add secondary backend (West Europe App Service)
az afd origin create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --origin-group-name myOriginGroup \
  --origin-name westeurope-origin \
  --host-name myapp-westeurope.azurewebsites.net \
  --origin-host-header myapp-westeurope.azurewebsites.net \
  --priority 2 \          # higher priority number = failover target
  --weight 100 \
  --enabled-state Enabled

# Create a route — all traffic goes to origin group
az afd route create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --route-name myRoute \
  --origin-group myOriginGroup \
  --supported-protocols Https \
  --https-redirect Enabled \
  --forwarding-protocol HttpsOnly \
  --patterns-to-match "/*"
```

---

### Routing — URL Path Based

One of Front Door's most powerful features — send different URL patterns to different backends:

```bash
# Route /api/* to your API backend
az afd route create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --route-name apiRoute \
  --origin-group apiOriginGroup \
  --patterns-to-match "/api/*" \
  --forwarding-protocol HttpsOnly \
  --cache-configuration '{"queryStringCachingBehavior": "IgnoreQueryString"}'

# Route /images/* to blob storage
az afd route create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --route-name imagesRoute \
  --origin-group storageOriginGroup \
  --patterns-to-match "/images/*" \
  --forwarding-protocol HttpsOnly \
  --cache-configuration '{"cacheBehavior": "HonorOrigin"}'

# Route everything else to web app
az afd route create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --route-name defaultRoute \
  --origin-group webOriginGroup \
  --patterns-to-match "/*" \
  --forwarding-protocol HttpsOnly
```

---

### Health Probes and Failover

Front Door continuously monitors your backends with health probes. When a backend goes unhealthy, Front Door automatically stops sending traffic to it and routes to the next available backend.

```
Normal operation:
Traffic → East US (priority 1, healthy) ← 100% of traffic

East US goes down:
Health probe fails 3 times in a row → marked unhealthy
Traffic → West Europe (priority 2) ← 100% of traffic automatically

East US recovers:
Health probe succeeds → marked healthy
Traffic → East US (priority 1) ← 100% of traffic again
```

This happens automatically with no manual intervention and typically within 30-90 seconds of a failure being detected.

---

### WAF — Web Application Firewall

Front Door Premium includes a WAF that blocks common web attacks at the global edge — before malicious traffic ever reaches your application.

```bash
# Create a WAF policy
az network front-door waf-policy create \
  --resource-group myRG \
  --name myWafPolicy \
  --sku Premium_AzureFrontDoor \
  --mode Prevention    # Detection mode just logs, Prevention mode blocks

# Enable the Microsoft managed ruleset (covers OWASP top 10)
az network front-door waf-policy managed-rules add \
  --policy-name myWafPolicy \
  --resource-group myRG \
  --type Microsoft_DefaultRuleSet \
  --version 2.1

# Add a rate limiting rule — block IPs sending more than 1000 requests per minute
az network front-door waf-policy rule create \
  --policy-name myWafPolicy \
  --resource-group myRG \
  --name RateLimitRule \
  --priority 100 \
  --rule-type RateLimitRule \
  --rate-limit-duration OneMin \
  --rate-limit-threshold 1000 \
  --action Block \
  --match-variable RequestUri \
  --operator Contains \
  --values "/"

# Associate WAF policy with Front Door endpoint
az afd security-policy create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --security-policy-name mySecurityPolicy \
  --domains myafdendpoint \
  --waf-policy myWafPolicy
```

---

### Rule Sets — Request and Response Transformation

Similar to APIM policies, Front Door Rule Sets let you modify requests and responses at the edge:

```bash
# Create a rule set
az afd rule-set create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --rule-set-name myRuleSet

# Rule 1: Redirect HTTP to HTTPS
az afd rule create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --rule-set-name myRuleSet \
  --rule-name HttpsRedirect \
  --order 1 \
  --match-variable RequestScheme \
  --operator Equal \
  --match-values HTTP \
  --action-name UrlRedirect \
  --redirect-type Moved \
  --redirect-protocol Https

# Rule 2: Add security headers to all responses
az afd rule create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --rule-set-name myRuleSet \
  --rule-name SecurityHeaders \
  --order 2 \
  --action-name ModifyResponseHeader \
  --header-action Append \
  --header-name "Strict-Transport-Security" \
  --header-value "max-age=31536000; includeSubDomains"

# Rule 3: Route mobile users to mobile-optimized backend
az afd rule create \
  --resource-group myRG \
  --profile-name myafdprofile \
  --rule-set-name myRuleSet \
  --rule-name MobileRouting \
  --order 3 \
  --match-variable RequestHeader \
  --selector "User-Agent" \
  --operator Contains \
  --match-values "Mobile" \
  --action-name RouteConfigurationOverride \
  --origin-group mobileOriginGroup
```

---

### Caching in Front Door

Front Door can cache responses at the edge just like CDN — reducing backend load and improving response times for cacheable content:

```bash
# Enable caching on a route
az afd route update \
  --resource-group myRG \
  --profile-name myafdprofile \
  --endpoint-name myafdendpoint \
  --route-name myRoute \
  --cache-configuration '{
    "cacheBehavior": "HonorOrigin",
    "queryStringCachingBehavior": "UseQueryString",
    "compressionSettings": {
      "isCompressionEnabled": true,
      "contentTypesToCompress": ["text/html", "text/css", "application/javascript"]
    }
  }'
```

Query string caching behaviors:

- **IgnoreQueryString** — same cache entry regardless of query params. Good for assets.
- **UseQueryString** — different cache entries per unique query string. Good for APIs with query-based filtering.
- **IgnoreSpecifiedQueryStrings** — ignore certain query params (like tracking params) but respect others.

---

### Session Affinity

When you need a user to always hit the same backend (for stateful apps), enable session affinity:

```bash
az afd origin-group update \
  --resource-group myRG \
  --profile-name myafdprofile \
  --origin-group-name myOriginGroup \
  --session-affinity-state Enabled
```

Front Door sets a cookie on the first response. Subsequent requests from the same user go to the same backend. If that backend fails, Front Door breaks affinity and routes to a healthy one.

---

## Putting It All Together — When to Use What

The exam will present scenarios. Here's how to think through them:

**Use Azure CDN when:**

- You have static files (images, CSS, JS, videos) that need fast global delivery
- Your origin is a single region
- You want the simplest, cheapest solution for caching static assets
- You're using Blob Storage as your file store

**Use Azure Front Door when:**

- You have a globally distributed application with backends in multiple regions
- You need automatic failover if a region goes down
- You need a WAF to protect against attacks
- You need URL-path-based routing to different backends
- You need intelligent load balancing (latency-based, priority-based, weighted)
- Your app has both static and dynamic content with complex routing requirements

**Use both together when:**

- Front Door handles routing, WAF, and dynamic content
- CDN handles pure static asset delivery from blob storage

---

## AZ-204 Exam Summary

For **Azure CDN** the exam focuses on understanding **what CDN is for** (static cacheable content, global delivery), the **CDN endpoint and origin** relationship, **caching rules and TTL** configuration, **cache purging** and why versioned file names are better, and CDN with **Blob Storage as origin**.

For **Azure Front Door** the exam focuses on the **distinction from CDN** (dynamic apps, multi-region, intelligent routing), the **components** (profile, endpoint, origin group, origin, route, rule set, WAF), how **health probes and automatic failover** work, **URL path-based routing** to different backends, the **WAF** and its two modes (Detection vs Prevention), and **session affinity** for stateful applications.

The biggest exam trap is choosing between CDN and Front Door for a given scenario — remember CDN is for static files and simplicity, Front Door is for global applications that need intelligence, resilience, and security.

---

That's the last major topic covered. You've now been through the entire AZ-204 syllabus. Want to do a full practice exam session with scenario-based questions across all topics?