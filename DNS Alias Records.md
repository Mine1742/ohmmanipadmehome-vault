#dns 
# Azure DNS Alias Records — Dynamic DNS Updates

## The Problem Alias Records Solve

With traditional (static) DNS records, you hardcode a value into the record — an IP address in an A record, a hostname in a CNAME. If the underlying resource changes (a public IP gets deallocated and reassigned, a VM restarts with a new IP, a load balancer gets recreated), the DNS record is now stale. Someone has to manually update it, and until they do, traffic either blackholes or — worse — lands on a completely different resource that has been assigned the old IP.

This creates two distinct problems:

1. **Stale records** — the DNS record points to an IP that no longer belongs to your resource. This causes outages.
2. **Dangling DNS** — the DNS record points to a deleted resource's former IP. An attacker can claim that IP and receive your traffic. This is a real, exploitable attack vector in Azure.

Standard DNS has no concept of "follow this resource wherever it goes." Records are static strings with a TTL. Azure DNS alias records add that concept within the Azure ecosystem.

---

## How Alias Records Work

An alias record doesn't store a static IP or hostname. Instead, it stores an **Azure Resource Manager (ARM) resource ID** — a direct reference to an Azure resource. When a DNS query arrives, Azure DNS resolves the alias at query time by looking up the current state of the referenced resource and returning its current IP.

### Traditional A record

```
vpn.archkey.com  →  A  →  20.85.1.100   (static, hardcoded)
```

If the public IP resource gets deleted and recreated, the A record still says `20.85.1.100`. It's wrong until someone manually updates it.

### Alias A record

```
vpn.archkey.com  →  ALIAS  →  /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Network/publicIPAddresses/{pip-name}
```

Azure DNS holds a pointer to the public IP _resource_, not the IP _value_. At query time, Azure DNS resolves the resource ID to whatever IP address that resource currently holds and returns it as a normal A record response to the client. The client never sees the alias mechanism — it receives a standard A record answer.

### The resolution flow

```
Client queries vpn.archkey.com (A)
  → Recursive resolver queries Azure DNS authoritative NS
    → Azure DNS sees this is an alias record
    → Azure DNS looks up the ARM resource ID internally
    → ARM returns the current IP of the public IP resource
    → Azure DNS returns that IP as a standard A record response
  → Recursive resolver caches the response per TTL
→ Client receives the IP
```

The alias resolution happens server-side within Azure's infrastructure. There's no extra DNS hop from the client's perspective — it's a single A record answer. The "dynamic" part is that the IP value Azure DNS returns is always the current value of the referenced resource at the moment of the query.

---

## What Alias Records Can Point To

Alias records work with a specific set of Azure resource types:

|Alias target|Supported record types|Use case|
|---|---|---|
|**Azure Public IP**|A, AAAA|VM, Application Gateway, Load Balancer, NVA — anything fronted by a PIP|
|**Azure Traffic Manager profile**|A, AAAA, CNAME|Global load balancing, failover, geographic routing|
|**Azure Front Door**|A, AAAA, CNAME|Global HTTP load balancing, WAF, CDN|
|**Azure CDN endpoint**|A, AAAA, CNAME|Content delivery|
|**Another record set in the same zone**|A, AAAA, CNAME|Internal zone aliasing (one record set follows another)|

Alias records **cannot** point to resources outside Azure (external IPs, on-prem servers, other cloud providers). For those, you still need traditional static records.

---

## Zone Apex Support

This is one of the biggest practical wins. Standard DNS does not allow a CNAME at the zone apex (`archkey.com` with no subdomain) because a CNAME cannot coexist with other record types, and the apex always has SOA and NS records.

This means you can't do:

```
archkey.com  →  CNAME  →  archkey.azurewebsites.net    ← INVALID at apex
```

But you _can_ create an alias A record at the apex that points to a Traffic Manager profile, Front Door, or public IP:

```
archkey.com  →  ALIAS A  →  /subscriptions/.../trafficManagerProfiles/archkey-tm
```

Azure DNS resolves this to a standard A record at query time. Clients and resolvers see a normal A record — no protocol violation, no extra hops.

### Typical zone apex pattern

```
archkey.com         →  Alias A  →  Traffic Manager profile (or Front Door)
www.archkey.com     →  CNAME    →  archkey.com
```

This gives you naked domain support, www support, global load balancing, and automatic failover with just two records.

---

## Dangling DNS Prevention

This is the security feature. With a traditional A record:

1. You create `app.archkey.com → A → 20.85.1.100` pointing to your public IP.
2. Someone deletes the public IP resource (or the VM behind it is deprovisioned).
3. The A record still says `20.85.1.100`.
4. An attacker provisions a new Azure resource and gets assigned `20.85.1.100`.
5. Your DNS now sends your traffic to the attacker's resource.

With an alias record:

1. You create `app.archkey.com → ALIAS → {resource-id-of-your-pip}`.
2. Someone deletes the public IP resource.
3. Azure DNS detects the target resource no longer exists.
4. The alias record becomes an **empty record set** — it stops resolving entirely.
5. Clients get `NXDOMAIN` or `NODATA` instead of being sent to a hijacked IP.

The lifecycle of the DNS record is tightly coupled to the lifecycle of the Azure resource. Delete the resource, and the DNS record effectively self-nullifies.

---

## Creating Alias Records

### Azure CLI

```bash
# Create an alias A record at the zone apex pointing to a public IP
az network dns record-set a create \
  --resource-group rg-dns \
  --zone-name archkey.com \
  --name "@" \
  --target-resource "/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Network/publicIPAddresses/{pip-name}"
```

### PowerShell

```powershell
# Create an alias A record pointing to a public IP
$pip = Get-AzPublicIpAddress -Name "pip-archkey-web" -ResourceGroupName "rg-networking"

New-AzDnsRecordSet -Name "@" `
  -RecordType A `
  -ZoneName "archkey.com" `
  -ResourceGroupName "rg-dns" `
  -TargetResourceId $pip.Id `
  -Ttl 300
```

### Portal

1. Open the DNS zone → **+ Record set**.
2. Set the record type (A, AAAA, or CNAME).
3. Toggle **Alias record set** to **Yes**.
4. Select the **Alias type** (Azure resource or Zone record set).
5. Pick the subscription and target resource.

### Verifying it's an alias

```bash
az network dns record-set a show \
  --resource-group rg-dns \
  --zone-name archkey.com \
  --name "@" \
  --output json
```

If the output contains a `targetResource` field with an ARM resource ID, it's an alias. If it contains an `aRecords` array with IP addresses, it's a standard static record.

---

## Key Constraints and Gotchas

- **Azure resources only.** Alias records cannot point to anything outside Azure. For external targets, use standard records.
- **Cross-subscription requires registration.** If the DNS zone and the target resource are in different subscriptions, both subscriptions must have the `Microsoft.Network` resource provider registered.
- **Traffic Manager + A/AAAA aliases require external endpoints with IPs.** If you alias an A or AAAA record to a Traffic Manager profile, that profile's endpoints must be external endpoints with IPv4/IPv6 addresses — not FQDNs. Use static IPs where possible.
- **TTL is still in play.** The alias resolves dynamically at the authoritative server, but downstream recursive resolvers still cache the answer per the TTL. If the IP changes and a resolver has a cached copy, that resolver won't see the new IP until the TTL expires. Keep TTLs short (300s) on alias records for resources whose IPs may change.
- **No wildcard alias records.** You can't create `*.archkey.com` as an alias.
- **Supported record types only.** Alias records work with A, AAAA, and CNAME record sets. You can't alias an MX, TXT, SRV, or other record type.

---

## Alias Records vs. CNAME vs. Static A

|Behavior|Static A|CNAME|Alias A|
|---|---|---|---|
|Stores|IP address (hardcoded)|Hostname|ARM resource ID|
|Zone apex support|Yes|No|Yes|
|Auto-updates when IP changes|No|N/A (points to hostname)|Yes (at query time)|
|Dangling DNS protection|No|No|Yes (empty set on delete)|
|Extra DNS lookup hop|No|Yes (resolver follows CNAME)|No (resolved server-side)|
|Works with non-Azure targets|Yes|Yes|No|
|Cost|Standard Azure DNS pricing|Standard Azure DNS pricing|Standard Azure DNS pricing (no extra charge)|

---

## Summary

Alias records are Azure DNS's answer to the static nature of traditional DNS. Instead of storing a value, they store a pointer to an Azure resource and resolve it dynamically at query time. The three core benefits are: automatic IP tracking when the underlying resource changes, zone apex support without CNAME protocol violations, and dangling DNS prevention when resources are deleted. The key limitation is that they only work within the Azure ecosystem — anything pointing to a non-Azure target still needs a traditional record.