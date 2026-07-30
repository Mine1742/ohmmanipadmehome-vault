
APIM is one of those things that makes no sense until you have the right mental picture. Let me build that picture first before we touch a single line of policy XML.

---

## Start Here: The Problem APIM Solves

Imagine you work at a company and you've built three backend services:

```
Orders API      → https://orders-app.azurewebsites.net
Inventory API   → https://inventory-app.azurewebsites.net
Customers API   → https://customers-app.azurewebsites.net
```

You want to let three different groups call these APIs:

- Your own **mobile app**
- A **partner company**
- **Third-party developers**

Immediately you have problems:

- How does each caller prove who they are?
- How do you stop one bad caller from hammering your APIs with millions of requests?
- How do you stop partners from calling the Customers API (they should only see Orders)?
- How do you hide the fact that your backend URLs changed when you moved from App Service to Functions?
- How do you give developers documentation so they know how to use your APIs?

You could solve all of this inside each individual API — but then you're duplicating security logic, rate limiting, and documentation across three separate codebases. That's a maintenance nightmare.

**APIM is the single front door that solves all of this in one place.** Your backends stay simple. APIM handles everything else.

```
                    ┌──────────────────┐
Mobile App    ─────►│                  │─────► Orders API
Partner       ─────►│   API Management │─────► Inventory API
3rd Party Dev ─────►│                  │─────► Customers API
                    └──────────────────┘
                      One front door.
                      All the rules live here.
```

---

## The Five Things APIM Does

Before any code or config, just internalize these five jobs:

**1. Authentication** — "Who are you? Show me your key or token."

**2. Authorization** — "You're allowed to call Orders but not Customers."

**3. Rate Limiting** — "You can make 100 calls per minute. After that, you're blocked until the next minute."

**4. Transformation** — "The backend expects XML but the caller sent JSON — I'll convert it. The backend returns sensitive fields — I'll strip them before responding."

**5. Routing** — "Send v1 callers to the old backend. Send v2 callers to the new backend."

All five happen **between** the caller and your backend. Your backend never has to think about any of it.

---

## The Three Main Pieces

There are only three things you really need to understand structurally.

### 1. The Gateway

This is the actual URL your callers hit — something like `https://myapim.azure-api.net`. When a request comes in, the gateway:

- Checks the caller is who they say they are
- Applies whatever rules you've defined
- Forwards the request to the right backend
- Gets the response and applies any outbound rules
- Returns the response to the caller

The gateway is the engine. Everything else is configuration for that engine.

### 2. APIs

An API in APIM is just a **description of a backend service** — its URL, its endpoints, and what parameters they accept. You import it from a Swagger/OpenAPI file or define it manually.

Think of it like a menu. The menu doesn't make the food — it just describes what's available and how to order it. Your actual backend makes the food.

### 3. Products

A product is a **bundle of APIs with a set of rules attached**.

Think of it like a phone plan:

- **Free plan** — access to basic APIs, 100 calls/day
- **Standard plan** — access to more APIs, 10,000 calls/day
- **Enterprise plan** — access to all APIs, unlimited calls

Callers subscribe to a product. When they subscribe, they get a **subscription key** — a long string they include with every API call to prove they have access. APIM reads that key, figures out which product they're on, and applies that product's rules.

---

## A Concrete Walkthrough

Let's say a partner calls your Orders API. Here's what happens step by step:

```
1. Partner sends request:
   GET https://myapim.azure-api.net/orders/123
   Header: Ocp-Apim-Subscription-Key: abc123xyz

2. APIM Gateway receives it and thinks:
   "Let me look up this subscription key abc123xyz..."
   "OK — this is Contoso Ltd, on the Standard product."

3. APIM checks the Standard product's rules:
   "Have they exceeded their rate limit? No — 45 calls this minute, limit is 100."
   "Are they allowed to call the Orders API? Yes — it's in the Standard product."

4. APIM transforms the request if needed:
   "Strip the subscription key header — backend doesn't need it."
   "Add X-Partner-Id: contoso — so the backend knows who's calling."

5. APIM forwards to backend:
   GET https://orders-app.azurewebsites.net/orders/123
   Header: X-Partner-Id: contoso

6. Backend responds with the order data.

7. APIM processes the response:
   "Strip the internal cost-price field — partners shouldn't see that."
   "Add a cache header."

8. APIM returns the cleaned response to the partner.
```

The partner never knew the backend URL. The backend never had to validate the subscription key. Everything happened in the middle.

---

## Policies — Now They'll Make Sense

A policy is just **a rule that APIM applies during that process**. That's it.

The XML format looks scary at first but it's just a structured way of saying:

- **Inbound** — rules to apply to the incoming request (before it reaches the backend)
- **Backend** — how to forward the request
- **Outbound** — rules to apply to the response (before it reaches the caller)
- **On-error** — what to do if something goes wrong

Think of it as four checkpoints the request passes through:

```
Caller ──► [Inbound checkpoint] ──► Backend ──► [Outbound checkpoint] ──► Caller
                                        ↕
                              [On-error if anything breaks]
```

Let's look at a dead simple policy — just adding a header:

```xml
<policies>
    <inbound>
        <!-- When a request comes IN, add this header before sending to backend -->
        <set-header name="X-Partner-Id" exists-action="override">
            <value>contoso</value>
        </set-header>
    </inbound>

    <outbound>
        <!-- When a response comes OUT, remove this internal field -->
        <set-header name="X-Internal-Cost" exists-action="delete" />
    </outbound>
</policies>
```

That's a real policy. It adds a header going in and removes one going out. Everything else we covered before is just more of those same building blocks.

---

## The `<base />` Tag Explained Simply

This is the one thing that trips everyone up.

Policies can be defined at four levels — think of them as nested:

```
Global policy (applies to everything)
  └── Product policy (applies to this product)
        └── API policy (applies to this API)
              └── Operation policy (applies to this one endpoint)
```

When you write a policy at the API level, you might still want the product-level rules to also run. The `<base />` tag means **"run the parent level's policy right here."**

```xml
<!-- This is the API-level policy -->
<policies>
    <inbound>
        <base />   <!-- ← run the product-level inbound rules first -->
        <!-- then run my API-specific rules -->
        <set-header name="X-Api-Name" exists-action="override">
            <value>orders-api</value>
        </set-header>
    </inbound>
</policies>
```

Without `<base />`, the parent policy is skipped entirely. With it, parent runs at exactly that point. That's all it does.

---

## Rate Limiting Explained Simply

Rate limiting is one of the most common policy uses. Two types — and the exam tests both:

**rate-limit** — a sliding window. "Max 100 calls per 60 seconds." If you send 100 calls in the first 5 seconds, you're blocked for the remaining 55 seconds. Then the window resets.

**quota** — a longer-term allowance. "Max 10,000 calls per day." Doesn't matter how fast you send them — once you hit 10,000 you're done until tomorrow.

They work together — rate-limit prevents bursts, quota prevents total overuse:

```xml
<inbound>
    <!-- Don't send more than 10 per second -->
    <rate-limit calls="10" renewal-period="1" />

    <!-- And don't send more than 10,000 total per day -->
    <quota calls="10000" renewal-period="86400" />
</inbound>
```

When you exceed rate-limit → caller gets **429 Too Many Requests** When you exceed quota → caller gets **403 Forbidden**

---

## JWT Validation Explained Simply

When you want callers to authenticate with Azure AD tokens instead of (or in addition to) subscription keys, you use the `validate-jwt` policy.

The caller gets a token from Azure AD and sends it in the Authorization header. APIM intercepts the request and checks:

- Is this token actually from Azure AD? (checks the signature)
- Is this token meant for my API? (checks the `aud` claim)
- Has it expired? (checks the `exp` claim)

If any check fails, APIM blocks the request with a 401 before it ever reaches your backend. Your backend doesn't need to implement any auth logic at all.

```xml
<inbound>
    <validate-jwt header-name="Authorization"
                  failed-validation-httpcode="401"
                  failed-validation-error-message="Please provide a valid token">

        <!-- Where to find Azure AD's public keys to verify the token signature -->
        <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />

        <!-- The token must be intended for your API (the 'aud' claim) -->
        <required-claims>
            <claim name="aud">
                <value>api://your-api-client-id</value>
            </claim>
        </required-claims>
    </validate-jwt>
</inbound>
```

---

## Named Values Explained Simply

Named values are just **APIM's version of environment variables or app settings**. Instead of hardcoding a value directly in your policy, you give it a name and reference it by that name.

Why? Because if the value changes, you update it in one place rather than hunting through every policy.

```xml
<!-- Without named values — hardcoded, bad -->
<set-header name="X-Api-Key" exists-action="override">
    <value>sk-live-abc123supersecrethardcoded</value>
</set-header>

<!-- With named values — clean, manageable -->
<set-header name="X-Api-Key" exists-action="override">
    <value>{{backend-api-key}}</value>
</set-header>
```

`{{backend-api-key}}` is the named value. Its actual value is stored securely in APIM (or as a Key Vault reference). The double curly brace syntax is just how you reference it in policies.

---

## Versions vs Revisions — The Simple Version

**Versions** = two different menus at the same restaurant, running at the same time.

Your API has a v1 at `/v1/orders` and a v2 at `/v2/orders`. Both are live. Old callers use v1, new callers use v2. They coexist.

**Revisions** = updating the menu without closing the restaurant.

You want to add a new endpoint to your API. You make a revision, test it privately, then "promote" it to be the current version. All existing callers don't notice — they never changed their URL. You just quietly updated what's behind it.

---

## The Developer Portal — One Sentence

The Developer Portal is an auto-generated website where external developers can browse your APIs, read documentation, test calls, and get their subscription key — without you having to build any of that yourself.

# Azure API Management (APIM)

Think of Azure API Management as a **front door for all your APIs**. Instead of exposing your backend services directly to consumers, you put APIM in front — it handles authentication, rate limiting, transformation, caching, monitoring, and documentation in one place. Your backends stay simple and focused on business logic while APIM handles all the cross-cutting concerns.

---

## The Core Concept

```
                        ┌─────────────────────────────┐
                        │     API Management           │
API Consumers           │                             │     Backend Services
─────────────           │  ┌─────────────────────┐   │     ───────────────
Mobile Apps    ─────►   │  │   Gateway           │   │  ►  App Service
Web Apps       ─────►   │  │   - Auth            │   │  ►  Azure Functions
Partners       ─────►   │  │   - Rate limiting   │   │  ►  AKS / Containers
Third parties  ─────►   │  │   - Transformation  │   │  ►  On-premises APIs
                        │  │   - Caching         │   │  ►  Logic Apps
                        │  │   - Logging         │   │
                        │  └─────────────────────┘   │
                        │                             │
                        │  Developer Portal           │
                        │  - API docs                 │
                        │  - Try it out               │
                        │  - Subscription keys        │
                        └─────────────────────────────┘
```

---

## Key Components

**Gateway** — the actual endpoint that receives API calls, applies policies, and forwards to backends. This is the runtime component — everything else is configuration.

**Management Plane** — the Azure portal / ARM / CLI interface for configuring APIs, products, policies, and users.

**Developer Portal** — an auto-generated, customizable website where API consumers can discover your APIs, read documentation, try them out, and get subscription keys. Can be published publicly or privately.

**APIs** — the definitions of your backend services imported into APIM. Can be imported from OpenAPI specs, WSDL, WADL, Azure Functions, App Service, Logic Apps, or defined manually.

**Products** — a way to bundle one or more APIs together and apply a shared set of policies (rate limits, quotas). Consumers subscribe to products, not individual APIs. Think of products as subscription tiers — Free (100 calls/day), Standard (10,000 calls/day), Premium (unlimited).

**Subscriptions** — a consumer's access key to a product. Every API call includes a subscription key in the `Ocp-Apim-Subscription-Key` header (or query string). APIM validates the key and identifies the consumer.

**Policies** — XML-based rules applied to API calls that can transform, restrict, or augment requests and responses. The most powerful feature of APIM and the heaviest exam topic.

---

## Service Tiers

**Consumption** — serverless, pay-per-call. No fixed cost. Scales to zero. No developer portal. No VNet integration. Good for lightweight scenarios and dev/test.

**Developer** — full feature set but single unit, no SLA. Not for production. Good for building and testing.

**Basic** — production-grade with SLA, limited scale. No VNet integration.

**Standard** — full feature set, VNet integration (external mode), more scale.

**Premium** — multi-region, VNet integration (internal and external), availability zones, highest scale. For enterprise production workloads.

The exam expects you to know that **VNet integration requires Standard or Premium** and that **multi-region deployment requires Premium**.

---

## Importing and Creating APIs

```bash
# Create an APIM instance
az apim create \
  --resource-group myRG \
  --name myapim \
  --publisher-name "My Company" \
  --publisher-email admin@mycompany.com \
  --sku-name Consumption

# Import API from OpenAPI spec (Swagger)
az apim api import \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-api \
  --path orders \
  --specification-format OpenApi \
  --specification-url https://myapp.azurewebsites.net/swagger/v1/swagger.json

# Import from Azure Function App
az apim api import \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-functions \
  --path functions/orders \
  --specification-format OpenApiJson \
  --specification-url https://myfunctionapp.azurewebsites.net/api/swagger.json

# Create a product
az apim product create \
  --resource-group myRG \
  --service-name myapim \
  --product-id standard-tier \
  --product-name "Standard" \
  --description "Standard API access — 10,000 calls per day" \
  --subscription-required true \
  --approval-required false \
  --state published

# Add API to product
az apim product api add \
  --resource-group myRG \
  --service-name myapim \
  --product-id standard-tier \
  --api-id orders-api
```

---

## Policies — The Heart of APIM

Policies are XML documents applied at four scopes and four execution points. This is the most tested area of APIM on the exam.

### Policy Scopes (outer to inner — inner overrides outer)

**Global** — applies to all APIs in the APIM instance.

**Product** — applies to all APIs in a specific product.

**API** — applies to all operations in a specific API.

**Operation** — applies to a single API operation (most specific).

When policies at multiple scopes exist, they're combined using the `<base />` element which represents "run the parent scope's policy here."

### Policy Execution Points

```xml
<policies>
    <inbound>
        <!-- Applied to the incoming request BEFORE forwarding to backend -->
        <!-- Authentication, rate limiting, transformation, caching checks -->
        <base />   <!-- insert parent scope's inbound policies here -->
    </inbound>

    <backend>
        <!-- Applied just before the request is forwarded to backend -->
        <!-- Usually just <forward-request /> -->
        <base />
    </backend>

    <outbound>
        <!-- Applied to the response FROM backend BEFORE returning to client -->
        <!-- Response transformation, header injection, caching -->
        <base />
    </outbound>

    <on-error>
        <!-- Applied when an error occurs in any other section -->
        <!-- Error handling, custom error responses -->
        <base />
    </on-error>
</policies>
```

---

## Policy Examples — The Ones That Matter for the Exam

### Rate Limiting and Quotas

```xml
<!-- Rate limit by subscription key — sliding window -->
<!-- Allows bursts up to the limit within each window -->
<inbound>
    <rate-limit calls="100" renewal-period="60" />
    <!-- 100 calls per 60 seconds per subscription -->
</inbound>

<!-- Quota by subscription — cumulative over longer period -->
<!-- Once quota is exhausted, consumer gets 403 until period resets -->
<inbound>
    <quota calls="10000" renewal-period="86400" />
    <!-- 10,000 calls per day (86400 seconds) per subscription -->
</inbound>

<!-- Rate limit by key — more flexible, can key on anything -->
<inbound>
    <rate-limit-by-key
        calls="100"
        renewal-period="60"
        counter-key="@(context.Request.IpAddress)"
        increment-condition="@(context.Response.StatusCode >= 200 && context.Response.StatusCode < 300)" />
    <!-- 100 successful calls per minute per IP address -->
</inbound>
```

### Authentication Policies

```xml
<!-- Validate a JWT token -->
<inbound>
    <validate-jwt
        header-name="Authorization"
        failed-validation-httpcode="401"
        failed-validation-error-message="Unauthorized — invalid token"
        require-expiration-time="true"
        require-signed-tokens="true">

        <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />

        <required-claims>
            <claim name="aud" match="any">
                <value>api://my-api-client-id</value>
            </claim>
        </required-claims>
    </validate-jwt>
    <base />
</inbound>

<!-- Validate subscription key (default behavior, explicit here for clarity) -->
<inbound>
    <check-header
        name="Ocp-Apim-Subscription-Key"
        failed-check-httpcode="401"
        failed-check-error-message="Missing subscription key"
        ignore-case="true" />
    <base />
</inbound>

<!-- Strip subscription key before forwarding to backend -->
<!-- Backend shouldn't need to see the APIM subscription key -->
<inbound>
    <set-header name="Ocp-Apim-Subscription-Key" exists-action="delete" />
    <base />
</inbound>
```

### Header and Request Transformation

```xml
<inbound>
    <!-- Add a header -->
    <set-header name="X-Forwarded-For" exists-action="override">
        <value>@(context.Request.IpAddress)</value>
    </set-header>

    <!-- Add backend API key from named value (Key Vault reference) -->
    <set-header name="X-Api-Key" exists-action="override">
        <value>{{backend-api-key}}</value>   <!-- named value, double curly braces -->
    </set-header>

    <!-- Remove a header -->
    <set-header name="X-Internal-Header" exists-action="delete" />

    <!-- Set a query parameter -->
    <set-query-parameter name="api-version" exists-action="override">
        <value>2024-01-01</value>
    </set-query-parameter>

    <!-- Rewrite the URL path -->
    <rewrite-uri template="/v2/orders/{orderId}" />

    <base />
</inbound>

<outbound>
    <!-- Add CORS headers in response -->
    <set-header name="Access-Control-Allow-Origin" exists-action="override">
        <value>https://myapp.com</value>
    </set-header>

    <!-- Remove internal headers from response before sending to client -->
    <set-header name="X-Powered-By" exists-action="delete" />
    <set-header name="Server" exists-action="delete" />

    <base />
</outbound>
```

### Caching

```xml
<inbound>
    <!-- Check cache before forwarding to backend -->
    <cache-lookup
        vary-by-developer="false"
        vary-by-developer-groups="false"
        downstream-caching-type="none">
        <vary-by-header>Accept</vary-by-header>
        <vary-by-query-parameter>customerId</vary-by-query-parameter>
    </cache-lookup>
    <base />
</inbound>

<outbound>
    <!-- Store response in cache for 60 seconds -->
    <cache-store duration="60" />
    <base />
</outbound>

<!-- External cache (Redis) for distributed caching across APIM units -->
<inbound>
    <cache-lookup-value
        key="@("orders-" + context.Request.MatchedParameters["customerId"])"
        variable-name="cachedOrders" />

    <choose>
        <when condition="@(context.Variables.ContainsKey("cachedOrders"))">
            <!-- Cache hit — return immediately without hitting backend -->
            <return-response>
                <set-status code="200" reason="OK" />
                <set-header name="Content-Type" exists-action="override">
                    <value>application/json</value>
                </set-header>
                <set-body>@((string)context.Variables["cachedOrders"])</set-body>
            </return-response>
        </when>
    </choose>
    <base />
</inbound>

<outbound>
    <!-- Store in external cache -->
    <cache-store-value
        key="@("orders-" + context.Request.MatchedParameters["customerId"])"
        value="@(context.Response.Body.As<string>(preserveContent: true))"
        duration="300" />
    <base />
</outbound>
```

### Request and Response Body Transformation

```xml
<!-- Transform JSON request body -->
<inbound>
    <set-body>@{
        var body = context.Request.Body.As<JObject>();
        body["processedAt"] = DateTime.UtcNow.ToString("O");
        body["source"] = "apim-gateway";
        return body.ToString();
    }</set-body>
    <base />
</inbound>

<!-- Transform XML response to JSON -->
<outbound>
    <xml-to-json kind="direct" apply="always" consider-accept-header="false" />
    <base />
</outbound>

<!-- Filter sensitive fields from response -->
<outbound>
    <set-body>@{
        var body = context.Response.Body.As<JObject>();
        body.Remove("internalId");
        body.Remove("costPrice");
        return body.ToString();
    }</set-body>
    <base />
</outbound>
```

### Conditional Logic

```xml
<!-- Route to different backends based on request -->
<inbound>
    <choose>
        <when condition="@(context.Request.Headers.GetValueOrDefault("X-Version", "") == "v2")">
            <!-- Route v2 clients to new backend -->
            <set-backend-service base-url="https://myapp-v2.azurewebsites.net" />
        </when>
        <when condition="@(context.User.Groups.Contains("beta-testers"))">
            <!-- Route beta testers to canary backend -->
            <set-backend-service base-url="https://myapp-canary.azurewebsites.net" />
        </when>
        <otherwise>
            <!-- Everyone else goes to stable backend -->
            <set-backend-service base-url="https://myapp.azurewebsites.net" />
        </otherwise>
    </choose>
    <base />
</inbound>

<!-- Return mock response without hitting backend -->
<inbound>
    <choose>
        <when condition="@(context.Request.Headers.GetValueOrDefault("X-Mock", "") == "true")">
            <return-response>
                <set-status code="200" reason="OK" />
                <set-header name="Content-Type" exists-action="override">
                    <value>application/json</value>
                </set-header>
                <set-body>{"id": "mock-001", "status": "pending"}</set-body>
            </return-response>
        </when>
    </choose>
    <base />
</inbound>
```

### Error Handling

```xml
<on-error>
    <!-- Log the error -->
    <set-variable name="errorMessage" value="@(context.LastError.Message)" />

    <!-- Return consistent error format regardless of backend error shape -->
    <return-response>
        <set-status code="@(context.Response.StatusCode)" reason="@(context.Response.StatusReason)" />
        <set-header name="Content-Type" exists-action="override">
            <value>application/json</value>
        </set-header>
        <set-body>@{
            return new JObject(
                new JProperty("error", context.LastError.Message),
                new JProperty("requestId", context.RequestId),
                new JProperty("timestamp", DateTime.UtcNow)
            ).ToString();
        }</set-body>
    </return-response>
    <base />
</on-error>
```

### Retry and Circuit Breaker

```xml
<backend>
    <!-- Retry up to 3 times on 5xx errors with exponential backoff -->
    <retry
        condition="@(context.Response.StatusCode >= 500)"
        count="3"
        interval="2"
        delta="2"
        max-interval="10"
        first-fast-retry="false">
        <forward-request timeout="30" />
    </retry>
</backend>
```

---

## Named Values

Named values are **key-value pairs stored in APIM** — used to avoid hardcoding values in policies. They can be plain text, secrets (encrypted), or Key Vault references.

```bash
# Create a plain named value
az apim nv create \
  --resource-group myRG \
  --service-name myapim \
  --named-value-id backend-timeout \
  --display-name "Backend Timeout" \
  --value "30"

# Create a secret named value
az apim nv create \
  --resource-group myRG \
  --service-name myapim \
  --named-value-id backend-api-key \
  --display-name "Backend API Key" \
  --value "sk-live-abc123" \
  --secret true

# Create a Key Vault reference (recommended for secrets)
az apim nv create \
  --resource-group myRG \
  --service-name myapim \
  --named-value-id backend-api-key \
  --display-name "Backend API Key" \
  --key-vault-secret-identifier "https://mykeyvault.vault.azure.net/secrets/BackendApiKey"
```

In policies, reference named values with double curly braces:

```xml
<set-header name="X-Api-Key" exists-action="override">
    <value>{{backend-api-key}}</value>
</set-header>
```

APIM must have a managed identity with `Key Vault Secrets User` role to use Key Vault references — same pattern as App Service.

---

## The Policy Expression Context Object

The `context` object is available in all policy expressions. Know its key properties for the exam:

```csharp
// Available in C# policy expressions as context.*

context.Request.IpAddress              // caller's IP
context.Request.Method                 // GET, POST, etc.
context.Request.Url.Path               // /api/orders/123
context.Request.Headers["X-Custom"]   // request headers
context.Request.Body.As<JObject>()    // deserialize body
context.Request.MatchedParameters["orderId"]  // route parameters

context.Response.StatusCode            // backend response code
context.Response.Body.As<JObject>()   // response body

context.Subscription.Id                // subscription ID
context.Subscription.Name              // subscription name
context.User.Id                        // user ID
context.User.Groups                    // user's groups

context.Variables["myVar"]            // values set with set-variable
context.RequestId                      // unique request ID
context.LastError.Message              // error in on-error section
context.Elapsed                        // time since request started
```

---

## Backends

Backends in APIM represent the actual services being called. Defining named backends lets you reference them in policies and switch them without changing policy code.

```bash
# Create a backend
az apim backend create \
  --resource-group myRG \
  --service-name myapim \
  --backend-id orders-backend \
  --url "https://myapp.azurewebsites.net/api" \
  --protocol http \
  --description "Orders API Backend"

# Reference in policy
# <set-backend-service backend-id="orders-backend" />
```

**Service Fabric backend** — APIM can directly communicate with Service Fabric clusters, routing to specific services and partitions.

**Load-balanced backends (backend pools)** — Premium feature for distributing traffic across multiple backend instances with health probes.

---

## APIM and Azure Functions / App Service Integration

APIM has native integration with both:

```bash
# Import directly from App Service
az apim api import \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-api \
  --path orders \
  --specification-format OpenApiJson \
  --specification-url "https://myapp.azurewebsites.net/swagger/v1/swagger.json"

# Import from Function App
az apim api import \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-functions-api \
  --path functions \
  --specification-format OpenApiJson \
  --specification-url "https://myfunctionapp.azurewebsites.net/api/swagger.json"
```

When importing from Functions, APIM automatically configures the function key — the function itself can use Anonymous auth while APIM handles authentication at its layer.

---

## Versioning and Revisions

These are two separate concepts that are often confused.

**Versions** — multiple live versions of an API coexisting simultaneously. Consumers choose which version to call. Two versioning schemes:

- **Path-based** — `/api/v1/orders`, `/api/v2/orders`
- **Header-based** — `Api-Version: v1` header
- **Query string-based** — `?api-version=v1`

**Revisions** — changes to an API without breaking existing consumers. Revisions are non-breaking changes you can test before making current. Only one revision is "current" at a time. Previous revisions stay accessible via a revision-specific URL for testing.

```bash
# Create a new API version
az apim api create \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-api-v2 \
  --path orders \
  --display-name "Orders API v2" \
  --api-version v2 \
  --api-version-scheme Segment \  # path-based: /v2/orders
  --api-version-set-id orders-version-set

# Create a revision
az apim api revision create \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-api \
  --api-revision 2 \
  --api-revision-description "Added bulk endpoint"

# Make revision current
az apim api release create \
  --resource-group myRG \
  --service-name myapim \
  --api-id orders-api \
  --api-revision 2 \
  --notes "Deployed bulk order endpoint"
```

---

## Monitoring APIM

APIM integrates natively with Azure Monitor:

**Built-in Analytics** — request volume, success rates, response times, top APIs, top operations — available in the portal without configuration.

**Application Insights Integration** — full request tracing, dependency tracking, custom metrics. Configure at the APIM instance level or per API.

```bash
# Connect APIM to Application Insights
az apim update \
  --resource-group myRG \
  --name myapim \
  --set properties.customProperties.APIM_AppInsightsInstrumentationKey=<key>
```

**Diagnostic Logs** — route to Log Analytics for KQL querying:

```kql
// APIM request logs in Log Analytics
ApiManagementGatewayLogs
| where TimeGenerated > ago(1h)
| where ResponseCode >= 400
| project TimeGenerated, OperationId, ApiId, ProductId,
          ResponseCode, DurationMs, ClientIp, RequestSize
| order by TimeGenerated desc

// Error rate by API
ApiManagementGatewayLogs
| where TimeGenerated > ago(24h)
| summarize
    total = count(),
    errors = countif(ResponseCode >= 500)
  by ApiId
| extend errorRate = (errors * 100.0) / total
| order by errorRate desc
```

---

## CORS Policy

A very common real-world requirement — enabling cross-origin requests from browser-based apps:

```xml
<inbound>
    <cors allow-credentials="true">
        <allowed-origins>
            <origin>https://myapp.com</origin>
            <origin>https://staging.myapp.com</origin>
        </allowed-origins>
        <allowed-methods>
            <method>GET</method>
            <method>POST</method>
            <method>PUT</method>
            <method>DELETE</method>
            <method>OPTIONS</method>
        </allowed-methods>
        <allowed-headers>
            <header>Authorization</header>
            <header>Content-Type</header>
            <header>Ocp-Apim-Subscription-Key</header>
        </allowed-headers>
        <expose-headers>
            <header>X-Request-Id</header>
        </expose-headers>
    </cors>
    <base />
</inbound>
```

---

## Full Policy Example — Putting It All Together

A realistic production policy combining multiple features:

```xml
<policies>
    <inbound>
        <!-- 1. Validate JWT from Azure AD -->
        <validate-jwt
            header-name="Authorization"
            failed-validation-httpcode="401"
            failed-validation-error-message="Valid bearer token required">
            <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />
            <required-claims>
                <claim name="aud">
                    <value>api://my-api-client-id</value>
                </claim>
            </required-claims>
        </validate-jwt>

        <!-- 2. Rate limit per subscription -->
        <rate-limit calls="1000" renewal-period="3600" />

        <!-- 3. Check cache -->
        <cache-lookup vary-by-developer="false" vary-by-developer-groups="false">
            <vary-by-query-parameter>customerId</vary-by-query-parameter>
        </cache-lookup>

        <!-- 4. Add correlation ID for tracing -->
        <set-header name="X-Correlation-ID" exists-action="skip">
            <value>@(context.RequestId.ToString())</value>
        </set-header>

        <!-- 5. Add backend API key from Key Vault named value -->
        <set-header name="X-Backend-Key" exists-action="override">
            <value>{{backend-api-key}}</value>
        </set-header>

        <!-- 6. Remove subscription key — backend doesn't need it -->
        <set-header name="Ocp-Apim-Subscription-Key" exists-action="delete" />

        <base />
    </inbound>

    <backend>
        <!-- Retry on transient failures -->
        <retry condition="@(context.Response.StatusCode == 503)" count="3" interval="1">
            <forward-request timeout="30" />
        </retry>
    </backend>

    <outbound>
        <!-- Cache successful responses -->
        <cache-store duration="60" />

        <!-- Remove internal headers from response -->
        <set-header name="X-Powered-By" exists-action="delete" />
        <set-header name="X-Backend-Key" exists-action="delete" />

        <!-- Add response time header for monitoring -->
        <set-header name="X-Response-Time" exists-action="override">
            <value>@(context.Elapsed.TotalMilliseconds.ToString())</value>
        </set-header>

        <base />
    </outbound>

    <on-error>
        <return-response>
            <set-status code="@(context.Response.StatusCode)" />
            <set-header name="Content-Type" exists-action="override">
                <value>application/json</value>
            </set-header>
            <set-body>@{
                return new JObject(
                    new JProperty("error", context.LastError.Message),
                    new JProperty("requestId", context.RequestId),
                    new JProperty("timestamp", DateTime.UtcNow.ToString("O"))
                ).ToString();
            }</set-body>
        </return-response>
        <base />
    </on-error>
</policies>
```

---

## Self-Hosted Gateway

Premium feature — deploy the APIM gateway component on your own infrastructure (Kubernetes, on-premises, other clouds). The gateway runs as a container but is managed from your Azure APIM instance. Useful for:

- APIs that must stay on-premises for compliance
- Edge deployments close to IoT devices
- Hybrid cloud scenarios

```bash
# Create a self-hosted gateway resource
az apim gateway create \
  --resource-group myRG \
  --service-name myapim \
  --gateway-id my-onprem-gateway \
  --description "On-premises gateway" \
  --location-data '{"name": "On-premises DC", "city": "Washington"}'

# Deploy as Kubernetes deployment using the generated config
# (portal provides the Kubernetes YAML with connection token)
```

---

## AZ-204 Exam Summary

APIM is tested heavily on **policies** — know the four execution sections (inbound, backend, outbound, on-error), the four policy scopes (global, product, API, operation), and how `<base />` works to chain them. Know the specific policies: `rate-limit`, `quota`, `rate-limit-by-key`, `validate-jwt`, `cache-lookup`/`cache-store`, `set-header`, `set-body`, `rewrite-uri`, `choose`/`when`, `return-response`, and `retry`. Understand **named values** and why Key Vault references are preferred for secrets. Know the difference between **versions** (multiple live APIs) and **revisions** (non-breaking changes to one API). Know the **tier differences** especially around VNet integration and multi-region. Understand how APIM integrates with **Azure AD token validation**, **Application Insights**, and **Azure Functions/App Service**. Finally know the **context object** properties available in policy expressions.

Want practice scenario questions on APIM, or shall we move to the next topic?