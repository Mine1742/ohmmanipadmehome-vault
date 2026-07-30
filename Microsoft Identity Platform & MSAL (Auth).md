
# Microsoft Identity Platform & MSAL

This is one of the most conceptually dense topics in AZ-204 because it combines identity theory (OAuth 2.0, OpenID Connect) with practical implementation (MSAL, app registrations, token handling). Once the concepts click together, the implementation becomes straightforward.

---

## The Core Concept

The Microsoft Identity Platform is **Azure AD's developer-facing authentication and authorization service**. It's the system that lets your applications:

- Sign users in with their Microsoft/work/school accounts
- Acquire tokens to call APIs (Microsoft Graph, your own APIs, third-party APIs)
- Control what users and applications can access

Everything flows through **tokens** — specifically two kinds:

**Access Token** — proves that the bearer has permission to access a specific resource. Short-lived (typically 1 hour). Sent in the `Authorization: Bearer <token>` header on API calls.

**Refresh Token** — used to get a new access token when the current one expires. Longer-lived (days to months). Never sent to APIs — only exchanged with the identity platform for new access tokens.

**ID Token** — proves who the user is (authentication). Contains claims about the user (name, email, object ID). Used by the client app, not sent to APIs.

---

## OAuth 2.0 and OpenID Connect — The Foundation

OAuth 2.0 is the **authorization** protocol — it answers "what is this app/user allowed to do?"

OpenID Connect (OIDC) is built on top of OAuth 2.0 and adds **authentication** — it answers "who is this user?"

The identity platform uses both. Know the key roles:

**Resource Owner** — the user who owns the data and grants access.

**Client** — the application requesting access (your app).

**Authorization Server** — the Microsoft identity platform (`login.microsoftonline.com`). Issues tokens.

**Resource Server** — the API being called (Microsoft Graph, your API, etc.). Validates tokens.

---

## App Registration — The Foundation of Everything

Before any OAuth flow can happen, you register your application in Azure AD. This gives it an identity in the directory.

```bash
# Register an application
az ad app create \
  --display-name "MyWebApp" \
  --sign-in-audience AzureADMyOrg \
  --web-redirect-uris "https://myapp.azurewebsites.net/auth/callback" \
                      "http://localhost:5000/auth/callback"

# Get the app ID
APP_ID=$(az ad app list --display-name "MyWebApp" --query [0].appId -o tsv)

# Create a client secret (for confidential clients)
az ad app credential reset \
  --id $APP_ID \
  --append \
  --display-name "Production Secret" \
  --end-date "2025-12-31"

# Add API permissions (e.g., Microsoft Graph User.Read)
az ad app permission add \
  --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \  # Microsoft Graph resource ID
  --api-permissions e1fe6dd8-ba31-4d61-89e7-88639da4683d=Scope  # User.Read scope

# Grant admin consent (for delegated permissions in dev)
az ad app permission grant \
  --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --scope User.Read
```

Key concepts from app registration the exam tests:

**Application (Client) ID** — the unique identifier for your app. Also called `client_id`.

**Tenant ID** — identifies your Azure AD directory. Also called `authority` combined with the base URL.

**Client Secret / Certificate** — credentials used by confidential clients to prove their identity to the authorization server. Secrets are strings; certificates are more secure.

**Redirect URI** — where the authorization server sends the user after authentication. Must be pre-registered — the server rejects requests with unregistered redirect URIs.

**Sign-in Audience** — who can sign into your app:

- `AzureADMyOrg` — only users in your tenant (single-tenant)
- `AzureADMultipleOrgs` — users in any Azure AD tenant (multi-tenant)
- `AzureADandPersonalMicrosoftAccount` — work/school accounts AND personal Microsoft accounts
- `PersonalMicrosoftAccount` — personal accounts only

---

## OAuth 2.0 Flows — Which One to Use When

This is the most heavily tested area. Each flow is designed for a specific scenario.

### Authorization Code Flow (with PKCE)

**Use for:** Web apps and SPAs where a user signs in interactively. The most secure and most common flow for user-facing applications.

```
1. User clicks "Sign In"
2. App redirects to Azure AD:
   GET https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize
       ?client_id=<app-id>
       &response_type=code
       &redirect_uri=https://myapp.com/callback
       &scope=openid profile email User.Read
       &code_challenge=<PKCE-challenge>          ← prevents auth code interception
       &code_challenge_method=S256
       &state=<random-value>                     ← CSRF protection

3. User authenticates and consents

4. Azure AD redirects back with authorization code:
   GET https://myapp.com/callback
       ?code=<authorization-code>
       &state=<same-random-value>

5. App exchanges code for tokens (back-channel, server-to-server):
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
   Body: grant_type=authorization_code
         &code=<authorization-code>
         &redirect_uri=https://myapp.com/callback
         &client_id=<app-id>
         &client_secret=<secret>                 ← confidential clients only
         &code_verifier=<PKCE-verifier>          ← proves same client as step 2

6. Azure AD returns access token, refresh token, ID token
```

**PKCE (Proof Key for Code Exchange)** — required for SPAs and mobile apps where you can't safely store a client secret. The app generates a random `code_verifier`, hashes it to create `code_challenge`, sends the hash in step 2, and sends the original verifier in step 5. Azure AD verifies they match — proving the same client that started the flow is completing it.

### Client Credentials Flow

**Use for:** Daemon applications, background services, microservices — anything that runs without a user present. The app authenticates as itself, not on behalf of a user.

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
Body: grant_type=client_credentials
      &client_id=<app-id>
      &client_secret=<secret>              ← or a certificate assertion
      &scope=https://graph.microsoft.com/.default
```

No user involvement. No authorization code. The app presents its own credentials and gets a token. Used for app-to-app scenarios.

The scope is always `https://<resource>/.default` — this means "all the application permissions that have been granted to this app."

### On-Behalf-Of Flow (OBO)

**Use for:** A middle-tier API that calls another downstream API on behalf of the signed-in user. The user's identity flows through the chain.

```
User → [calls] → API A (with user's access token)
                    → [needs to call] → API B
                    → exchanges user's token for new token scoped to API B
                    → [calls] → API B (with delegated token)
```

```
POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
Body: grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer
      &client_id=<api-a-app-id>
      &client_secret=<api-a-secret>
      &assertion=<user-access-token-received-by-api-a>
      &requested_token_use=on_behalf_of
      &scope=https://api-b.com/read
```

### Device Code Flow

**Use for:** Devices without browsers or with limited input capability — CLI tools, smart TVs, IoT devices.

```
1. App requests a device code:
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode
   Body: client_id=<app-id>&scope=User.Read

2. Azure AD returns:
   {
     "device_code": "BAQABAAEAAAD...",
     "user_code": "ABCDEFGH",
     "verification_uri": "https://microsoft.com/devicelogin",
     "expires_in": 900,
     "interval": 5,
     "message": "Go to https://microsoft.com/devicelogin and enter ABCDEFGH"
   }

3. App displays message to user

4. App polls for token every 5 seconds:
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
   Body: grant_type=urn:ietf:params:oauth:grant-type:device_code
         &device_code=BAQABAAEAAAD...
         &client_id=<app-id>

5. User goes to device login URL on another device, enters ABCDEFGH, authenticates

6. Next poll returns tokens
```

### Implicit Flow (Legacy — avoid)

The old flow for SPAs before PKCE existed. Tokens returned directly in the redirect URI fragment. **Do not use for new applications** — it's less secure than Authorization Code + PKCE. The exam may ask you to identify it and know why it's deprecated.

---

## MSAL — Microsoft Authentication Library

MSAL is the SDK that implements all these flows for you. You never manually construct OAuth requests — MSAL handles the protocol, token caching, refresh, and retry logic.

```bash
# Install for .NET
dotnet add package Microsoft.Identity.Client

# For ASP.NET Core web apps (wraps MSAL)
dotnet add package Microsoft.Identity.Web
dotnet add package Microsoft.Identity.Web.UI
```

### Public vs Confidential Clients

This distinction maps directly to the OAuth flows:

**Public Client** — cannot keep a secret. Mobile apps, desktop apps, SPAs, CLI tools. The user is present. Uses Authorization Code + PKCE or Device Code flow.

**Confidential Client** — can securely store a secret or certificate. Web apps running on a server, daemons, APIs. Uses Authorization Code flow (server-side) or Client Credentials flow.

---

### Confidential Client — ASP.NET Core Web App

```csharp
// Program.cs — web app that signs users in and calls Microsoft Graph
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.UI;

var builder = WebApplication.CreateBuilder(args);

// Microsoft.Identity.Web wraps MSAL and integrates with ASP.NET Core
// Reads config from appsettings.json AzureAd section
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"))
    // Chain: also configure token acquisition to call downstream APIs
    .EnableTokenAcquisitionToCallDownstreamApi(new[] { "User.Read" })
    .AddMicrosoftGraph(builder.Configuration.GetSection("MicrosoftGraph"))
    .AddInMemoryTokenCaches();   // cache tokens in memory (use distributed cache in production)

builder.Services.AddControllersWithViews()
    .AddMicrosoftIdentityUI();   // adds /signin, /signout, /error routes

builder.Services.AddRazorPages();

// Require authentication for all pages by default
builder.Services.AddAuthorization(options =>
{
    options.FallbackPolicy = options.DefaultPolicy;
});

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllerRoute("default", "{controller=Home}/{action=Index}/{id?}");
app.MapRazorPages();

app.Run();
```

```json
// appsettings.json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "your-tenant-id",
    "ClientId": "your-app-client-id",
    "ClientSecret": "your-client-secret",       // or use Key Vault reference
    "CallbackPath": "/auth/callback"
  },
  "MicrosoftGraph": {
    "BaseUrl": "https://graph.microsoft.com/v1.0",
    "Scopes": "User.Read"
  }
}
```

```csharp
// HomeController.cs — using the signed-in user's identity
using Microsoft.Identity.Web;
using Microsoft.Graph;

[Authorize]
public class HomeController : Controller
{
    private readonly GraphServiceClient _graphClient;
    private readonly ITokenAcquisition _tokenAcquisition;

    public HomeController(
        GraphServiceClient graphClient,
        ITokenAcquisition tokenAcquisition)
    {
        _graphClient = graphClient;
        _tokenAcquisition = tokenAcquisition;
    }

    public async Task<IActionResult> Index()
    {
        // Call Microsoft Graph on behalf of the signed-in user
        // MSAL handles token acquisition and refresh automatically
        var user = await _graphClient.Me.GetAsync();

        ViewBag.UserName = user.DisplayName;
        ViewBag.Email = user.Mail;

        return View();
    }

    public async Task<IActionResult> CallCustomApi()
    {
        // Acquire a token for your own downstream API
        string[] scopes = new[] { "api://your-api-client-id/access_as_user" };
        string accessToken = await _tokenAcquisition.GetAccessTokenForUserAsync(scopes);

        // Use the token to call your API
        using var httpClient = new HttpClient();
        httpClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", accessToken);

        var response = await httpClient.GetAsync("https://myapi.azurewebsites.net/api/data");
        var content = await response.Content.ReadAsStringAsync();

        ViewBag.ApiResult = content;
        return View();
    }
}
```

---

### Confidential Client — Daemon / Background Service

```csharp
// DaemonService.cs — app-to-app, no user involved
using Microsoft.Identity.Client;

public class DaemonService
{
    private readonly IConfidentialClientApplication _app;
    private readonly string[] _scopes;

    public DaemonService(IConfiguration config)
    {
        _app = ConfidentialClientApplicationBuilder
            .Create(config["AzureAd:ClientId"])
            .WithClientSecret(config["AzureAd:ClientSecret"])
            // Alternative: use a certificate (more secure than secret)
            // .WithCertificate(certificate)
            .WithAuthority($"https://login.microsoftonline.com/{config["AzureAd:TenantId"]}")
            .Build();

        // .default scope means "all application permissions granted to this app"
        _scopes = new[] { "https://graph.microsoft.com/.default" };
    }

    public async Task<string> GetTokenAsync()
    {
        AuthenticationResult result;

        try
        {
            // Try to get token from cache first (MSAL caches tokens automatically)
            result = await _app.AcquireTokenForClient(_scopes)
                .ExecuteAsync();
        }
        catch (MsalUiRequiredException)
        {
            // Token not in cache — acquire fresh (normal on first call)
            result = await _app.AcquireTokenForClient(_scopes)
                .ExecuteAsync();
        }

        Console.WriteLine($"Token expires: {result.ExpiresOn}");
        Console.WriteLine($"From cache: {result.AuthenticationResultMetadata.TokenSource}");

        return result.AccessToken;
    }

    public async Task CallGraphApiAsync()
    {
        var token = await GetTokenAsync();

        using var httpClient = new HttpClient();
        httpClient.DefaultRequestHeaders.Authorization =
            new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);

        // Call Graph as the application (not on behalf of a user)
        // Requires application permissions (not delegated)
        var response = await httpClient.GetAsync("https://graph.microsoft.com/v1.0/users");
        var content = await response.Content.ReadAsStringAsync();
        Console.WriteLine(content);
    }
}
```

---

### Public Client — Desktop / CLI App

```csharp
// DesktopAuthService.cs
using Microsoft.Identity.Client;

public class DesktopAuthService
{
    private readonly IPublicClientApplication _app;
    private readonly string[] _scopes = { "User.Read", "Files.Read" };

    public DesktopAuthService(string clientId, string tenantId)
    {
        _app = PublicClientApplicationBuilder
            .Create(clientId)
            .WithAuthority($"https://login.microsoftonline.com/{tenantId}")
            // For desktop apps — redirect to localhost
            .WithRedirectUri("http://localhost")
            .Build();

        // Configure token cache persistence (optional but recommended)
        // Without this, users re-authenticate every time the app restarts
        TokenCacheHelper.EnableSerialization(_app.UserTokenCache);
    }

    // ─────────────────────────────────────
    // Try cache first, then interactive
    // This is the standard pattern for desktop apps
    // ─────────────────────────────────────
    public async Task<string> GetTokenAsync()
    {
        AuthenticationResult result;
        var accounts = await _app.GetAccountsAsync();

        try
        {
            // Silent: try to get token from cache or refresh token
            // No user interaction — throws MsalUiRequiredException if not possible
            result = await _app.AcquireTokenSilent(_scopes, accounts.FirstOrDefault())
                .ExecuteAsync();

            Console.WriteLine("Token acquired silently from cache");
        }
        catch (MsalUiRequiredException)
        {
            // Silent failed — need user interaction
            // Falls through to interactive acquisition
            result = await _app.AcquireTokenInteractive(_scopes)
                .WithPrompt(Prompt.SelectAccount)   // always show account picker
                .ExecuteAsync();

            Console.WriteLine("Token acquired interactively");
        }

        return result.AccessToken;
    }

    // Device code flow — for headless/CLI scenarios
    public async Task<string> GetTokenDeviceCodeAsync()
    {
        var result = await _app.AcquireTokenWithDeviceCode(_scopes, deviceCodeResult =>
        {
            // Display the user code and URL to the user
            Console.WriteLine(deviceCodeResult.Message);
            return Task.CompletedTask;
        }).ExecuteAsync();

        return result.AccessToken;
    }

    // Sign out — removes all accounts from cache
    public async Task SignOutAsync()
    {
        var accounts = await _app.GetAccountsAsync();
        foreach (var account in accounts)
        {
            await _app.RemoveAsync(account);
        }
        Console.WriteLine("Signed out");
    }
}
```

---

### Protecting Your Own API

When you build an API that clients call with tokens, your API needs to **validate the incoming token** and check claims.

```csharp
// Program.cs — API that validates tokens from the identity platform
var builder = WebApplication.CreateBuilder(args);

// Validate Bearer tokens from Microsoft identity platform
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization();
builder.Services.AddControllers();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

```csharp
// OrdersController.cs — protecting API endpoints with scopes and roles
using Microsoft.Identity.Web.Resource;

[Authorize]
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    // RequiredScope checks the token's "scp" claim
    // The client must have requested and been granted this scope
    [HttpGet]
    [RequiredScope("orders.read")]
    public async Task<IActionResult> GetOrdersAsync()
    {
        // HttpContext.User contains the claims from the validated token
        var userId = User.FindFirst("oid")?.Value;        // object ID
        var userName = User.FindFirst("name")?.Value;
        var tenantId = User.FindFirst("tid")?.Value;

        return Ok(new { userId, userName, message = "Here are your orders" });
    }

    [HttpPost]
    [RequiredScope("orders.write")]
    public async Task<IActionResult> CreateOrderAsync([FromBody] Order order)
    {
        return Created($"/api/orders/{order.Id}", order);
    }

    // Role-based — checks "roles" claim (application roles, not Azure RBAC)
    [HttpDelete("{id}")]
    [Authorize(Roles = "OrderAdmin")]
    public async Task<IActionResult> DeleteOrderAsync(string id)
    {
        return NoContent();
    }

    // Allow both delegated (user) and app-only (daemon) access
    [HttpGet("all")]
    public async Task<IActionResult> GetAllOrdersAsync()
    {
        // Check if this is a delegated call (user present) or app-only
        bool isAppOnly = !User.Claims.Any(c => c.Type == "scp");

        if (isAppOnly)
        {
            // Verify the app has the right application permission
            if (!User.IsInRole("Orders.ReadAll"))
                return Forbid();
        }

        return Ok(new { isAppOnly, message = "All orders" });
    }
}
```

---

## Scopes — Delegated vs Application Permissions

This is a critical distinction:

**Delegated Permissions (Scopes)** — the app acts on behalf of a signed-in user. The effective permissions are the intersection of what the app is granted AND what the user is allowed to do. Present in the token's `scp` claim.

**Application Permissions (App Roles)** — the app acts as itself, no user involved. The app has whatever permissions were granted, regardless of any user. Present in the token's `roles` claim. Requires admin consent. Used with Client Credentials flow.

```
Delegated:    App has User.Read + user has read access → can read
              App has User.ReadWrite + user has read-only → can only read
              (intersection)

Application:  App has Users.ReadAll → can read all users
              No user in the picture at all
```

---

## Token Claims — What's Inside a Token

Tokens are JWTs (JSON Web Tokens) — base64-encoded JSON with a signature. You can decode them at jwt.ms to inspect claims. Key claims the exam tests:

```json
{
  "aud": "api://your-api-client-id",    // audience — who the token is for
  "iss": "https://login.microsoftonline.com/{tenant}/v2.0", // issuer
  "iat": 1710000000,                    // issued at (Unix timestamp)
  "exp": 1710003600,                    // expiry (1 hour from issue)
  "nbf": 1710000000,                    // not valid before
  "sub": "user-object-id",             // subject — unique user identifier
  "oid": "user-object-id",             // object ID in Azure AD
  "tid": "tenant-id",                  // tenant ID
  "name": "John Smith",                // display name
  "preferred_username": "john@company.com",
  "scp": "orders.read orders.write",   // delegated scopes (space-separated)
  "roles": ["OrderAdmin"],             // application roles
  "ver": "2.0"                         // token version
}
```

Your API validates the token by checking:

- **Signature** — was this token issued by the expected authority?
- **`aud`** — is this token meant for my API?
- **`exp`** — has the token expired?
- **`iss`** — was this issued by the expected tenant?
- **`scp` or `roles`** — does the caller have the required permissions?

---

## Conditional Access and MFA

Conditional Access policies in Azure AD can require MFA, compliant devices, or specific locations before granting tokens. Your MSAL app must handle the `MsalUiRequiredException` that gets thrown when a Conditional Access policy kicks in mid-session:

```csharp
try
{
    result = await _app.AcquireTokenSilent(scopes, account).ExecuteAsync();
}
catch (MsalUiRequiredException ex)
{
    // Could be expired token, MFA required, Conditional Access policy triggered,
    // or consent needed for a new scope
    if (ex.Classification == UiRequiredExceptionClassification.ConsentRequired)
    {
        Console.WriteLine("User needs to consent to new permissions");
    }
    else if (ex.Classification == UiRequiredExceptionClassification.UserPasswordExpired)
    {
        Console.WriteLine("User password expired");
    }

    // Fall back to interactive to let the user satisfy the requirement
    result = await _app.AcquireTokenInteractive(scopes)
        .WithClaims(ex.Claims)   // pass claims challenge from the exception
        .ExecuteAsync();
}
```

---

## Token Caching

MSAL has a built-in token cache that automatically stores and reuses tokens. For web apps handling many users, configure a **distributed cache** (Redis or SQL) so tokens survive app restarts and work across multiple instances.

```csharp
// Program.cs — configure distributed token cache
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"))
    .EnableTokenAcquisitionToCallDownstreamApi()
    .AddDistributedTokenCaches();   // use IDistributedCache

// Configure Redis as the distributed cache backend
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration["RedisConnection"];
    options.InstanceName = "tokens:";
});
```

For desktop/mobile apps, persist the token cache to disk so users don't re-authenticate every launch:

```csharp
// Simple file-based token cache for desktop apps
public static class TokenCacheHelper
{
    private static readonly string CacheFilePath =
        Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
        "myapp.tokenCache");

    private static readonly object FileLock = new();

    public static void EnableSerialization(ITokenCache tokenCache)
    {
        tokenCache.SetBeforeAccess(BeforeAccessNotification);
        tokenCache.SetAfterAccess(AfterAccessNotification);
    }

    private static void BeforeAccessNotification(TokenCacheNotificationArgs args)
    {
        lock (FileLock)
        {
            args.TokenCache.DeserializeMsalV3(
                File.Exists(CacheFilePath)
                    ? File.ReadAllBytes(CacheFilePath)
                    : null);
        }
    }

    private static void AfterAccessNotification(TokenCacheNotificationArgs args)
    {
        if (args.HasStateChanged)
        {
            lock (FileLock)
            {
                File.WriteAllBytes(CacheFilePath,
                    args.TokenCache.SerializeMsalV3());
            }
        }
    }
}
```

---

## Exposing Your API — App Roles and Scopes

When you build an API, you define what permissions clients can request via your app registration.

```bash
# Add a scope to your API app registration
# (defines what delegated permissions clients can request)
az ad app update \
  --id $API_APP_ID \
  --set api.oauth2PermissionScopes='[
    {
      "id": "unique-guid-1",
      "adminConsentDescription": "Read orders on behalf of the user",
      "adminConsentDisplayName": "Read orders",
      "userConsentDescription": "Read your orders",
      "userConsentDisplayName": "Read your orders",
      "isEnabled": true,
      "type": "User",
      "value": "orders.read"
    },
    {
      "id": "unique-guid-2",
      "adminConsentDescription": "Create and modify orders on behalf of the user",
      "adminConsentDisplayName": "Write orders",
      "isEnabled": true,
      "type": "Admin",     // Admin consent required — user cannot consent themselves
      "value": "orders.write"
    }
  ]'

# Add an app role (for application permissions — daemon-to-API)
az ad app update \
  --id $API_APP_ID \
  --set appRoles='[
    {
      "id": "unique-guid-3",
      "allowedMemberTypes": ["Application"],
      "description": "Read all orders (app permission)",
      "displayName": "Read All Orders",
      "isEnabled": true,
      "value": "Orders.ReadAll"
    }
  ]'
```

---

## Microsoft Graph — The Unified API

Microsoft Graph (`https://graph.microsoft.com/v1.0`) is the primary API for accessing Microsoft 365 data — users, groups, emails, calendar, files, Teams, and more. It's a common downstream API target in AZ-204 scenarios.

```csharp
// GraphService.cs — calling Graph with MSAL tokens
using Microsoft.Graph;
using Microsoft.Graph.Models;
using Azure.Identity;

public class GraphService
{
    private readonly GraphServiceClient _graphClient;

    public GraphService()
    {
        // For daemon/background: app-only credential
        var credential = new ClientSecretCredential(
            tenantId: "your-tenant-id",
            clientId: "your-client-id",
            clientSecret: "your-client-secret");

        _graphClient = new GraphServiceClient(credential);
    }

    // Get the signed-in user's profile
    public async Task<User> GetCurrentUserAsync()
    {
        return await _graphClient.Me.GetAsync();
    }

    // List all users in the tenant (requires Users.Read.All app permission)
    public async Task<List<User>> GetAllUsersAsync()
    {
        var users = new List<User>();
        var page = await _graphClient.Users.GetAsync(config =>
        {
            config.QueryParameters.Select = new[] { "id", "displayName", "mail" };
            config.QueryParameters.Top = 100;
        });

        // Graph uses paging — use PageIterator to get all results
        var pageIterator = PageIterator<User, UserCollectionResponse>
            .CreatePageIterator(_graphClient, page, user =>
            {
                users.Add(user);
                return true;   // return false to stop iteration
            });

        await pageIterator.IterateAsync();
        return users;
    }

    // Send an email on behalf of a user (requires Mail.Send delegated permission)
    public async Task SendEmailAsync(string toAddress, string subject, string body)
    {
        await _graphClient.Me.SendMail.PostAsync(new()
        {
            Message = new Message
            {
                Subject = subject,
                Body = new ItemBody
                {
                    ContentType = BodyType.Html,
                    Content = body
                },
                ToRecipients = new List<Recipient>
                {
                    new() { EmailAddress = new EmailAddress { Address = toAddress } }
                }
            }
        });
    }
}
```

---

## Managed Identity vs MSAL — Knowing Which to Use

This trips people up on the exam. The distinction is straightforward once you see it:

**Managed Identity + DefaultAzureCredential** — for **Azure service-to-Azure service** authentication. Your app authenticates to Key Vault, Storage, Cosmos DB, Service Bus. No user involved. No MSAL needed. The identity is the Azure resource itself.

**MSAL** — for **user authentication** or **calling APIs that require OAuth tokens**. Your web app signs users in. Your daemon calls Microsoft Graph. Your API protects its endpoints with Bearer tokens.

```
Azure Function → Key Vault          = Managed Identity (DefaultAzureCredential)
Azure Function → Microsoft Graph    = MSAL (Client Credentials)
Web App → Signs in user             = MSAL (Authorization Code flow)
Web App → Calls your own API        = MSAL (On-Behalf-Of flow)
CLI Tool → Signs in developer       = MSAL (Device Code flow)
```

---

## AZ-204 Exam Summary

The exam focuses heavily on **choosing the right OAuth flow** for a given scenario — know Authorization Code + PKCE for web apps and SPAs, Client Credentials for daemons, On-Behalf-Of for middle-tier APIs, and Device Code for headless apps. You should understand **public vs confidential clients** and what each can safely do. Know the difference between **delegated permissions (scp claim)** and **application permissions (roles claim)** and when admin consent is required. Understand how to **protect an API** using `AddMicrosoftIdentityWebApi` and `RequiredScope`. Know what's inside a JWT token and which claims matter for validation — especially `aud`, `iss`, `exp`, `scp`, and `roles`. Understand **MSAL token caching** — silent acquisition first, interactive as fallback — and why the `MsalUiRequiredException` gets thrown. Finally know when to use **managed identity vs MSAL** — they solve different problems and the exam will present scenarios where you need to pick the right one.

# Managed Identity vs MSAL — When to Use Which

The confusion usually comes from the fact that both involve tokens and Azure AD under the hood. The key is understanding **what is authenticating** and **what it's authenticating to**.

---

## The One-Sentence Rule

**Managed Identity** — an Azure resource proving its own identity to another Azure resource. No humans, no user tokens, no OAuth flows you write.

**MSAL** — a human user or application going through an OAuth flow to get a token, typically to call an API that requires user context or Microsoft Graph.

---

## The Decision Tree

```
Who or what needs to authenticate?
│
├── An Azure resource (App Service, Function, ACI, AKS pod, VM)
│   calling another Azure resource (Key Vault, Storage, Cosmos DB,
│   Service Bus, SQL, your own API registered in Azure AD)
│   └── USE MANAGED IDENTITY + DefaultAzureCredential
│
├── A user signing into a web app or desktop app
│   └── USE MSAL — Authorization Code + PKCE flow
│
├── A background service / daemon calling Microsoft Graph
│   or another API, with no user involved
│   └── DEPENDS:
│       ├── Running in Azure? → Managed Identity if the target supports it
│       └── Calling Graph or an API that needs OAuth client credentials?
│           → USE MSAL — Client Credentials flow
│
├── A middle-tier API calling a downstream API on behalf of a user
│   └── USE MSAL — On-Behalf-Of flow
│
└── A CLI tool or headless device needing a user to sign in
    └── USE MSAL — Device Code flow
```

---

## Side-by-Side Scenarios

### Scenario 1: Azure Function reading a secret from Key Vault

```csharp
// ✅ MANAGED IDENTITY — Azure resource to Azure resource
// No OAuth flow, no MSAL, no credentials anywhere

var client = new SecretClient(
    new Uri("https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential());   // uses managed identity automatically

var secret = await client.GetSecretAsync("MySecret");
```

Why managed identity? Key Vault is an Azure resource. The Function is an Azure resource. Azure handles the token exchange entirely. You just assign the Function's identity the `Key Vault Secrets User` role and the SDK takes care of the rest. No code changes between local dev (uses your `az login`) and production (uses managed identity).

---

### Scenario 2: Azure Function calling Microsoft Graph to read user data

```csharp
// ✅ MSAL — calling an API that requires an OAuth client credentials token
// Graph doesn't support managed identity auth directly for app-level calls

var credential = new ClientSecretCredential(
    tenantId: config["TenantId"],
    clientId: config["ClientId"],
    clientSecret: config["ClientSecret"]);   // store this in Key Vault!

var graphClient = new GraphServiceClient(credential);
var users = await graphClient.Users.GetAsync();
```

Why MSAL here? Microsoft Graph requires an OAuth token with specific application permissions (`Users.Read.All` etc). Your Function needs to present credentials (client ID + secret/certificate) and go through the Client Credentials flow. The credential itself should come from Key Vault via managed identity — so you end up using **both** in the same app:

```csharp
// The elegant pattern: use managed identity to get the secret,
// then use that secret with MSAL to call Graph

// Step 1: Managed identity fetches the client secret from Key Vault
var kvClient = new SecretClient(
    new Uri("https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential());
var clientSecret = await kvClient.GetSecretAsync("GraphClientSecret");

// Step 2: MSAL uses that secret to call Graph
var credential = new ClientSecretCredential(
    config["TenantId"],
    config["ClientId"],
    clientSecret.Value.Value);

var graphClient = new GraphServiceClient(credential);
```

---

### Scenario 3: Web app signs users in and calls your own API

```csharp
// ✅ MSAL — user authentication + delegated API call
// The user's identity needs to flow through

// In Program.cs
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"))
    .EnableTokenAcquisitionToCallDownstreamApi(new[] { "api://myapi/orders.read" })
    .AddInMemoryTokenCaches();

// In a controller — token acquired on behalf of the signed-in user
public async Task<IActionResult> GetMyOrdersAsync()
{
    var token = await _tokenAcquisition
        .GetAccessTokenForUserAsync(new[] { "api://myapi/orders.read" });

    // Call your API with the user's delegated token
    httpClient.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer", token);

    var orders = await httpClient.GetFromJsonAsync<List<Order>>("https://myapi.com/orders");
    return View(orders);
}
```

Why MSAL? A real user is signing in. The downstream API needs to know who the user is and what they're allowed to see. Managed identity can't carry user context — it only represents the Azure resource itself.

---

### Scenario 4: Middle-tier API calling another API on behalf of user

```csharp
// ✅ MSAL — On-Behalf-Of flow
// User token comes in, gets exchanged for a token scoped to the downstream API

[HttpGet]
[Authorize]
public async Task<IActionResult> GetEnrichedOrderAsync(string orderId)
{
    // The user's token arrived in the Authorization header
    // Exchange it for a token scoped to the inventory API
    var userToken = HttpContext.GetTokenAsync("access_token").Result;

    var app = ConfidentialClientApplicationBuilder
        .Create(config["ClientId"])
        .WithClientSecret(config["ClientSecret"])
        .WithAuthority($"https://login.microsoftonline.com/{config["TenantId"]}")
        .Build();

    var result = await app
        .AcquireTokenOnBehalfOf(
            new[] { "api://inventory-api/inventory.read" },
            new UserAssertion(userToken))
        .ExecuteAsync();

    // Now call the inventory API with the new token — user identity preserved
    httpClient.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("Bearer", result.AccessToken);

    var inventory = await httpClient.GetFromJsonAsync<Inventory>(
        $"https://inventoryapi.com/items/{orderId}");

    return Ok(inventory);
}
```

---

### Scenario 5: App Service reading from Azure Blob Storage

```csharp
// ✅ MANAGED IDENTITY — Azure resource to Azure resource
// Assign Storage Blob Data Reader role to the App Service's identity

var blobClient = new BlobServiceClient(
    new Uri("https://mystorageaccount.blob.core.windows.net"),
    new DefaultAzureCredential());

var container = blobClient.GetBlobContainerClient("uploads");
var blob = container.GetBlobClient("myfile.csv");
var content = await blob.DownloadContentAsync();
```

No MSAL. No connection strings. No storage keys. Just a role assignment and one line of credential code that works everywhere.

---

## The Conceptual Summary

Think of it this way — managed identity answers the question **"which Azure resource is this?"** while MSAL answers the question **"who is this user or application, and what are they allowed to do via OAuth?"**

If the thing authenticating is an Azure resource and the thing being called understands Azure RBAC (which most Azure services do — Key Vault, Storage, Cosmos DB, Service Bus, SQL, Event Hubs), use managed identity. It's simpler, more secure, and requires zero credential management.

If a user is involved, or if you're calling an API that requires an explicit OAuth token with specific scopes (Microsoft Graph, your own APIs, third-party OAuth APIs), use MSAL. And when you do use MSAL inside an Azure resource, use managed identity to safely fetch whatever credentials MSAL needs — so you still end up with no secrets hardcoded anywhere.

---

## Quick Reference Card

|Situation|Use|
|---|---|
|Function → Key Vault|Managed Identity|
|Function → Storage|Managed Identity|
|Function → Cosmos DB|Managed Identity|
|Function → Service Bus|Managed Identity|
|Function → SQL (with AAD auth)|Managed Identity|
|Function → Microsoft Graph|MSAL (Client Credentials)|
|Function → Your OAuth-protected API|MSAL (Client Credentials)|
|Web app → Sign in user|MSAL (Auth Code + PKCE)|
|Web app → Call API as user|MSAL (Auth Code + token acquisition)|
|API → Downstream API (user context)|MSAL (On-Behalf-Of)|
|Daemon → Any Azure resource|Managed Identity|
|Daemon → Graph|MSAL (Client Credentials)|
|CLI tool → Sign in developer|MSAL (Device Code)|
|Local dev → Any Azure resource|DefaultAzureCredential (falls back to CLI)|

The pattern that keeps coming up in production: **use managed identity to get secrets, use those secrets with MSAL to do OAuth flows**. The two work together rather than competing.

