
# Azure Key Vault & Managed Identity

These two topics are deeply intertwined — Key Vault is where you store secrets, and Managed Identity is how your Azure resources access them without credentials. Together they form the foundation of **secrets management and zero-credential architecture** in Azure.

---

## The Core Problem They Solve

Every application needs secrets — database connection strings, API keys, certificates, encryption keys. The naive approach is storing them in config files, environment variables, or source code. This is how breaches happen.

The right approach:

```
❌ Naive:    App config file contains "Password=supersecret123"
❌ Better:   App setting contains the password (still a secret in plain text)
✅ Correct:  App has an identity → identity has permission → app fetches secret at runtime
             No human ever handles the secret. Nothing is stored anywhere insecure.
```

Key Vault holds the secrets. Managed Identity is how your app proves who it is to fetch them. No passwords to manage, rotate, or accidentally leak.

---

## Part 1: Azure Key Vault

### What Key Vault Stores

Key Vault stores three distinct types of objects and the exam tests all three:

**Secrets** — any arbitrary string value. Connection strings, API keys, passwords, anything you'd otherwise put in a config file. Stored as name/value pairs with versioning.

**Keys** — cryptographic keys (RSA or EC) used for encryption, decryption, signing, and verification. The private key material **never leaves Key Vault** — you send data to Key Vault and it performs the cryptographic operation and returns the result. You can also use keys stored in HSMs (Hardware Security Modules) for FIPS 140-2 Level 2/3 compliance.

**Certificates** — X.509 certificates with their private keys. Key Vault can manage the full certificate lifecycle — creation, renewal, and integration with CAs like DigiCert and GlobalSign for automatic renewal.

---

### Service Tiers

**Standard** — software-protected keys and secrets. Sufficient for most workloads.

**Premium** — adds HSM-protected keys. Keys are generated and stored in dedicated hardware. Required for regulated industries (finance, healthcare, government).

---

### Creating and Managing Secrets

```bash
# Create a Key Vault
az keyvault create \
  --resource-group myRG \
  --name mykeyvault \
  --location eastus \
  --sku standard \
  --enable-rbac-authorization true   # use RBAC instead of legacy access policies
                                     # RBAC is the recommended model

# Store a secret
az keyvault secret set \
  --vault-name mykeyvault \
  --name "CosmosDBConnection" \
  --value "AccountEndpoint=https://myaccount.documents.azure.com;AccountKey=abc123..."

# Store with expiration date
az keyvault secret set \
  --vault-name mykeyvault \
  --name "ExternalApiKey" \
  --value "sk-live-abc123" \
  --expires "2025-12-31T00:00:00Z"

# Retrieve a secret
az keyvault secret show \
  --vault-name mykeyvault \
  --name "CosmosDBConnection" \
  --query value \
  --output tsv

# List all secrets (names only, not values)
az keyvault secret list --vault-name mykeyvault

# Show a specific version
az keyvault secret show \
  --vault-name mykeyvault \
  --name "CosmosDBConnection" \
  --version "abc123def456..."

# List all versions of a secret
az keyvault secret list-versions \
  --vault-name mykeyvault \
  --name "CosmosDBConnection"

# Soft delete — secrets aren't permanently deleted immediately
az keyvault secret delete \
  --vault-name mykeyvault \
  --name "CosmosDBConnection"

# Purge permanently (only possible after soft delete, or if purge protection disabled)
az keyvault secret purge \
  --vault-name mykeyvault \
  --name "CosmosDBConnection"

# Recover a soft-deleted secret
az keyvault secret recover \
  --vault-name mykeyvault \
  --name "CosmosDBConnection"
```

---

### Access Control: RBAC vs Access Policies

This is a critical distinction for the exam.

**Access Policies (legacy)** — an older model where you grant permissions directly on the vault to a principal (user, group, service principal, managed identity). The permissions are coarse-grained — you grant access to all secrets, all keys, or all certificates in the vault. You can't scope to individual secrets.

**RBAC (recommended)** — uses Azure Role-Based Access Control, the same system used everywhere else in Azure. Supports fine-grained assignments at the vault level or individual secret/key/certificate level. More consistent, more auditable, supports Privileged Identity Management (PIM) for just-in-time access.

Key Vault built-in RBAC roles:

- **Key Vault Administrator** — full management of all vault objects
- **Key Vault Secrets Officer** — create, read, update, delete secrets
- **Key Vault Secrets User** — read secret values only (what apps need)
- **Key Vault Crypto Officer** — manage keys
- **Key Vault Crypto User** — use keys for crypto operations
- **Key Vault Certificate Officer** — manage certificates
- **Key Vault Reader** — read vault metadata, not secret values

```bash
# Grant an app's managed identity permission to read secrets
IDENTITY_PRINCIPAL_ID=$(az identity show \
  --name myappidentity \
  --resource-group myRG \
  --query principalId \
  --output tsv)

VAULT_ID=$(az keyvault show \
  --name mykeyvault \
  --query id \
  --output tsv)

az role assignment create \
  --assignee $IDENTITY_PRINCIPAL_ID \
  --role "Key Vault Secrets User" \
  --scope $VAULT_ID

# Scope to a SINGLE secret (more restrictive)
SECRET_ID=$(az keyvault secret show \
  --vault-name mykeyvault \
  --name "CosmosDBConnection" \
  --query id \
  --output tsv)

az role assignment create \
  --assignee $IDENTITY_PRINCIPAL_ID \
  --role "Key Vault Secrets User" \
  --scope $SECRET_ID
```

---

### Soft Delete and Purge Protection

Two safety features that protect against accidental or malicious deletion:

**Soft Delete** — when you delete a vault or an object, it enters a deleted-but-recoverable state for a configurable retention period (7–90 days, default 90). You can recover it during this window. **Soft delete is now enabled by default on all new vaults and cannot be disabled.**

**Purge Protection** — when enabled, even soft-deleted vaults/objects cannot be permanently purged during the retention period. Not even vault administrators or Microsoft can purge them. Critical for compliance scenarios where you must prove data wasn't tampered with.

```bash
# Enable purge protection (cannot be undone)
az keyvault update \
  --name mykeyvault \
  --enable-purge-protection true \
  --retention-days 90
```

---

### Key Vault Firewall and Network Access

By default Key Vault is accessible from the public internet (authenticated). For production you want to lock this down:

```bash
# Restrict to specific IP ranges and Azure services
az keyvault network-rule add \
  --name mykeyvault \
  --ip-address 203.0.113.0/24

# Allow Azure services (like App Service, Functions) through the firewall
az keyvault update \
  --name mykeyvault \
  --default-action Deny \
  --bypass AzureServices

# Add a VNet rule (requires Microsoft.KeyVault service endpoint on subnet)
az keyvault network-rule add \
  --name mykeyvault \
  --vnet-name myVNet \
  --subnet mySubnet
```

For full network isolation, use a **Private Endpoint** — same pattern as ACR and Cosmos DB private endpoints covered earlier.

---

### .NET SDK — Accessing Key Vault

```bash
dotnet add package Azure.Security.KeyVault.Secrets
dotnet add package Azure.Security.KeyVault.Keys
dotnet add package Azure.Security.KeyVault.Certificates
dotnet add package Azure.Identity
```

```csharp
// KeyVaultService.cs
using Azure.Security.KeyVault.Secrets;
using Azure.Security.KeyVault.Keys;
using Azure.Security.KeyVault.Keys.Cryptography;
using Azure.Security.KeyVault.Certificates;
using Azure.Identity;

public class KeyVaultService
{
    private readonly SecretClient _secretClient;
    private readonly KeyClient _keyClient;
    private readonly CertificateClient _certClient;

    public KeyVaultService(string vaultUri)
    {
        // DefaultAzureCredential tries in order:
        // 1. Environment variables (for CI/CD)
        // 2. Workload identity (for AKS)
        // 3. Managed identity (for Azure-hosted apps)
        // 4. Visual Studio credential (local dev)
        // 5. Azure CLI credential (local dev)
        // 6. Azure PowerShell credential
        // 7. Interactive browser (last resort)
        var credential = new DefaultAzureCredential();

        _secretClient = new SecretClient(new Uri(vaultUri), credential);
        _keyClient = new KeyClient(new Uri(vaultUri), credential);
        _certClient = new CertificateClient(new Uri(vaultUri), credential);
    }

    // ─────────────────────────────────────
    // SECRETS
    // ─────────────────────────────────────

    public async Task<string> GetSecretAsync(string secretName)
    {
        // Gets the current (latest) version
        KeyVaultSecret secret = await _secretClient.GetSecretAsync(secretName);
        return secret.Value;
    }

    public async Task<string> GetSecretVersionAsync(string secretName, string version)
    {
        KeyVaultSecret secret = await _secretClient.GetSecretAsync(secretName, version);
        return secret.Value;
    }

    public async Task SetSecretAsync(string name, string value,
        DateTimeOffset? expiresOn = null)
    {
        var secret = new KeyVaultSecret(name, value);

        if (expiresOn.HasValue)
            secret.Properties.ExpiresOn = expiresOn;

        await _secretClient.SetSecretAsync(secret);
    }

    public async Task<List<SecretProperties>> ListSecretVersionsAsync(string secretName)
    {
        var versions = new List<SecretProperties>();

        // PropertiesOfSecretVersions returns metadata, not values
        await foreach (var version in _secretClient.GetPropertiesOfSecretVersionsAsync(secretName))
        {
            versions.Add(version);
            Console.WriteLine($"Version: {version.Version}, " +
                              $"Created: {version.CreatedOn}, " +
                              $"Enabled: {version.Enabled}");
        }

        return versions;
    }

    public async Task DisableSecretVersionAsync(string name, string version)
    {
        // Disable a specific version without deleting it
        // Useful when rotating secrets — disable old version, keep it for audit
        var properties = (await _secretClient.GetSecretAsync(name, version)).Value.Properties;
        properties.Enabled = false;
        await _secretClient.UpdateSecretPropertiesAsync(properties);
    }

    public async Task DeleteSecretAsync(string secretName)
    {
        // Initiates soft delete — secret goes to deleted state
        var operation = await _secretClient.StartDeleteSecretAsync(secretName);

        // Wait for deletion to complete before trying to purge
        await operation.WaitForCompletionAsync();
    }

    public async Task PurgeSecretAsync(string secretName)
    {
        // Permanently deletes — only possible after soft delete completes
        // Will throw if purge protection is enabled during retention period
        await _secretClient.PurgeDeletedSecretAsync(secretName);
    }

    // ─────────────────────────────────────
    // KEYS — for cryptographic operations
    // ─────────────────────────────────────

    public async Task<KeyVaultKey> CreateRsaKeyAsync(string keyName)
    {
        var options = new CreateRsaKeyOptions(keyName)
        {
            KeySize = 2048,
            KeyOperations =
            {
                KeyOperation.Encrypt,
                KeyOperation.Decrypt,
                KeyOperation.Sign,
                KeyOperation.Verify,
                KeyOperation.WrapKey,
                KeyOperation.UnwrapKey
            },
            ExpiresOn = DateTimeOffset.UtcNow.AddYears(1)
        };

        return await _keyClient.CreateRsaKeyAsync(options);
    }

    public async Task<byte[]> EncryptAsync(string keyName, byte[] plaintext)
    {
        // Get a reference to the key
        KeyVaultKey key = await _keyClient.GetKeyAsync(keyName);

        // Create a CryptographyClient scoped to this key
        // The actual encryption happens INSIDE Key Vault — plaintext is sent to KV,
        // encrypted there, and ciphertext is returned.
        // The private key never leaves the vault.
        var cryptoClient = new CryptographyClient(key.Id, new DefaultAzureCredential());

        EncryptResult result = await cryptoClient.EncryptAsync(
            EncryptionAlgorithm.RsaOaep, plaintext);

        return result.Ciphertext;
    }

    public async Task<byte[]> DecryptAsync(string keyName, byte[] ciphertext)
    {
        KeyVaultKey key = await _keyClient.GetKeyAsync(keyName);
        var cryptoClient = new CryptographyClient(key.Id, new DefaultAzureCredential());

        DecryptResult result = await cryptoClient.DecryptAsync(
            EncryptionAlgorithm.RsaOaep, ciphertext);

        return result.Plaintext;
    }

    public async Task<byte[]> SignAsync(string keyName, byte[] digest)
    {
        KeyVaultKey key = await _keyClient.GetKeyAsync(keyName);
        var cryptoClient = new CryptographyClient(key.Id, new DefaultAzureCredential());

        SignResult result = await cryptoClient.SignAsync(SignatureAlgorithm.RS256, digest);
        return result.Signature;
    }

    public async Task<bool> VerifyAsync(string keyName, byte[] digest, byte[] signature)
    {
        KeyVaultKey key = await _keyClient.GetKeyAsync(keyName);
        var cryptoClient = new CryptographyClient(key.Id, new DefaultAzureCredential());

        VerifyResult result = await cryptoClient.VerifyAsync(
            SignatureAlgorithm.RS256, digest, signature);

        return result.IsValid;
    }

    // ─────────────────────────────────────
    // CERTIFICATES
    // ─────────────────────────────────────

    public async Task<CertificateOperation> CreateSelfSignedCertAsync(string certName)
    {
        var policy = new CertificatePolicy("Self", "CN=myapp.example.com")
        {
            // Auto-renew 30 days before expiry
            LifetimeActions =
            {
                new LifetimeAction(CertificatePolicyAction.AutoRenew)
                {
                    DaysBeforeExpiry = 30
                }
            },
            ValidityInMonths = 12,
            KeySize = 2048,
            KeyType = CertificateKeyType.Rsa,
            // Exportable = true means the private key can be downloaded
            // Set to false for maximum security
            Exportable = false
        };

        return await _certClient.StartCreateCertificateAsync(certName, policy);
    }

    public async Task<X509Certificate2> GetCertificateAsync(string certName)
    {
        KeyVaultCertificateWithPolicy cert =
            await _certClient.GetCertificateAsync(certName);

        // Returns the public portion — private key stays in Key Vault
        return new X509Certificate2(cert.Cer);
    }
}
```

---

### ASP.NET Core Configuration Integration

Rather than calling the SDK manually everywhere, you can integrate Key Vault directly into the .NET configuration system. Secrets become available like any other configuration value.

```csharp
// Program.cs
using Azure.Identity;
using Microsoft.Extensions.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Add Key Vault as a configuration source
// All secrets in the vault become available via IConfiguration
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential());

// Now secrets are accessible anywhere via IConfiguration or IOptions
// Secret named "CosmosDBConnection" → config["CosmosDBConnection"]
// Secret named "ExternalApi--ApiKey" → config["ExternalApi:ApiKey"]
// (double dash in KV secret name maps to colon in config hierarchy)

builder.Services.AddSingleton<CosmosClient>(sp =>
{
    var config = sp.GetRequiredService<IConfiguration>();
    return new CosmosClient(
        config["CosmosDBEndpoint"],
        new DefaultAzureCredential());
});

var app = builder.Build();
```

---

### App Service / Functions Key Vault References

The cleanest approach for App Service and Functions — no SDK changes needed. Set an app setting value to a Key Vault reference syntax and the platform resolves it transparently at startup.

```bash
# Set an app setting that references a Key Vault secret
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings "ConnectionStrings__DefaultConnection=@Microsoft.KeyVault(SecretUri=https://mykeyvault.vault.azure.net/secrets/CosmosDBConnection/)"

# Or reference latest version (no specific version — always gets current)
az webapp config appsettings set \
  --resource-group myRG \
  --name myapp \
  --settings "ApiKey=@Microsoft.KeyVault(VaultName=mykeyvault;SecretName=ExternalApiKey)"
```

Two reference formats:

```
# Format 1 — specific version (pinned)
@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/MySecret/abc123version)

# Format 2 — always latest version (recommended for most cases)
@Microsoft.KeyVault(VaultName=myvault;SecretName=MySecret)
```

The app's **managed identity** must have `Key Vault Secrets User` role on the vault. When the app starts, Azure resolves all Key Vault references and injects the actual secret values as environment variables. Your code sees them as normal config values — no Key Vault SDK needed.

---

## Part 2: Managed Identity

### The Two Types

**System-Assigned Managed Identity**

- Created automatically when you enable it on a resource
- Tied to the lifecycle of that resource — deleted when the resource is deleted
- One-to-one relationship: one identity per resource
- Good for: single-purpose resources, simplicity

**User-Assigned Managed Identity**

- Created as a standalone Azure resource in a resource group
- Independent lifecycle — persists even if the associated resource is deleted
- Can be assigned to multiple resources simultaneously
- Good for: shared permissions across multiple resources, pre-creating identities before resources, consistent identity across redeployments

```bash
# ─────────────────────────────────────
# SYSTEM-ASSIGNED
# ─────────────────────────────────────

# Enable on App Service
az webapp identity assign \
  --resource-group myRG \
  --name myapp

# Enable on Azure Function
az functionapp identity assign \
  --resource-group myRG \
  --name myfunctionapp

# Enable on ACI
az container create \
  --resource-group myRG \
  --name mycontainer \
  --image myapp:latest \
  --assign-identity '[system]'

# Enable on VM
az vm identity assign \
  --resource-group myRG \
  --name myVM

# Get the principal ID to use in role assignments
az webapp identity show \
  --resource-group myRG \
  --name myapp \
  --query principalId \
  --output tsv

# ─────────────────────────────────────
# USER-ASSIGNED
# ─────────────────────────────────────

# Create the identity (standalone resource)
az identity create \
  --resource-group myRG \
  --name myManagedIdentity

# Get its IDs
CLIENT_ID=$(az identity show \
  --name myManagedIdentity \
  --resource-group myRG \
  --query clientId \
  --output tsv)

PRINCIPAL_ID=$(az identity show \
  --name myManagedIdentity \
  --resource-group myRG \
  --query principalId \
  --output tsv)

IDENTITY_ID=$(az identity show \
  --name myManagedIdentity \
  --resource-group myRG \
  --query id \
  --output tsv)

# Assign to App Service
az webapp identity assign \
  --resource-group myRG \
  --name myapp \
  --identities $IDENTITY_ID

# Assign to Function App
az functionapp identity assign \
  --resource-group myRG \
  --name myfunctionapp \
  --identities $IDENTITY_ID

# A resource can have BOTH system-assigned AND one or more user-assigned
az webapp identity assign \
  --resource-group myRG \
  --name myapp \
  --identities '[system]' $IDENTITY_ID
```

---

### How Managed Identity Works Under the Hood

This is worth understanding from first principles rather than just memorizing.

Every Azure compute resource that supports managed identity has access to the **Instance Metadata Service (IMDS)** — a special HTTP endpoint at `http://169.254.169.254` that is only accessible from within the Azure resource itself (not from the internet).

When your code calls `new DefaultAzureCredential()` and makes an authenticated request, here's what actually happens:

```
1. Your code: "I need a token for https://vault.azure.net"
        │
        ▼
2. DefaultAzureCredential calls IMDS:
   GET http://169.254.169.254/metadata/identity/oauth2/token
       ?api-version=2019-08-01
       &resource=https://vault.azure.net
   Header: Metadata: true
        │
        ▼
3. Azure IMDS: "This VM/App/Function has a managed identity.
                Let me get a token from Azure AD on its behalf."
        │
        ▼
4. Azure AD issues a short-lived access token (valid ~1 hour)
        │
        ▼
5. Token returned to your code
        │
        ▼
6. Your code includes token in Authorization header:
   GET https://mykeyvault.vault.azure.net/secrets/MySecret
   Authorization: Bearer eyJ0eXAi...
        │
        ▼
7. Key Vault validates token with Azure AD
   "Is this token valid? Does this identity have Key Vault Secrets User role?"
        │
        ▼
8. Key Vault returns the secret value
```

Your code never sees credentials. No passwords. No rotation. Azure handles steps 2-4 transparently — the SDK does it automatically.

---

### DefaultAzureCredential Chain

```csharp
// DefaultAzureCredential tries each credential type in order
// until one succeeds. This means the same code works:
// - Locally (uses your az login session or VS credentials)
// - In CI/CD (uses environment variables with a service principal)
// - In Azure (uses managed identity)

var credential = new DefaultAzureCredential();

// You can see the order it tries:
// 1. EnvironmentCredential       — AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
// 2. WorkloadIdentityCredential  — for AKS workload identity
// 3. ManagedIdentityCredential   — for Azure-hosted resources
// 4. SharedTokenCacheCredential  — Visual Studio Token Cache
// 5. VisualStudioCredential      — Visual Studio sign-in
// 6. VisualStudioCodeCredential  — VS Code sign-in
// 7. AzureCliCredential          — az login session
// 8. AzurePowerShellCredential   — Connect-AzAccount session
// 9. InteractiveBrowserCredential — browser popup (disabled by default)

// If you want to be explicit about which identity to use
// (e.g., a specific user-assigned identity):
var specificIdentity = new ManagedIdentityCredential(
    clientId: "your-user-assigned-client-id");

// For local dev where you want to force CLI credential:
var cliCredential = new AzureCliCredential();
```

---

### Common Managed Identity Patterns

#### Pattern 1: App Service → Key Vault

```csharp
// Startup: configure Key Vault as config source using managed identity
builder.Configuration.AddAzureKeyVault(
    new Uri("https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential());  // uses managed identity in Azure, CLI locally

// In a controller or service — secret available via normal IConfiguration
public class OrderController : ControllerBase
{
    private readonly string _connectionString;

    public OrderController(IConfiguration config)
    {
        // Resolved from Key Vault transparently
        _connectionString = config["CosmosDBConnection"];
    }
}
```

#### Pattern 2: Azure Function → Storage + Cosmos DB

```csharp
// Program.cs
var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices((context, services) =>
    {
        var credential = new DefaultAzureCredential();

        // Cosmos DB with managed identity — no connection string needed
        services.AddSingleton(new CosmosClient(
            context.Configuration["CosmosDBEndpoint"],
            credential));

        // Blob Storage with managed identity
        services.AddSingleton(new BlobServiceClient(
            new Uri($"https://{context.Configuration["StorageAccountName"]}.blob.core.windows.net"),
            credential));

        // Service Bus with managed identity
        services.AddSingleton(new ServiceBusClient(
            $"{context.Configuration["ServiceBusNamespace"]}.servicebus.windows.net",
            credential));
    })
    .Build();
```

#### Pattern 3: AKS Workload Identity

For AKS, managed identity is handled slightly differently via **Workload Identity** — a Kubernetes service account is federated with an Azure managed identity. This is more complex but the SDK usage is identical.

```csharp
// In your pod, the code is exactly the same
// DefaultAzureCredential automatically detects the workload identity
var client = new SecretClient(
    new Uri("https://mykeyvault.vault.azure.net/"),
    new DefaultAzureCredential());

var secret = await client.GetSecretAsync("MySecret");
```

The configuration happens at the Kubernetes/Azure level — annotating the service account and creating a federated credential. Your application code doesn't change.

---

### Granting Access — The Full Role Assignment Pattern

```csharp
// In Bicep — the complete pattern for App Service + Key Vault + Managed Identity
// This is the most common infrastructure-as-code pattern for the exam

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: 'myappidentity'
  location: resourceGroup().location
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: 'mykeyvault'
  location: resourceGroup().location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true      // use RBAC, not access policies
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'
    }
  }
}

// Key Vault Secrets User role ID — fixed GUID, same in every Azure environment
var kvSecretsUserRoleId = '4633458b-17de-408a-b874-0445c86b69e6'

resource kvRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, identity.id, kvSecretsUserRoleId)
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      kvSecretsUserRoleId)
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource appService 'Microsoft.Web/sites@2022-03-01' = {
  name: 'myapp'
  location: resourceGroup().location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AZURE_CLIENT_ID'
          // Tell DefaultAzureCredential which user-assigned identity to use
          // when multiple are assigned to a resource
          value: identity.properties.clientId
        }
        {
          name: 'CosmosDBConnection'
          value: '@Microsoft.KeyVault(VaultName=mykeyvault;SecretName=CosmosDBConnection)'
        }
      ]
    }
  }
  dependsOn: [kvRoleAssignment]   // don't create app until role is assigned
}
```

---

### Secret Rotation

A common exam scenario — how do you rotate a secret without downtime?

```
Step 1: Generate new credential (e.g., new storage account key)

Step 2: Add as a NEW VERSION of the existing secret in Key Vault
        az keyvault secret set --vault-name mykeyvault --name "StorageKey" --value "<new-key>"
        (Key Vault automatically makes the new version current)

Step 3: App using Key Vault references automatically picks up new version
        on next restart, or within the cache refresh window

Step 4: Revoke the old credential (e.g., regenerate the other storage key,
        invalidating the one you just rotated away from)

Step 5: Disable the old secret version in Key Vault for audit trail
        (don't delete — keep the history)
```

For automated rotation, **Azure Event Grid** can trigger a rotation function when a secret is about to expire. Key Vault fires a `SecretNearExpiry` event 30 days before expiration — you subscribe to it with a Function that generates a new credential and stores it.

---

## Putting It All Together — Zero-Credential Architecture

Here's the full pattern for a production deployment with no secrets stored anywhere except Key Vault:

```
Developer pushes code to GitHub
        │
        ▼
GitHub Actions pipeline runs
  - Authenticates to Azure using Federated Credential (no stored secret)
  - Deploys Bicep template that creates:
      └─ User-Assigned Managed Identity
      └─ Key Vault (with RBAC)
      └─ Role assignment: identity → Key Vault Secrets User
      └─ App Service (with identity assigned)
      └─ App Settings with Key Vault References
        │
        ▼
At runtime, App Service starts
  - App Setting "DB_CONNECTION" resolves from Key Vault via managed identity
  - Application code uses DefaultAzureCredential for all Azure SDK calls
  - No secrets in code, config files, environment variables, or pipelines
  - Everything authenticated through Azure AD tokens
```

---

## Common Mistakes for the Exam

**Using access policies instead of RBAC** — access policies are legacy. The exam expects you to know RBAC is recommended and to know the specific role names (`Key Vault Secrets User` for reading, `Key Vault Secrets Officer` for managing).

**Granting too broad a role** — apps should have `Key Vault Secrets User` (read only), not `Key Vault Administrator`. Least privilege.

**Using system-assigned when user-assigned is better** — if the same identity needs to be shared across multiple resources or pre-created before the resource, use user-assigned.

**Forgetting `AZURE_CLIENT_ID` when multiple user-assigned identities are present** — if a resource has more than one user-assigned identity, `DefaultAzureCredential` needs to know which one to use. Set the `AZURE_CLIENT_ID` environment variable to the client ID of the correct identity.

**Not setting `dependsOn` in Bicep** — role assignments take time to propagate. Always make resources that need the role depend on the role assignment resource.

**Confusing soft delete with purge protection** — soft delete is on by default and lets you recover deleted secrets. Purge protection prevents permanent deletion during the retention period. They're separate settings.

---

## AZ-204 Exam Summary

The exam focuses heavily on the **three types of Key Vault objects** (secrets, keys, certificates) and their use cases, **RBAC vs access policies** and the specific role names, **soft delete and purge protection** and the difference between them, how **Key Vault references in App Service/Functions** work and their two syntax formats, the **two types of managed identity** (system vs user-assigned) and when to use each, how **DefaultAzureCredential** works and its credential chain, how to **grant role assignments** to managed identities in both CLI and Bicep, and the **zero-credential architecture pattern** end to end.

