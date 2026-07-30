# Azure Blob Storage
These two services live under the same Azure Storage Account umbrella but serve very different purposes. Blob Storage is for storing files and data. Storage Queues are a lightweight messaging solution. Together they're foundational services that show up across virtually every Azure architecture.

---

## The Storage Account — The Container for Everything

Before Blob Storage or Queues, there's the **Storage Account** — the top-level Azure resource that houses all storage services. One account can contain blobs, queues, tables, and file shares simultaneously.

```bash
# Create a storage account
az storage account create \
  --resource-group myRG \
  --name mystorageaccount \
  --location eastus \
  --sku Standard_LRS \           # replication type
  --kind StorageV2 \             # general purpose v2 — always use this for new accounts
  --access-tier Hot \            # default blob access tier
  --enable-hierarchical-namespace false  # set true for Data Lake Storage Gen2
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false       # disable anonymous public access
```

### Replication Options

Know these for the exam — they determine how many copies of your data exist and where:

**LRS (Locally Redundant Storage)** — 3 copies within a single datacenter. Cheapest. Protects against hardware failure but not datacenter outage.

**ZRS (Zone Redundant Storage)** — 3 copies across 3 availability zones in one region. Protects against zone failure. Recommended for most production workloads.

**GRS (Geo-Redundant Storage)** — LRS in primary region + asynchronous replication to a secondary region. Protects against full region failure. Secondary is read-only unless failover is initiated.

**GZRS (Geo-Zone Redundant Storage)** — ZRS in primary + async replication to secondary. Best of both worlds. Most resilient, most expensive.

**RA-GRS / RA-GZRS** — same as GRS/GZRS but secondary region is **readable at all times** (not just after failover). Endpoint is `mystorageaccount-secondary.blob.core.windows.net`.

---

## Part 1: Azure Blob Storage

### Core Concept

Blob Storage is **object storage for unstructured data** — files, images, videos, backups, logs, documents, binary data of any kind. Massively scalable, highly durable, and deeply integrated with the rest of Azure.

---

### Data Model

**Storage Account** → **Container** → **Blob**

**Container** — like a folder at the top level. You can't nest containers. Blobs live directly in containers. Access control is configured at the container level.

**Blob** — the actual file. Three types and the exam tests all three:

**Block Blob** — the default and most common type. Optimized for uploading large files efficiently by breaking them into blocks that can be uploaded in parallel. Used for documents, images, videos, logs — most general-purpose scenarios.

**Append Blob** — optimized for append operations. Each write adds to the end. You can't modify existing blocks. Perfect for log files, audit trails, diagnostic data — scenarios where you're continuously adding data.

**Page Blob** — optimized for random read/write access. Made up of 512-byte pages. Used for Azure VM disks (VHD files). Rarely used directly in application development.

---

### Access Tiers

This is heavily tested. Access tiers balance storage cost vs access cost — cheaper to store means more expensive to access.

**Hot** — optimized for frequently accessed data. Highest storage cost, lowest access cost. Default for new blobs.

**Cool** — optimized for infrequently accessed data (at least 30 days). Lower storage cost, higher access cost. 30-day minimum retention — early deletion is charged.

**Cold** — optimized for rarely accessed data (at least 90 days). Lower storage cost than Cool, higher access cost. 90-day minimum retention.

**Archive** — lowest storage cost, highest access cost. Data is **offline** — you must **rehydrate** before you can read it. Rehydration can take hours. 180-day minimum retention.

```bash
# Set default access tier on storage account
az storage account update \
  --name mystorageaccount \
  --resource-group myRG \
  --access-tier Cool

# Set tier on individual blob
az storage blob set-tier \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myblob.csv \
  --tier Archive

# Rehydrate from Archive (must specify priority)
az storage blob set-tier \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myblob.csv \
  --tier Hot \
  --rehydrate-priority Standard   # Standard = up to 15 hours, High = under 1 hour
```

---

### Lifecycle Management Policies

Instead of manually managing tiers, you define rules that automatically transition or delete blobs based on age. This is a key exam topic.

```bash
az storage account management-policy create \
  --account-name mystorageaccount \
  --resource-group myRG \
  --policy '{
    "rules": [
      {
        "name": "logFileLifecycle",
        "enabled": true,
        "type": "Lifecycle",
        "definition": {
          "filters": {
            "blobTypes": ["blockBlob"],
            "prefixMatch": ["logs/"]
          },
          "actions": {
            "baseBlob": {
              "tierToCool": { "daysAfterModificationGreaterThan": 30 },
              "tierToArchive": { "daysAfterModificationGreaterThan": 90 },
              "delete": { "daysAfterModificationGreaterThan": 365 }
            },
            "snapshot": {
              "delete": { "daysAfterCreationGreaterThan": 90 }
            }
          }
        }
      }
    ]
  }'
```

Rules can filter by blob type, prefix, tags, and blob index tags. Actions include tier transitions and deletion. This is how you implement cost-optimized storage at scale without manual intervention.

---

### .NET SDK — Core Operations

```bash
dotnet add package Azure.Storage.Blobs
dotnet add package Azure.Identity
```

```csharp
// BlobStorageService.cs
using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using Azure.Storage.Blobs.Specialized;
using Azure.Identity;

public class BlobStorageService
{
    private readonly BlobServiceClient _serviceClient;

    public BlobStorageService(string accountName)
    {
        // Managed identity — no connection string or key
        _serviceClient = new BlobServiceClient(
            new Uri($"https://{accountName}.blob.core.windows.net"),
            new DefaultAzureCredential());
    }

    // ─────────────────────────────────────
    // CONTAINERS
    // ─────────────────────────────────────

    public async Task<BlobContainerClient> CreateContainerAsync(
        string containerName,
        PublicAccessType accessType = PublicAccessType.None)
    {
        // PublicAccessType.None    — no anonymous access (recommended)
        // PublicAccessType.Blob    — anonymous read for blobs only
        // PublicAccessType.BlobContainer — anonymous read + list
        var container = _serviceClient.GetBlobContainerClient(containerName);
        await container.CreateIfNotExistsAsync(accessType);
        return container;
    }

    public async Task ListContainersAsync()
    {
        await foreach (var container in _serviceClient.GetBlobContainersAsync())
        {
            Console.WriteLine($"Container: {container.Name}, " +
                              $"Last modified: {container.Properties.LastModified}");
        }
    }

    // ─────────────────────────────────────
    // UPLOADING
    // ─────────────────────────────────────

    public async Task UploadBlobAsync(string containerName, string blobName,
        Stream content, string contentType = "application/octet-stream")
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);
        var blob = container.GetBlobClient(blobName);

        var uploadOptions = new BlobUploadOptions
        {
            HttpHeaders = new BlobHttpHeaders
            {
                ContentType = contentType,
                CacheControl = "max-age=3600"
            },
            // Set metadata — key/value pairs stored alongside the blob
            Metadata = new Dictionary<string, string>
            {
                { "uploadedBy", "myapp" },
                { "environment", "production" }
            },
            // Set access tier at upload time
            AccessTier = AccessTier.Hot,
            // Progress reporting for large uploads
            ProgressHandler = new Progress<long>(bytesUploaded =>
                Console.WriteLine($"Uploaded: {bytesUploaded} bytes"))
        };

        await blob.UploadAsync(content, uploadOptions);
        Console.WriteLine($"Uploaded {blobName}");
    }

    // Large file upload — uses parallel block uploads automatically
    public async Task UploadLargeFileAsync(string containerName,
        string blobName, string localFilePath)
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);
        var blob = container.GetBlobClient(blobName);

        var transferOptions = new StorageTransferOptions
        {
            // Max size of each block (4MB default, up to 4000MB)
            MaximumTransferSize = 4 * 1024 * 1024,
            // How many blocks to upload in parallel
            MaximumConcurrency = 4
        };

        using var fileStream = File.OpenRead(localFilePath);
        await blob.UploadAsync(fileStream, transferOptions: transferOptions);
    }

    // ─────────────────────────────────────
    // DOWNLOADING
    // ─────────────────────────────────────

    public async Task<Stream> DownloadBlobAsync(string containerName, string blobName)
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);
        var blob = container.GetBlobClient(blobName);

        BlobDownloadStreamingResult result = await blob.DownloadStreamingAsync();
        return result.Content;
    }

    public async Task DownloadToFileAsync(string containerName,
        string blobName, string localPath)
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);
        var blob = container.GetBlobClient(blobName);

        await blob.DownloadToAsync(localPath);
    }

    // ─────────────────────────────────────
    // LISTING BLOBS
    // ─────────────────────────────────────

    public async Task ListBlobsAsync(string containerName, string prefix = null)
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);

        // Flat listing — all blobs regardless of virtual directory structure
        await foreach (var blob in container.GetBlobsAsync(
            traits: BlobTraits.Metadata,
            states: BlobStates.All,   // includes snapshots and uncommitted blobs
            prefix: prefix))
        {
            Console.WriteLine($"Name: {blob.Name}, " +
                              $"Size: {blob.Properties.ContentLength}, " +
                              $"Tier: {blob.Properties.AccessTier}, " +
                              $"LastModified: {blob.Properties.LastModified}");
        }
    }

    // Hierarchical listing — respects virtual directory structure using /
    public async Task ListBlobsHierarchicalAsync(string containerName, string prefix = "")
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);

        // GetBlobsByHierarchyAsync returns both blobs and virtual directories (prefixes)
        await foreach (var item in container.GetBlobsByHierarchyAsync(
            delimiter: "/", prefix: prefix))
        {
            if (item.IsPrefix)
                Console.WriteLine($"[DIR] {item.Prefix}");
            else
                Console.WriteLine($"[BLOB] {item.Blob.Name}");
        }
    }

    // ─────────────────────────────────────
    // BLOB PROPERTIES AND METADATA
    // ─────────────────────────────────────

    public async Task GetBlobPropertiesAsync(string containerName, string blobName)
    {
        var blob = _serviceClient
            .GetBlobContainerClient(containerName)
            .GetBlobClient(blobName);

        BlobProperties props = await blob.GetPropertiesAsync();

        Console.WriteLine($"ContentType: {props.ContentType}");
        Console.WriteLine($"ContentLength: {props.ContentLength}");
        Console.WriteLine($"ETag: {props.ETag}");
        Console.WriteLine($"LastModified: {props.LastModified}");
        Console.WriteLine($"AccessTier: {props.AccessTier}");
        Console.WriteLine($"LeaseState: {props.LeaseState}");
        Console.WriteLine($"BlobType: {props.BlobType}");

        foreach (var meta in props.Metadata)
            Console.WriteLine($"Metadata: {meta.Key} = {meta.Value}");
    }

    public async Task SetMetadataAsync(string containerName,
        string blobName, Dictionary<string, string> metadata)
    {
        var blob = _serviceClient
            .GetBlobContainerClient(containerName)
            .GetBlobClient(blobName);

        // SetMetadata REPLACES all existing metadata
        // Read first if you want to merge
        await blob.SetMetadataAsync(metadata);
    }

    // ─────────────────────────────────────
    // COPY, DELETE, AND MANAGE
    // ─────────────────────────────────────

    public async Task CopyBlobAsync(string sourceContainer, string sourceBlob,
        string destContainer, string destBlob)
    {
        var source = _serviceClient
            .GetBlobContainerClient(sourceContainer)
            .GetBlobClient(sourceBlob);

        var dest = _serviceClient
            .GetBlobContainerClient(destContainer)
            .GetBlobClient(destBlob);

        // Server-side copy — no data leaves Azure
        var operation = await dest.StartCopyFromUriAsync(source.Uri);

        // Wait for copy to complete
        await operation.WaitForCompletionAsync();
        Console.WriteLine($"Copy status: {operation.HasCompleted}");
    }

    public async Task DeleteBlobAsync(string containerName, string blobName,
        bool includeSnapshots = true)
    {
        var blob = _serviceClient
            .GetBlobContainerClient(containerName)
            .GetBlobClient(blobName);

        await blob.DeleteAsync(
            includeSnapshots
                ? DeleteSnapshotsOption.IncludeSnapshots
                : DeleteSnapshotsOption.None);
    }
}
```

---

### Snapshots and Versioning

Two mechanisms for preserving blob history — both are testable.

**Snapshots** — a read-only, point-in-time copy of a blob you take manually. Identified by a DateTime timestamp appended to the blob URI. You pay only for the delta between the snapshot and the current blob.

**Versioning** — when enabled on the storage account, Azure **automatically** preserves every previous version of a blob whenever it's overwritten or deleted. Each version gets a unique version ID. More powerful than snapshots for audit and recovery scenarios.

```csharp
public class SnapshotAndVersioningDemo
{
    private readonly BlobServiceClient _serviceClient;

    public SnapshotAndVersioningDemo(BlobServiceClient client)
    {
        _serviceClient = client;
    }

    // ─────────────────────────────────────
    // SNAPSHOTS — manual point-in-time copy
    // ─────────────────────────────────────
    public async Task CreateAndUseSnapshotsAsync()
    {
        var blob = _serviceClient
            .GetBlobContainerClient("mycontainer")
            .GetBlobClient("myfile.txt");

        // Create a snapshot
        BlobSnapshotInfo snapshot = await blob.CreateSnapshotAsync();
        Console.WriteLine($"Snapshot created at: {snapshot.Snapshot}");

        // Access a specific snapshot
        // Snapshot is identified by its DateTime string appended to URI
        BlobClient snapshotBlob = blob.WithSnapshot(snapshot.Snapshot);
        BlobDownloadStreamingResult content = await snapshotBlob.DownloadStreamingAsync();

        // Promote snapshot to base blob (restore to that point in time)
        await blob.StartCopyFromUriAsync(snapshotBlob.Uri);

        // List all snapshots of a blob
        var container = _serviceClient.GetBlobContainerClient("mycontainer");
        await foreach (var item in container.GetBlobsAsync(
            states: BlobStates.Snapshots,
            prefix: "myfile.txt"))
        {
            Console.WriteLine($"Snapshot: {item.Snapshot}, " +
                              $"Created: {item.Properties.LastModified}");
        }
    }

    // ─────────────────────────────────────
    // VERSIONING — automatic version history
    // (must be enabled at storage account level)
    // ─────────────────────────────────────
    public async Task UseVersioningAsync()
    {
        var blob = _serviceClient
            .GetBlobContainerClient("mycontainer")
            .GetBlobClient("myfile.txt");

        // Each upload automatically creates a new version
        await blob.UploadAsync(BinaryData.FromString("version 1"), overwrite: true);
        await blob.UploadAsync(BinaryData.FromString("version 2"), overwrite: true);
        await blob.UploadAsync(BinaryData.FromString("version 3"), overwrite: true);

        // List all versions
        var container = _serviceClient.GetBlobContainerClient("mycontainer");
        await foreach (var item in container.GetBlobsAsync(
            states: BlobStates.Version,
            prefix: "myfile.txt"))
        {
            Console.WriteLine($"VersionId: {item.VersionId}, " +
                              $"IsCurrent: {item.IsCurrentVersion}");
        }

        // Access a specific version
        BlobClient versionedBlob = blob.WithVersion("2024-03-15T10:30:00.0000000Z");
        var versionContent = await versionedBlob.DownloadContentAsync();
        Console.WriteLine(versionContent.Value.Content.ToString());
    }
}
```

---

### Leases — Distributed Locking

Leases give you **exclusive write access** to a blob or container for a period of time. Used to implement distributed locks — only one process can modify the blob while the lease is held.

```csharp
public async Task LeaseDemo()
{
    var blob = _serviceClient
        .GetBlobContainerClient("mycontainer")
        .GetBlobClient("shared-resource.json");

    // Get a lease client
    var leaseClient = blob.GetBlobLeaseClient();

    // Acquire a 30-second lease (15-60 seconds, or -1 for infinite)
    BlobLease lease = await leaseClient.AcquireAsync(TimeSpan.FromSeconds(30));
    Console.WriteLine($"Lease acquired: {lease.LeaseId}");

    try
    {
        // Only the holder of the lease ID can modify the blob
        var uploadOptions = new BlobUploadOptions
        {
            Conditions = new BlobRequestConditions
            {
                LeaseId = lease.LeaseId   // must provide lease ID or upload fails
            }
        };

        await blob.UploadAsync(
            BinaryData.FromString("updated content"),
            uploadOptions);

        // Renew before it expires if processing takes longer
        await leaseClient.RenewAsync();
    }
    finally
    {
        // Always release the lease when done
        await leaseClient.ReleaseAsync();
        Console.WriteLine("Lease released");
    }
}
```

---

### Shared Access Signatures (SAS)

SAS tokens grant **time-limited, scoped access** to storage resources without sharing account keys. Critical for the exam.

Three types:

**Service SAS** — scoped to a specific service (Blob, Queue, Table, File) and resource within it.

**Account SAS** — scoped to one or more storage services at the account level.

**User Delegation SAS** — uses Azure AD credentials instead of account keys. More secure — recommended for production.

```csharp
public class SasDemo
{
    private readonly BlobServiceClient _serviceClient;
    private readonly StorageSharedKeyCredential _sharedKeyCredential;

    public SasDemo(string accountName, string accountKey)
    {
        _sharedKeyCredential = new StorageSharedKeyCredential(accountName, accountKey);
        _serviceClient = new BlobServiceClient(
            new Uri($"https://{accountName}.blob.core.windows.net"),
            _sharedKeyCredential);
    }

    // Service SAS — for sharing a single blob with an external party
    public Uri GenerateBlobSasUri(string containerName, string blobName)
    {
        var blob = _serviceClient
            .GetBlobContainerClient(containerName)
            .GetBlobClient(blobName);

        var sasBuilder = new BlobSasBuilder
        {
            BlobContainerName = containerName,
            BlobName = blobName,
            Resource = "b",                          // "b" for blob, "c" for container
            ExpiresOn = DateTimeOffset.UtcNow.AddHours(1),
            ContentDisposition = "attachment; filename=myfile.csv"  // forces download
        };

        // Grant read permission only
        sasBuilder.SetPermissions(BlobSasPermissions.Read);

        // Generate the SAS URI
        Uri sasUri = blob.GenerateSasUri(sasBuilder);
        Console.WriteLine($"SAS URI: {sasUri}");
        return sasUri;
    }

    // Container SAS — for granting access to all blobs in a container
    public Uri GenerateContainerSasUri(string containerName)
    {
        var container = _serviceClient.GetBlobContainerClient(containerName);

        var sasBuilder = new BlobSasBuilder
        {
            BlobContainerName = containerName,
            Resource = "c",                          // "c" for container
            ExpiresOn = DateTimeOffset.UtcNow.AddDays(7)
        };

        // Read and list permissions
        sasBuilder.SetPermissions(
            BlobSasPermissions.Read |
            BlobSasPermissions.List);

        return container.GenerateSasUri(sasBuilder);
    }

    // User delegation SAS — uses Azure AD, more secure than key-based SAS
    public async Task<Uri> GenerateUserDelegationSasAsync(
        string containerName, string blobName)
    {
        // Get user delegation key (valid up to 7 days)
        // Requires Storage Blob Delegator role on the storage account
        var delegationKey = await _serviceClient.GetUserDelegationKeyAsync(
            DateTimeOffset.UtcNow,
            DateTimeOffset.UtcNow.AddDays(1));

        var sasBuilder = new BlobSasBuilder
        {
            BlobContainerName = containerName,
            BlobName = blobName,
            Resource = "b",
            ExpiresOn = DateTimeOffset.UtcNow.AddHours(2)
        };

        sasBuilder.SetPermissions(BlobSasPermissions.Read | BlobSasPermissions.Write);

        // Build URI with user delegation key instead of account key
        var blobUri = new Uri(
            $"https://{_serviceClient.AccountName}.blob.core.windows.net/" +
            $"{containerName}/{blobName}");

        var sasQueryParams = sasBuilder.ToSasQueryParameters(
            delegationKey,
            _serviceClient.AccountName);

        return new UriBuilder(blobUri) { Query = sasQueryParams.ToString() }.Uri;
    }
}
```

---

### Stored Access Policies

Instead of embedding permissions directly in a SAS token, you can define a **Stored Access Policy** on a container. The SAS token references the policy by name. This lets you **revoke access** by modifying or deleting the policy — without needing to reissue tokens.

```csharp
public async Task StoredAccessPolicyDemo()
{
    var container = _serviceClient.GetBlobContainerClient("mycontainer");

    // Create a stored access policy
    var policies = new List<BlobSignedIdentifier>
    {
        new BlobSignedIdentifier
        {
            Id = "readPolicy",                    // policy name referenced in SAS
            AccessPolicy = new BlobAccessPolicy
            {
                PolicyStartsOn = DateTimeOffset.UtcNow,
                PolicyExpiresOn = DateTimeOffset.UtcNow.AddDays(30),
                Permissions = "r"                 // read only
            }
        },
        new BlobSignedIdentifier
        {
            Id = "writePolicy",
            AccessPolicy = new BlobAccessPolicy
            {
                PolicyStartsOn = DateTimeOffset.UtcNow,
                PolicyExpiresOn = DateTimeOffset.UtcNow.AddDays(7),
                Permissions = "rw"                // read and write
            }
        }
    };

    await container.SetAccessPolicyAsync(accessPolicy: policies);

    // Create a SAS that references the policy
    var sasBuilder = new BlobSasBuilder
    {
        BlobContainerName = "mycontainer",
        Resource = "c",
        Identifier = "readPolicy"              // reference policy by ID
        // No ExpiresOn — policy controls it
        // No permissions — policy controls those too
    };

    var sasUri = container.GenerateSasUri(sasBuilder);

    // To revoke: delete or modify the "readPolicy" stored access policy
    // All SAS tokens referencing it immediately become invalid
}
```

---

### Append Blob — Logging Pattern

```csharp
public class AppendBlobLogger
{
    private readonly AppendBlobClient _appendBlob;

    public AppendBlobLogger(string accountName, string containerName, string blobName)
    {
        var serviceClient = new BlobServiceClient(
            new Uri($"https://{accountName}.blob.core.windows.net"),
            new DefaultAzureCredential());

        // GetAppendBlobClient gives you append-specific operations
        _appendBlob = serviceClient
            .GetBlobContainerClient(containerName)
            .GetAppendBlobClient(blobName);
    }

    public async Task InitializeAsync()
    {
        // Create the append blob if it doesn't exist
        await _appendBlob.CreateIfNotExistsAsync();
    }

    public async Task LogAsync(string message)
    {
        var logEntry = $"{DateTime.UtcNow:O} | {message}\n";
        var bytes = Encoding.UTF8.GetBytes(logEntry);

        using var stream = new MemoryStream(bytes);

        // AppendBlock adds to the END — can never modify previous blocks
        // Max 4MB per append, max 50,000 blocks per blob
        await _appendBlob.AppendBlockAsync(stream);
    }
}
```

---

### Blob Index Tags

Blob index tags let you **tag blobs with key-value pairs and query across them** — unlike metadata which isn't searchable. Useful for content management and discovery.

```csharp
public async Task BlobIndexTagsDemo()
{
    var blob = _serviceClient
        .GetBlobContainerClient("mycontainer")
        .GetBlobClient("myfile.csv");

    // Set index tags (searchable unlike metadata)
    await blob.SetTagsAsync(new Dictionary<string, string>
    {
        { "project", "az204-study" },
        { "status", "processed" },
        { "year", "2024" }
    });

    // Find blobs by tag across an entire storage account
    // Requires Storage Blob Data Reader role
    string query = @"""project"" = 'az204-study' AND ""status"" = 'processed'";

    await foreach (var taggedBlob in _serviceClient.FindBlobsByTagsAsync(query))
    {
        Console.WriteLine($"Found: {taggedBlob.BlobName} in {taggedBlob.BlobContainerName}");
    }
}
```

---



## AZ-204 Exam Summary

For **Blob Storage** the exam focuses on the **three blob types** (Block, Append, Page) and their use cases, **access tiers** (Hot/Cool/Cold/Archive) and their trade-offs including minimum retention periods, **lifecycle management policies** for automating tier transitions, **SAS tokens** — the three types (Service, Account, User Delegation), how to generate them, and why stored access policies are better for revocability, **leases** for distributed locking, the difference between **snapshots and versioning**, and using **DefaultAzureCredential** for managed identity access instead of connection strings or keys.

For **Storage Queues** the exam focuses on the **comparison with Service Bus** and when to use each, the **receive/delete pattern** with `messageId` and `popReceipt`, the **visibility timeout** concept and why messages reappear if not deleted, handling **poison messages** with `DequeueCount`, and how **Azure Functions Queue trigger** simplifies consumption.

Want practice scenario questions on this, or shall we move to the next topic?