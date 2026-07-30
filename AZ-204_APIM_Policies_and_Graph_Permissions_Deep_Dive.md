# AZ-204 Deep Dive: APIM Policies & Microsoft Graph Permissions

---

## Part 1: APIM Policies — Know Them Cold

### How Policies Work

Policies are XML documents that execute as a pipeline on every API request. Think of them like middleware — they intercept the request on the way in, can modify the backend call, intercept the response on the way out, and handle errors.

### The Four Policy Sections

Every policy document has exactly four sections that execute in this order:

```
Client → [INBOUND] → [BACKEND] → Azure backend service → [OUTBOUND] → Client
                                                              ↓
                                                         [ON-ERROR] (if anything throws)
```

```xml
<policies>
    <inbound>
        <!-- Executes BEFORE the request reaches your backend -->
        <!-- Use for: auth, rate limiting, caching lookups, request transforms -->
        <base />
    </inbound>
    <backend>
        <!-- Controls HOW the request is forwarded to the backend -->
        <!-- Use for: routing, retry, forwarding -->
        <base />
    </backend>
    <outbound>
        <!-- Executes AFTER the backend responds, BEFORE client gets it -->
        <!-- Use for: response transforms, caching stores, header cleanup -->
        <base />
    </outbound>
    <on-error>
        <!-- Executes ONLY when an error occurs in any other section -->
        <!-- Use for: logging errors, returning custom error responses -->
        <base />
    </on-error>
</policies>
```

### The `<base />` Element — Exam Favorite

`<base />` controls WHERE the parent scope's policies run relative to the current scope's policies. Policies are scoped at four levels: **Global → Product → API → Operation**.

```xml
<!-- Parent policies run FIRST, then mine -->
<inbound>
    <base />
    <rate-limit calls="10" renewal-period="60" />
</inbound>

<!-- My policies run FIRST, then parent -->
<inbound>
    <set-header name="X-Custom" exists-action="override">
        <value>my-value</value>
    </set-header>
    <base />
</inbound>

<!-- Parent policies DON'T run at all (override completely) -->
<inbound>
    <rate-limit calls="10" renewal-period="60" />
    <!-- no <base /> = parent scope is ignored -->
</inbound>

<!-- Policies sandwich around parent -->
<inbound>
    <set-header name="Before" exists-action="override"><value>1</value></set-header>
    <base />
    <set-header name="After" exists-action="override"><value>2</value></set-header>
</inbound>
```

**Exam trap:** If `<base />` is missing, the parent scope's policies are completely skipped. This is a valid pattern but can cause unexpected behavior if you forget.

---

### Every Policy You Must Know

#### ACCESS RESTRICTION POLICIES (Inbound)

**`rate-limit` — Fixed window throttle**
```xml
<!-- Hard limit: 5 calls per 60 seconds per subscription -->
<rate-limit calls="5" renewal-period="60" />
```
Returns **HTTP 429 Too Many Requests** when exceeded. Counter is per-subscription by default.

**`rate-limit-by-key` — Flexible throttle keyed on any expression**
```xml
<!-- Limit by caller IP address -->
<rate-limit-by-key calls="10" renewal-period="90"
    counter-key="@(context.Request.IpAddress)" />

<!-- Limit by user identity claim -->
<rate-limit-by-key calls="100" renewal-period="60"
    counter-key="@(context.Request.Headers.GetValueOrDefault("Authorization","anonymous"))" />
```
Use this when you need to throttle by something other than subscription (IP, user ID, custom header, JWT claim).

**`quota` / `quota-by-key` — Hard cap over longer period**
```xml
<!-- 1000 calls and 10MB bandwidth per 7-day period -->
<quota calls="1000" bandwidth="10485760" renewal-period="604800" />

<!-- Quota per product -->
<quota-by-key calls="5000" renewal-period="2592000"
    counter-key="@(context.Product.Id)" />
```
Difference from rate-limit: quota is a **hard ceiling** that doesn't reset until the period ends. Rate-limit is a sliding/fixed window.

**Exam question pattern:** "Limit each user to 100 calls per minute" → `rate-limit-by-key`. "Limit each subscription to 10,000 calls per month" → `quota`.

**`ip-filter` — Allow/deny by IP**
```xml
<!-- Only allow these IPs -->
<ip-filter action="allow">
    <address>10.0.0.1</address>
    <address-range from="192.168.0.0" to="192.168.0.255" />
</ip-filter>

<!-- Block specific IPs -->
<ip-filter action="forbid">
    <address>203.0.113.50</address>
</ip-filter>
```

**`validate-jwt` — Validate OAuth tokens**
```xml
<validate-jwt header-name="Authorization" require-scheme="Bearer"
              failed-validation-httpcode="401"
              failed-validation-error-message="Unauthorized">
    <openid-config url="https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration" />
    <audiences>
        <audience>api://my-api-client-id</audience>
    </audiences>
    <issuers>
        <issuer>https://login.microsoftonline.com/{tenant}/v2.0</issuer>
    </issuers>
    <required-claims>
        <claim name="roles" match="any">
            <value>Admin</value>
            <value>Reader</value>
        </claim>
    </required-claims>
</validate-jwt>
```
This is how you protect APIs with Entra ID (Azure AD). The `openid-config` URL auto-discovers signing keys. You can check specific claims, audiences, and issuers.

**`check-header` — Require a specific header**
```xml
<check-header name="X-API-Version" failed-check-httpcode="400"
              failed-check-error-message="Missing version header" ignore-case="true">
    <value>v1</value>
    <value>v2</value>
</check-header>
```

**`cors` — Cross-origin resource sharing**
```xml
<cors allow-credentials="true">
    <allowed-origins>
        <origin>https://myapp.com</origin>
    </allowed-origins>
    <allowed-methods><method>GET</method><method>POST</method></allowed-methods>
    <allowed-headers><header>Authorization</header><header>Content-Type</header></allowed-headers>
</cors>
```

---

#### TRANSFORMATION POLICIES (Inbound or Outbound)

**`set-header` — Add, modify, or remove headers**
```xml
<!-- Add/override a header -->
<set-header name="X-Request-Source" exists-action="override">
    <value>apim-gateway</value>
</set-header>

<!-- Remove a header (e.g., strip internal headers from response) -->
<set-header name="X-Powered-By" exists-action="delete" />

<!-- Dynamic value from context -->
<set-header name="X-Subscription" exists-action="override">
    <value>@(context.Subscription.Id)</value>
</set-header>
```
`exists-action` values: `override`, `skip`, `append`, `delete`

**`set-query-parameter` — Add/modify query string params**
```xml
<set-query-parameter name="api-version" exists-action="override">
    <value>2024-01-01</value>
</set-query-parameter>
```

**`set-body` — Transform request or response body**
```xml
<!-- Static body -->
<set-body>{"status": "accepted"}</set-body>

<!-- Dynamic with Liquid template -->
<set-body template="liquid">
{
    "name": "{{body.firstName}} {{body.lastName}}",
    "email": "{{body.contactEmail}}"
}
</set-body>

<!-- C# expression for complex transforms -->
<set-body>@{
    var inBody = context.Request.Body.As<JObject>();
    inBody["timestamp"] = DateTime.UtcNow.ToString("o");
    return inBody.ToString();
}</set-body>
```

**`rewrite-uri` — Change the URL path before forwarding**
```xml
<!-- /external/resource → /internal/v2/resource -->
<rewrite-uri template="/internal/v2/resource" />
```
Only changes the path — not the hostname. The backend service URL stays the same.

**`find-and-replace` — Text replacement in body**
```xml
<find-and-replace from="://old-backend.com" to="://new-backend.com" />
```

**`xml-to-json` / `json-to-xml` — Format conversion**
```xml
<!-- In outbound: convert legacy XML backend to JSON for modern clients -->
<xml-to-json kind="direct" apply="always" consider-accept-header="false" />
```

---

#### CACHING POLICIES (Inbound + Outbound pair)

**`cache-lookup` (inbound) + `cache-store` (outbound)**
```xml
<inbound>
    <base />
    <!-- Check cache; if hit, skip backend and jump to outbound -->
    <cache-lookup vary-by-developer="false"
                  vary-by-developer-groups="false"
                  vary-by-query-parameter="category,page"
                  vary-by-header="Accept" />
</inbound>
<outbound>
    <base />
    <!-- Store response in cache for 1 hour -->
    <cache-store duration="3600" />
</outbound>
```
If `cache-lookup` finds a cached response, it skips the backend entirely and returns the cached version. The `vary-by-*` attributes control the cache key.

**`cache-store-value` / `cache-lookup-value` — Arbitrary key-value caching**
```xml
<!-- Store a value -->
<cache-store-value key="@("token-" + context.Subscription.Id)"
                   value="@(context.Response.Body.As<string>())"
                   duration="3600" />

<!-- Retrieve it later -->
<cache-lookup-value key="@("token-" + context.Subscription.Id)"
                    variable-name="cachedToken" />
<!-- Use: @((string)context.Variables["cachedToken"]) -->
```

**`cache-remove-value` — Invalidate a cached entry**
```xml
<cache-remove-value key="@("token-" + context.Subscription.Id)" />
```

---

#### BACKEND POLICIES

**`set-backend-service` — Route to a different backend dynamically**
```xml
<!-- Route based on a header value -->
<set-backend-service base-url="@{
    var region = context.Request.Headers.GetValueOrDefault("X-Region", "east");
    return region == "west" 
        ? "https://api-west.myapp.com" 
        : "https://api-east.myapp.com";
}" />
```

**`forward-request` — Control backend call behavior**
```xml
<forward-request timeout="30" follow-redirects="true" buffer-request-body="true" />
```
`buffer-request-body="true"` is needed if you read the body in inbound AND need it forwarded.

**`retry` — Retry failed backend calls**
```xml
<retry condition="@(context.Response.StatusCode == 503)"
       count="3" interval="1" max-interval="10" delta="2"
       first-fast-retry="true">
    <forward-request buffer-request-body="true" />
</retry>
```

---

#### ADVANCED / FLOW CONTROL POLICIES

**`send-request` — Make a side call to another service**
```xml
<!-- Example: validate a token with an external auth service -->
<send-request mode="new" response-variable-name="authResponse" timeout="10">
    <set-url>https://auth.myapp.com/validate</set-url>
    <set-method>POST</set-method>
    <set-header name="Content-Type" exists-action="override">
        <value>application/json</value>
    </set-header>
    <set-body>@(context.Request.Headers.GetValueOrDefault("Authorization",""))</set-body>
</send-request>
<!-- Now use: context.Variables["authResponse"] -->
<choose>
    <when condition="@(((IResponse)context.Variables["authResponse"]).StatusCode != 200)">
        <return-response>
            <set-status code="401" reason="Unauthorized" />
        </return-response>
    </when>
</choose>
```

**`return-response` — Short-circuit and return immediately**
```xml
<return-response>
    <set-status code="403" reason="Forbidden" />
    <set-header name="Content-Type" exists-action="override">
        <value>application/json</value>
    </set-header>
    <set-body>{"error": "Access denied"}</set-body>
</return-response>
```
Skips everything — no backend call, no outbound processing.

**`choose` — Conditional (if/else)**
```xml
<choose>
    <when condition="@(context.Request.Method == "POST")">
        <set-header name="X-Method" exists-action="override">
            <value>write</value>
        </set-header>
    </when>
    <when condition="@(context.Request.Method == "GET")">
        <set-header name="X-Method" exists-action="override">
            <value>read</value>
        </set-header>
    </when>
    <otherwise>
        <return-response>
            <set-status code="405" reason="Method Not Allowed" />
        </return-response>
    </otherwise>
</choose>
```

**`set-variable` — Store a value for later use**
```xml
<set-variable name="clientType" value="@(context.Request.Headers.GetValueOrDefault("X-Client","unknown"))" />
<!-- Later: @((string)context.Variables["clientType"]) -->
```

**`log-to-eventhub` — Send telemetry to Event Hubs**
```xml
<log-to-eventhub logger-id="my-logger">
    @{
        return new JObject(
            new JProperty("timestamp", DateTime.UtcNow),
            new JProperty("ip", context.Request.IpAddress),
            new JProperty("operation", context.Operation.Id)
        ).ToString();
    }
</log-to-eventhub>
```

**`emit-metric` — Custom metrics**
```xml
<emit-metric name="api-call" value="1" namespace="apim-metrics">
    <dimension name="API" value="@(context.Api.Name)" />
    <dimension name="Operation" value="@(context.Operation.Name)" />
</emit-metric>
```

**`mock-response` — Return a mock without hitting backend**
```xml
<!-- Returns the response defined in the API schema for this operation -->
<mock-response status-code="200" content-type="application/json" />
```

---

### Policy Context Object — Cheat Sheet

Inside `@()` expressions, you have access to the `context` object:

| Property | Example | What it gives you |
|----------|---------|-------------------|
| `context.Request.Method` | `"GET"` | HTTP method |
| `context.Request.Url.Path` | `"/api/orders"` | Request path |
| `context.Request.Url.Query["id"]` | `"123"` | Query param |
| `context.Request.IpAddress` | `"10.0.0.5"` | Client IP |
| `context.Request.Headers["name"]` | header value | Request header |
| `context.Request.Body.As<T>()` | JObject, string, etc. | Read body (consumes stream!) |
| `context.Response.StatusCode` | `200` | Backend response code |
| `context.Response.Headers["name"]` | header value | Response header |
| `context.Response.Body.As<T>()` | JObject, string | Response body |
| `context.Subscription.Id` | `"sub-abc"` | Subscription identifier |
| `context.Subscription.Key` | the key value | Subscription key used |
| `context.User.Email` | `"user@email.com"` | Authenticated user |
| `context.Product.Id` | `"prod-free"` | Product association |
| `context.Api.Name` | `"Orders API"` | Current API |
| `context.Operation.Id` | `"getOrders"` | Current operation |
| `context.Variables["name"]` | stored value | From set-variable |
| `context.Deployment.Region` | `"West US"` | Gateway region |

**Critical gotcha:** `Body.As<T>()` consumes the stream. If you need to read the body multiple times, use `Body.As<T>(preserveContent: true)` or `buffer-request-body="true"` on `forward-request`.

---

### Policy Quick Reference — Which Section?

| Policy | Section | Purpose |
|--------|---------|---------|
| `rate-limit` / `rate-limit-by-key` | inbound | Throttle requests |
| `quota` / `quota-by-key` | inbound | Hard call/bandwidth caps |
| `validate-jwt` | inbound | Token validation |
| `ip-filter` | inbound | IP allow/deny |
| `check-header` | inbound | Require headers |
| `cors` | inbound | CORS headers |
| `cache-lookup` | inbound | Check response cache |
| `set-header` | inbound / outbound | Modify headers |
| `set-query-parameter` | inbound | Modify query string |
| `set-body` | inbound / outbound | Transform body |
| `rewrite-uri` | inbound | Change URL path |
| `set-backend-service` | inbound / backend | Dynamic routing |
| `forward-request` | backend | Backend call config |
| `retry` | backend | Retry on failure |
| `cache-store` | outbound | Store in cache |
| `xml-to-json` / `json-to-xml` | outbound | Format conversion |
| `send-request` | any | Side HTTP call |
| `return-response` | any | Short-circuit return |
| `choose` | any | Conditional logic |
| `set-variable` | any | Store temporary value |
| `log-to-eventhub` | any | Telemetry |
| `mock-response` | inbound | Return mock data |

---

---

## Part 2: Microsoft Graph Permission Model — Delegated vs. Application

### The Two Permission Types

This distinction is fundamental to how Microsoft Graph enforces access control and shows up repeatedly on the exam.

### Delegated Permissions (User context)

**What it means:** Your app acts **on behalf of a signed-in user**. The app can never do more than what the user themselves can do.

**How it works:**
```
User signs in → App gets an access token → Token has delegated permissions
→ Graph API checks: Does the app have the permission AND does the user have access?
```

**Effective permissions = intersection of:**
1. What permissions the app was granted (configured in Entra ID app registration)
2. What the signed-in user is allowed to do (their role/license/admin status)

**Example:** Your app has `Mail.Read` delegated permission. User A signs in. The app can read User A's mail — not User B's. Even if the app technically "has" `Mail.Read`, it only applies within the signed-in user's scope.

**Consent model:**
- **User consent** — user agrees to let the app use their data. Works for low-privilege permissions like `User.Read`, `Mail.Read`.
- **Admin consent** — a tenant admin must agree. Required for higher-privilege delegated permissions like `User.Read.All` (read all users' profiles) or `Directory.Read.All`.

**OAuth flows used with delegated permissions:**
- **Authorization code flow** — web apps, SPAs (with PKCE)
- **On-behalf-of (OBO) flow** — when a middle-tier API needs to call Graph on behalf of the user who called it
- **Device code flow** — devices without browsers (IoT, CLI tools)

**Common delegated permissions:**

| Permission | What it allows | Admin consent? |
|-----------|---------------|----------------|
| `User.Read` | Read signed-in user's profile | No |
| `User.Read.All` | Read all users' profiles | Yes |
| `Mail.Read` | Read signed-in user's mail | No |
| `Mail.Send` | Send mail as signed-in user | No |
| `Calendars.ReadWrite` | Read/write signed-in user's calendar | No |
| `Files.ReadWrite` | Read/write signed-in user's OneDrive | No |
| `Group.Read.All` | Read all groups | Yes |
| `Directory.Read.All` | Read directory data | Yes |

### Application Permissions (No user context)

**What it means:** Your app acts **as itself**, not on behalf of any user. There is no signed-in user. This is for background services, daemons, scheduled jobs.

**How it works:**
```
App authenticates with client credentials (secret or certificate)
→ Gets an access token with application permissions
→ Token has NO user context
→ App can access data across the ENTIRE tenant
```

**Effective permissions = exactly what was granted to the app.** There's no user to intersect with. If the app has `Mail.Read` as an application permission, it can read EVERY user's mail in the tenant.

**This is why application permissions ALWAYS require admin consent.** They're extremely powerful.

**OAuth flow used with application permissions:**
- **Client credentials flow** — the only option. No user interaction.

```python
# Client credentials flow — application permissions
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-app-client-id",
    client_secret="your-client-secret"
)

graph_client = GraphServiceClient(credential)

# This reads ALL users because it's application permission
users = await graph_client.users.get()

# Must specify which user's mail (no "me" endpoint without a user context)
messages = await graph_client.users.by_user_id("user@domain.com").messages.get()
```

**Critical exam point:** With application permissions, you **cannot use `/me`** — there is no "me" because there is no signed-in user. You must always use `/users/{id-or-upn}/...`.

**Common application permissions:**

| Permission | What it allows | Scope |
|-----------|---------------|-------|
| `User.Read.All` | Read all users' profiles | Entire tenant |
| `Mail.Read` | Read all users' mail | Entire tenant |
| `Mail.Send` | Send mail as any user | Entire tenant |
| `Calendars.Read` | Read all users' calendars | Entire tenant |
| `Files.Read.All` | Read all files in OneDrive/SharePoint | Entire tenant |
| `Group.Read.All` | Read all groups | Entire tenant |
| `Directory.Read.All` | Read all directory data | Entire tenant |

---

### Side-by-Side Comparison

| Dimension | Delegated | Application |
|-----------|-----------|-------------|
| User present? | Yes — signed-in user required | No — app acts alone |
| Effective access | App permission ∩ User's own access | Exactly what's granted |
| Consent | User or Admin (depends on permission) | Always Admin |
| OAuth flow | Auth code, OBO, device code | Client credentials only |
| `/me` endpoint | Yes | **No** — must use `/users/{id}` |
| Typical use | Web apps, mobile apps, SPAs | Daemons, background services, cron jobs |
| Data scope | Scoped to the signed-in user's data | Entire tenant (all users) |
| Risk level | Lower — limited to user's access | Higher — tenant-wide access |

---

### Exam Scenario Patterns

**Scenario: "A web app needs to read the signed-in user's calendar"**
→ **Delegated** permission: `Calendars.Read`
→ Flow: Authorization code flow
→ Endpoint: `GET /me/calendar/events`

**Scenario: "A background service needs to read all users' calendars to find room availability"**
→ **Application** permission: `Calendars.Read`
→ Flow: Client credentials
→ Endpoint: `GET /users/{userId}/calendar/events`
→ Requires admin consent

**Scenario: "A middle-tier API receives a token from a frontend app and needs to call Graph on behalf of that user"**
→ **Delegated** permission with **On-Behalf-Of (OBO) flow**
→ The API exchanges the incoming token for a new token scoped to Graph

**Scenario: "A daemon app needs to send weekly report emails from a shared mailbox"**
→ **Application** permission: `Mail.Send`
→ Flow: Client credentials
→ Endpoint: `POST /users/{shared-mailbox}/sendMail`

**Scenario: "An app needs to display the current user's profile photo"**
→ **Delegated** permission: `User.Read`
→ Flow: Authorization code
→ Endpoint: `GET /me/photo/$value`

**Scenario: "You need to limit an application permission so it can only read ONE user's mail, not the entire tenant"**
→ Use **Application Access Policies** (Exchange Online)
→ Create a mail-enabled security group, add the user, scope the app to that group
→ `New-ApplicationAccessPolicy -AppId {id} -PolicyScopeGroupId {groupId} -AccessRight RestrictAccess`
→ This is a niche but testable topic

---

### Token Anatomy — What to Look For

When a question shows you a decoded JWT token, look for these clues:

**Delegated token indicators:**
```json
{
  "aud": "https://graph.microsoft.com",
  "iss": "https://login.microsoftonline.com/{tenant}/v2.0",
  "scp": "User.Read Mail.Read",          ← "scp" = delegated scopes
  "oid": "user-object-id",
  "name": "Albert Smith",
  "preferred_username": "albert@domain.com"
}
```

**Application token indicators:**
```json
{
  "aud": "https://graph.microsoft.com",
  "iss": "https://login.microsoftonline.com/{tenant}/v2.0",
  "roles": ["Mail.Read", "User.Read.All"],  ← "roles" = application permissions
  "oid": "app-service-principal-id",
  "sub": "app-service-principal-id"
  // NO "name", NO "preferred_username", NO "scp"
}
```

**Exam trap:** `scp` (scopes) = delegated. `roles` = application. If a question shows a token with `roles` and asks why `/me` returns 403, the answer is "application tokens have no user context."

---

### Registering Permissions in Entra ID — The Setup

This is the admin workflow that exam questions reference:

1. **App Registration** in Entra ID → **API Permissions** blade
2. Click **Add a permission** → **Microsoft Graph**
3. Choose **Delegated permissions** or **Application permissions**
4. Select specific permissions (e.g., `Mail.Read`)
5. For application permissions (and some delegated): click **Grant admin consent for {tenant}**

Without admin consent for application permissions, the app gets `403 Forbidden` even with a valid token. Exam questions often test this — "the app authenticates successfully but gets 403" → admin hasn't consented.

---

### Least Privilege Principle — Exam Loves This

Microsoft emphasizes requesting the **minimum permissions** needed. Exam questions test whether you pick the narrowest permission:

| If you need to... | Use this, not this |
|-------------------|--------------------|
| Read current user's profile | `User.Read` (not `User.Read.All`) |
| Read current user's mail | `Mail.Read` (not `Mail.ReadWrite`) |
| Send mail as current user | `Mail.Send` (not `Mail.ReadWrite`) |
| Read all users (daemon) | `User.Read.All` application (not `Directory.Read.All`) |

If two permissions both work, pick the one with narrower scope.

---

### Quick Decision Flowchart

```
Is there a signed-in user?
├── YES → Delegated permissions
│   ├── Web app / SPA → Authorization code flow (+ PKCE for SPA)
│   ├── Middle-tier API calling Graph → On-behalf-of flow
│   └── CLI / IoT device → Device code flow
│
└── NO (daemon, background job, scheduled task)
    → Application permissions
    → Client credentials flow
    → MUST use /users/{id}, cannot use /me
    → ALWAYS requires admin consent
```
