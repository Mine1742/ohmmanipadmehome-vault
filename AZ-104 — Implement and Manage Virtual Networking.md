
# AZ-104 — Implement and Manage Virtual Networking

## Comprehensive Study Guide

> **Exam weight:** 15–20% of AZ-104 (roughly 8–12 questions out of ~55) **Official domain:** "Implement and manage virtual networking" **Difficulty:** Widely considered the hardest AZ-104 domain — multi-step configs, NSG priority logic, peering constraints, and DNS topology questions all appear here.

---

## Domain Map (What Microsoft Tests)

The official objectives break into three sub-domains:

```
Implement and Manage Virtual Networking (15–20%)
│
├── 1. Configure and manage virtual networks in Azure
│   ├── Create and configure VNets and subnets
│   ├── Create and configure VNet peering
│   ├── Configure public IP addresses
│   ├── Configure user-defined routes (UDRs)
│   └── Troubleshoot network connectivity
│
├── 2. Configure secure access to virtual networks
│   ├── Create and configure NSGs and ASGs
│   ├── Evaluate effective security rules in NSGs
│   ├── Implement Azure Bastion
│   ├── Configure Service Endpoints for PaaS
│   └── Configure Private Endpoints for PaaS
│
└── 3. Configure name resolution and load balancing
    ├── Configure Azure DNS
    ├── Configure internal or public load balancer
    └── Troubleshoot load balancing
```

---

## Section 1 — Virtual Networks and Subnets

### What is a VNet?

A Virtual Network (VNet) is the fundamental networking building block in Azure. It is a logically isolated network in the Azure cloud that you control. Resources inside a VNet can communicate with each other by default; communication outside requires explicit configuration.

Key properties of a VNet:

- Scoped to a **single Azure region** (cannot span regions)
- Scoped to a **single subscription**
- Defined by one or more **address spaces** (CIDR blocks, e.g. `10.0.0.0/16`)
- Divided into **subnets** that carve up the address space
- Free to create; you pay for gateways, public IPs, and traffic egress

### Address Space Rules

- Use private RFC 1918 ranges: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- Address spaces cannot overlap between peered VNets — this is the #1 peering failure cause
- You can **add** address spaces to an existing VNet without downtime
- You cannot **remove** an address space while subnets are using it

### Subnets

A subnet is a range within the VNet address space assigned to a group of resources. Rules:

- Each subnet must fall within the VNet address space
- Subnets within the same VNet cannot overlap
- Azure reserves **5 IP addresses** per subnet (first 4 + last 1):
    - `.0` — Network address
    - `.1` — Default gateway (Azure reserved)
    - `.2`, `.3` — Azure DNS
    - `.255` — Broadcast
- Minimum usable subnet: `/29` gives 3 usable IPs
- For production workloads, use `/24` or larger

#### Special-purpose subnets (must use exact names)

|Name|Purpose|Min Size|
|---|---|---|
|`GatewaySubnet`|VPN / ExpressRoute Gateway|/27 (recommend /26)|
|`AzureFirewallSubnet`|Azure Firewall|/26|
|`AzureBastionSubnet`|Azure Bastion|/26|
|`RouteServerSubnet`|Azure Route Server|/27|

### Exam tips — VNets and subnets

- A VNet is **regional** — to connect VNets across regions, use global VNet peering
- You can resize a subnet only if no resources are deployed in it (usually)
- A VM NIC is assigned to a subnet, not directly to a VNet
- Multiple NICs on a VM can be in different subnets of the **same** VNet only

---

## Section 2 — VNet Peering

### What it does

VNet peering connects two VNets so resources in each can communicate using private IPs, over the Azure backbone (not the internet). Traffic is low-latency and high-bandwidth.

**Two types:**

- **Regional peering** — both VNets in the same region
- **Global peering** — VNets in different regions (same or different subscriptions)

### Key peering properties

|Property|Detail|
|---|---|
|**Non-transitive**|VNet A ↔ B and B ↔ C does NOT mean A ↔ C|
|**Bidirectional setup**|Must create a peering from A→B AND from B→A|
|**No address overlap**|Peered VNets must have non-overlapping address spaces|
|**No gateway in path**|Peered traffic does not traverse a VPN/ER gateway by default|
|**Reciprocal deletion**|Deleting one side leaves the other side in a "Disconnected" state|

### Peering settings (configured on each side)

|Setting|What it does|
|---|---|
|**Allow virtual network access**|Enables traffic between the two VNets (default: on)|
|**Allow forwarded traffic**|Allows traffic _forwarded_ from a third VNet through this peering|
|**Allow gateway transit**|Hub side: lets spokes use the hub's gateway|
|**Use remote gateways**|Spoke side: use the hub's gateway for on-prem connectivity|

#### Gateway transit pattern (hub-spoke)

```
On-Prem ──── VPN Gateway (hub VNet)
                    │ peering: "Allow gateway transit" = ON
              Hub VNet
                /       \
          Spoke1         Spoke2
  peering: "Use remote    peering: "Use remote
   gateways" = ON         gateways" = ON
```

Spokes can now reach on-prem via hub's VPN gateway without their own gateway.

### Transitivity workaround

Since peering is non-transitive, to enable A ↔ C communication through B, you need one of:

- Direct A ↔ C peering
- An NVA or Azure Firewall in B that routes A→C traffic (and UDRs to steer traffic through it)
- Azure Virtual WAN (managed hub that provides transitivity)

### Exam tips — peering

- Peering link state: **Initiated** (one side done), **Connected** (both sides done), **Disconnected** (other side deleted)
- Changing address space on a peered VNet requires **re-syncing** the peering
- Global peering has **same functionality** as regional peering but may have higher latency
- Peering is **not free** — you pay for data transferred across peerings

---

## Section 3 — Public IP Addresses

### SKUs

|Feature|Basic|Standard|
|---|---|---|
|Assignment|Static or Dynamic|Static only|
|Zone redundancy|No|Yes (zone-redundant by default)|
|Inbound flows|Open by default|Closed by default (NSG required)|
|Supports|Load Balancer Basic, VPN GW|Load Balancer Standard, App GW, Firewall, Bastion, NAT GW|
|Routing preference|Microsoft network|Microsoft network or Internet|

> **Standard is the current default and what the exam tests.** Basic is being retired — do not design new solutions with it.

### Public IP allocation

- **Static** — IP is assigned at creation and never changes (even when VM is deallocated)
- **Dynamic** (Basic only) — IP may change when resource is deallocated/restarted

### IP prefixes

- A reserved contiguous block of public IPs (`/28` to `/31`)
- All IPs share the same prefix — useful for firewall allowlisting
- IPs in a prefix are all Standard SKU

### Exam tips — public IPs

- Standard public IPs are **zone-redundant by default** — no extra configuration needed
- A Standard public IP **requires an NSG** to allow inbound traffic (Basic allows all by default)
- Public IPs are **regional** resources — you cannot move them between regions directly
- You can **disassociate** a public IP from a resource without deleting it

---

## Section 4 — User-Defined Routes (UDRs)

### How Azure routing works

Azure automatically creates a system route table for each subnet with these default routes:

|Address prefix|Next hop type|Description|
|---|---|---|
|VNet address space|Virtual network|Local VNet traffic|
|`0.0.0.0/0`|Internet|Default internet route|
|`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`|None|Drop RFC 1918 not in VNet|

### User-Defined Routes

You create a **Route Table** resource, add custom routes, and **associate it with subnets**. UDR routes override system routes for the same prefix (longest prefix match still applies).

**Next hop types:**

- `Virtual network gateway` — send to VPN/ER gateway
- `Virtual network` — within the VNet
- `Internet` — send to public internet
- `Virtual appliance` — send to an NVA's private IP (most common UDR use case)
- `None` — drop the traffic (black hole)

### Common UDR scenarios

**Force traffic through Azure Firewall:**

```
Route Table: "spoke-rt"
  Route: 0.0.0.0/0 → Next hop: Virtual appliance → 10.0.0.4 (Firewall private IP)
Associate with: all spoke subnets
```

**Prevent gateway subnet from sending spoke traffic back through firewall (avoid routing loops):**

```
Route Table: "gateway-rt"
  Route: 10.1.0.0/16 (spoke1) → Next hop: Virtual appliance → 10.0.0.4 (Firewall)
  Route: 10.2.0.0/16 (spoke2) → Next hop: Virtual appliance → 10.0.0.4 (Firewall)
Associate with: GatewaySubnet
```

### BGP route propagation

Route tables have a **"Propagate gateway routes"** setting:

- **Enabled (default):** Routes learned by the VPN/ER gateway (on-prem routes) are automatically added to the subnet's route table
- **Disabled:** Suppress gateway route propagation — useful when you want ALL traffic (including on-prem-destined) to go through a firewall first

### Exam tips — UDRs

- UDRs are associated with **subnets**, not VNets or NICs
- One route table can be associated with **multiple subnets**
- One subnet can only have **one route table** associated
- Longest prefix match always wins: a `/32` UDR beats a `/0` system route
- You **cannot** add a UDR to the `AzureFirewallSubnet` for traffic already being inspected there

---

## Section 5 — Network Security Groups (NSGs)

### What NSGs do

An NSG is a stateful packet filter — it contains **security rules** that allow or deny inbound/outbound traffic based on 5-tuple: source IP, destination IP, source port, destination port, protocol.

NSGs can be associated with:

- **Subnets** — applies to all NICs in the subnet
- **Network interfaces (NICs)** — applies to that VM only

When both are present, **both** are evaluated. Traffic must pass both the subnet NSG and the NIC NSG.

### Rule properties

Each rule has:

- **Priority** — 100 to 4096; **lower number = higher priority** (processed first)
- **Name** — unique within the NSG
- **Source/Destination** — IP, CIDR, Service Tag, or ASG
- **Port** — single port, range, or `*`
- **Protocol** — TCP, UDP, ICMP, or Any
- **Action** — Allow or Deny

### Default rules (always present, cannot be deleted)

**Inbound defaults:**

|Priority|Name|Source|Destination|Port|Action|
|---|---|---|---|---|---|
|65000|AllowVnetInBound|VirtualNetwork|VirtualNetwork|Any|Allow|
|65001|AllowAzureLoadBalancerInBound|AzureLoadBalancer|Any|Any|Allow|
|65500|DenyAllInBound|Any|Any|Any|**Deny**|

**Outbound defaults:**

|Priority|Name|Source|Destination|Port|Action|
|---|---|---|---|---|---|
|65000|AllowVnetOutBound|VirtualNetwork|VirtualNetwork|Any|Allow|
|65001|AllowInternetOutBound|Any|Internet|Any|Allow|
|65500|DenyAllOutBound|Any|Any|Any|**Deny**|

### Service Tags

Pre-built, Microsoft-managed groups of IP ranges for Azure services. Use in NSG rules instead of hardcoding IPs:

|Tag|Covers|
|---|---|
|`VirtualNetwork`|All VNet address spaces + peered VNets + on-prem via VPN/ER|
|`AzureLoadBalancer`|Azure load balancer health probe source IPs|
|`Internet`|All public IPs not known to be Azure|
|`AzureCloud`|All Azure datacenter IPs|
|`Storage`|Azure Storage service IPs|
|`Sql`|Azure SQL service IPs|
|`AppService`|App Service outbound IPs|
|`GatewayManager`|Azure gateway management plane (required for Bastion NSG)|

### Application Security Groups (ASGs)

ASGs let you group VM NICs logically (e.g. "WebServers", "DBServers") and use those groups as source/destination in NSG rules — without specifying individual IPs.

```
NSG Rule:
  Source: ASG-WebServers
  Destination: ASG-DBServers
  Port: 1433
  Action: Allow
```

- VMs are added to an ASG by assigning their NIC to the ASG
- A NIC can belong to multiple ASGs
- ASGs must be in the same region as the VNet
- Greatly simplifies rules as VMs are added/removed — you update the ASG, not the rules

### Evaluating effective security rules

The exam asks you to determine whether traffic is allowed or denied. Steps:

1. Traffic hits **subnet NSG** (if associated) — processed inbound or outbound
2. Traffic hits **NIC NSG** (if associated) — processed inbound or outbound
3. Rules evaluated by priority (lowest number first); first match wins
4. If no rule matches → hit the default Deny rule

**Inbound traffic path:** Internet → Subnet NSG → NIC NSG → VM **Outbound traffic path:** VM → NIC NSG → Subnet NSG → Internet

**Tool:** In the Azure portal → Network Interface → "Effective security rules" shows the merged view of all rules affecting a NIC, with their effective priorities. Use **Network Watcher → IP flow verify** to test whether a specific flow would be allowed or denied.

### Common NSG exam scenarios

**Allow RDP from specific IP only:**

```
Priority 100 | Allow | TCP | Source: 203.0.113.5/32 | Dest: * | Port: 3389
Priority 200 | Deny  | TCP | Source: *             | Dest: * | Port: 3389
```

**Allow web tier to DB tier only:**

```
ASG: WebTier, DBTier
Priority 100 | Allow | TCP | Source: ASG-WebTier | Dest: ASG-DBTier | Port: 1433
(Default DenyAll handles everything else)
```

### Exam tips — NSGs

- NSG rules are **stateful** — if inbound is allowed, the response is automatically allowed outbound
- **Lower priority number = evaluated first** — this is the #1 NSG exam trap
- `AllowVnetInBound` (priority 65000) allows all VNet traffic by default; add explicit deny rules at lower priority numbers to block specific traffic
- You can associate an NSG to **zero, one, or many** subnets/NICs
- NSG **flow logs** → stored in a Storage Account → analyzed with Traffic Analytics in Network Watcher

---

## Section 6 — Azure Bastion

### What it does

A managed PaaS jump host that provides browser-based RDP and SSH to VMs without exposing port 3389/22 or requiring public IPs on VMs.

### How it works

```
User browser ──── HTTPS (443) ──── Azure Bastion (AzureBastionSubnet)
                                         │ RDP/SSH (private IP)
                                       Target VM (no public IP needed)
```

### SKU comparison

|Feature|Basic|Standard|
|---|---|---|
|Browser-based RDP/SSH|✓|✓|
|Native RDP/SSH client|✗|✓|
|File transfer|✗|✓|
|Shareable links|✗|✓|
|IP-based connection|✗|✓|
|Connect to VMs in peered VNets|✗|✓|
|Scale units|2 fixed|2–50|

### Subnet and NSG requirements

Subnet name must be exactly `AzureBastionSubnet`, minimum `/26`.

Required NSG rules on `AzureBastionSubnet`:

**Inbound:**

|Priority|Source|Port|Action|
|---|---|---|---|
|100|Internet|443|Allow (HTTPS from users)|
|110|GatewayManager|443|Allow (Azure management plane)|
|120|AzureLoadBalancer|443|Allow (health probes)|

**Outbound:**

|Priority|Destination|Ports|Action|
|---|---|---|---|
|100|VirtualNetwork|3389, 22|Allow (RDP/SSH to VMs)|
|110|AzureCloud|443|Allow (Bastion control plane)|

### Exam tips — Bastion

- Basic SKU **cannot** connect to VMs in **peered VNets** — Standard required
- Bastion does not bypass NSGs on the **target VM's subnet** — those still apply
- Bastion always requires a **Standard public IP** associated to it
- One Bastion per VNet; in hub-spoke, deploy in hub (Standard SKU) to cover all spokes

---

## Section 7 — Service Endpoints

### What they do

Extend the VNet's network identity to Azure PaaS services (Storage, SQL, Key Vault, etc.) over the **Azure backbone**, so traffic doesn't leave the Microsoft network to reach those services.

### How to configure

1. Enable the Service Endpoint on a subnet (e.g. `Microsoft.Storage`)
2. Configure the PaaS resource's firewall to allow access from the VNet/subnet

### Supported services (common ones)

`Microsoft.Storage`, `Microsoft.Sql`, `Microsoft.KeyVault`, `Microsoft.ServiceBus`, `Microsoft.EventHub`, `Microsoft.ContainerRegistry`, `Microsoft.CognitiveServices`, `Microsoft.AppService`

### Service Endpoint Policies

- Restrict which **specific resources** within a service type a subnet can access
- Example: subnet can reach `storageaccountprod` but not `storageaccounttest`
- Currently supported for Storage and SQL only

### Service Endpoints vs Private Endpoints

||Service Endpoint|Private Endpoint|
|---|---|---|
|Private IP in your VNet|✗|✓|
|PaaS still has public IP|✓|✗ (can disable public access)|
|Traffic path|Azure backbone (VNet identity)|Fully private NIC in VNet|
|DNS changes needed|✗|✓ (private DNS zone required)|
|Cost|Free|~$7–10/month per endpoint + data|
|Cross-region access|Limited|✓|
|Data exfiltration protection|Partial (via policies)|Strong (private IP only)|
|Use case|Simple, cost-sensitive|Strict isolation, compliance|

### Exam tips — Service Endpoints

- Enabling a Service Endpoint **automatically adds a route** in the subnet's effective routes for that service
- Service Endpoints are configured **per-subnet**, not per-VNet
- The PaaS resource's firewall must explicitly allow the subnet — enabling the endpoint alone is not sufficient
- Traffic still originates from the **VNet's public IP space** from the PaaS perspective (not a private IP)

---

## Section 8 — Private Endpoints

### What they do

Inject a **private network interface** (with a private IP from your VNet) into your VNet, mapped to a specific PaaS resource. All traffic to that resource uses the private IP and stays entirely within Azure's private network.

### How it works

```
VM (10.1.0.4) ──── Private IP ──── Private Endpoint NIC (10.1.0.10) ──── Azure Storage Account
                                    (in your VNet subnet)
```

The storage account can have its public endpoint disabled, making it accessible **only** via the private endpoint.

### DNS resolution requirement

When a private endpoint is created, the PaaS resource's public DNS name must resolve to the **private IP**, not the public IP, for traffic to route correctly.

Solution: **Azure Private DNS Zones**

```
privatelink.blob.core.windows.net  → A record: 10.1.0.10
```

Steps:

1. Create Private Endpoint → get private IP
2. Create or use existing Private DNS Zone (e.g. `privatelink.blob.core.windows.net`)
3. Link the Private DNS Zone to the VNet
4. Add A record: storage account FQDN → private endpoint IP (done automatically if integrated)

**Private DNS Zone names by service:**

|Service|Private DNS Zone|
|---|---|
|Blob Storage|`privatelink.blob.core.windows.net`|
|File Storage|`privatelink.file.core.windows.net`|
|Azure SQL|`privatelink.database.windows.net`|
|Key Vault|`privatelink.vaultcore.azure.net`|
|Container Registry|`privatelink.azurecr.io`|

### Exam tips — Private Endpoints

- Private Endpoints are **subnet resources** — they consume an IP from the subnet
- **NSGs on the subnet do apply** to private endpoint traffic (as of recent updates — previously they did not)
- If DNS is not configured correctly, the resource FQDN resolves to the public IP and traffic won't use the private endpoint
- Private Endpoints can be accessed **cross-region** via global VNet peering
- A single private endpoint can only map to **one resource instance** (not a whole service)

---

## Section 9 — Azure DNS

### Azure-provided DNS (default)

Every VNet gets a DNS resolver at `168.63.129.16` (a "magic" Azure IP). It resolves:

- Azure internal names for VNet resources (auto-registered)
- Public DNS names (forwarded to Azure recursive resolvers)

Default internal DNS names: `<vm-name>.<location>.cloudapp.azure.com` — not useful for real apps.

### Azure DNS Zones

**Public DNS zones** — host DNS records for internet-resolvable domain names.

To use Azure DNS for a domain (e.g. `contoso.com`):

1. Create a Public DNS Zone named `contoso.com` in Azure
2. Note the Azure nameservers assigned (e.g. `ns1-01.azure-dns.com`)
3. Update your domain registrar's NS records to point to those Azure nameservers
4. Add records (A, CNAME, MX, TXT, etc.) in the Azure DNS zone

**Record types:**

|Type|Purpose|Example|
|---|---|---|
|A|IPv4 address|`www` → `1.2.3.4`|
|AAAA|IPv6 address|`www` → `2001:db8::1`|
|CNAME|Alias to another name|`www` → `contoso.azurewebsites.net`|
|MX|Mail server|`@` → `mail.contoso.com` priority 10|
|TXT|Verification, SPF|`@` → `"v=spf1 include:..."`|
|NS|Nameserver delegation|`@` → Azure DNS nameservers|
|SOA|Zone authority|Auto-created|
|PTR|Reverse lookup|`4.3.2.1.in-addr.arpa` → `host.contoso.com`|
|SRV|Service location|`_sip._tcp` → server/port|
|CAA|Certificate authority authorization|`@` → CA allowed to issue certs|

**Alias records:**

- Azure-specific record type that points to Azure resources (Load Balancer, Traffic Manager, CDN, public IP)
- Unlike CNAME, can be used at the **zone apex** (root of domain, e.g. `contoso.com`)
- Automatically updates when the Azure resource's IP changes

### Private DNS Zones

Used for DNS resolution **within VNets** — resources in the VNet can resolve names in the private zone.

Key concepts:

- **VNet link** — you must link the private zone to a VNet for resolution to work
- **Auto-registration** — when enabled on a VNet link, VMs in the VNet automatically get A records created in the zone when they start
- **Split-horizon DNS** — same zone name used for both public and private zones (different records); private zone takes precedence inside the VNet

Common private zone name patterns:

- `internal.contoso.com` — for internal resources
- `privatelink.blob.core.windows.net` — for private endpoints (see Section 8)

### Custom DNS servers

You can override the default Azure DNS and use your own DNS servers (e.g. Windows DNS, AD-integrated DNS):

- Set at the VNet level (applies to all subnets unless overridden)
- Custom DNS server must be reachable from the VNet
- Custom DNS server should forward Azure-internal names to `168.63.129.16` (Azure DNS)

### DNS resolution order (VNet with custom DNS server)

```
VM query → Custom DNS server → can't resolve → forwards to 168.63.129.16 → resolves
                             → can resolve → returns record
```

### Exam tips — DNS

- `168.63.129.16` is **Azure's magic DNS IP** — used internally even with custom DNS configured
- CNAME records **cannot** be created at the zone apex — use Alias records instead
- Auto-registration in private zones only works for VMs, not other resources (no auto-registration for App Services, etc.)
- A private DNS zone can be linked to **multiple VNets**; one VNet can be linked to **multiple private DNS zones** (each for different name spaces)
- TTL (Time to Live) controls how long DNS responses are cached — lower TTL = faster propagation of changes, higher DNS query cost

---

## Section 10 — Azure Load Balancer

### Overview

Azure Load Balancer (ALB) operates at **Layer 4 (TCP/UDP)**. It distributes inbound traffic across backend pool instances based on configurable rules. It does not inspect HTTP content — that's Application Gateway's job.

### SKUs

|Feature|Basic|Standard|
|---|---|---|
|Backend pool|VMs in same availability set or VMSS|Any VM in same VNet|
|Health probes|HTTP, TCP|HTTP, HTTPS, TCP|
|Availability zones|No|Yes (zone-redundant)|
|SLA|None|99.99%|
|HTTPS probes|No|Yes|
|Outbound rules|No|Yes|
|Multiple frontend IPs|No|Yes|
|Secure by default|No (open)|Yes (requires NSG)|
|Global load balancing|No|Yes (cross-region LB)|

> Standard is the current recommendation. Basic is being deprecated.

### Components

**Frontend IP configuration:** The IP address (public or private) that clients connect to.

**Backend pool:** The set of VMs (or VMSS instances) that receive traffic.

**Health probe:** Periodic checks to determine if backend instances are healthy.

- HTTP probe: sends GET to a path; 200 response = healthy
- TCP probe: checks if port is open
- HTTPS probe: like HTTP but over TLS (Standard only)
- If a VM fails the probe, it's removed from rotation until it recovers

**Load balancing rules:** Maps frontend IP:port → backend pool:port.

- **Session persistence (affinity):**
    - None (default) — each packet can go to any healthy backend
    - Client IP — all flows from same client IP go to same backend
    - Client IP and Protocol — same client IP + protocol go to same backend

**Inbound NAT rules:** Map a specific frontend IP:port to a specific backend VM:port. Used for direct VM access (e.g. RDP to individual VMs behind a shared public IP).

**Outbound rules (Standard only):** Control SNAT for outbound internet flows from the backend pool. Configure number of SNAT ports per instance.

### Public vs Internal Load Balancer

||Public LB|Internal LB (ILB)|
|---|---|---|
|Frontend IP|Public IP|Private IP (from VNet subnet)|
|Traffic direction|Internet → backends|Internal VNet → backends|
|Use case|Web tier, public APIs|Database tier, internal services, NVA HA|

### HA Ports rule (Standard ILB)

A special rule type that load-balances **all ports and all protocols** simultaneously. Used for NVA HA — traffic from any port/protocol is distributed across NVA instances.

```
Rule: Frontend 10.0.0.5:0 (HA Ports) → Backend pool: NVA instances
```

### Exam tips — Load Balancer

- **Standard LB requires NSG** to allow traffic to backend VMs — Basic allows all by default
- Health probe source IP is `168.63.129.16` — never block this in NSGs on backend VMs
- Load Balancer rules use **5-tuple hashing** by default (src IP, src port, dst IP, dst port, protocol) — results in good distribution but no stickiness
- Standard LB backend pool VMs **do not** need public IPs — the LB translates
- Standard LB supports **multiple frontend IPs** — useful for hosting multiple services on same backend pool

### Troubleshooting load balancing

**VM not receiving traffic:**

1. Check health probe status (portal → Load Balancer → Backend pools → Health status)
2. Check NSG — is the health probe port (168.63.129.16) allowed?
3. Check NSG — is the application port allowed from `AzureLoadBalancer` service tag?
4. Check the VM is running the service on the probed port
5. Check the LB rule maps correct frontend port to backend port

**Traffic going to one VM only:**

- Usually a health probe failure — other VMs failing probe, so traffic concentrates on healthy one

---

## Section 11 — Application Gateway

> See also the full service reference in Section 12 for AZ-700 overlap. Below focuses on what AZ-104 specifically tests.

### AZ-104 focus areas

**URL path-based routing:**

```
contoso.com/api/*   → Backend Pool: API servers
contoso.com/images/* → Backend Pool: CDN servers
contoso.com/*        → Backend Pool: Default web servers
```

**Multi-site hosting:**

```
app1.contoso.com → Listener 1 → Backend Pool 1
app2.contoso.com → Listener 2 → Backend Pool 2
(Both listeners on same App Gateway, same public IP)
```

**WAF modes:**

- **Detection** — logs threats but does not block
- **Prevention** — actively blocks matched requests

**Backend health:** App Gateway continuously probes backends via HTTP health probes. If a backend fails, it's taken out of rotation.

### AZ-104 exam tips — App Gateway

- App Gateway and Load Balancer are commonly compared on the exam:
    - Load Balancer: L4, TCP/UDP, any traffic type
    - App Gateway: L7, HTTP/HTTPS only, URL/header-aware
- App Gateway requires a **dedicated subnet** — no other resources in that subnet
- Both v1 and v2 SKUs exist; v2 supports autoscaling and zone redundancy — prefer v2

---

## Section 12 — Network Connectivity Troubleshooting

### Azure Network Watcher

A suite of network diagnostic and monitoring tools. Must be **enabled per region** (auto-enabled when you create a VNet in a region, but verify).

#### Key tools

**IP flow verify**

- Tests whether a specific traffic flow (src IP, dst IP, src port, dst port, protocol, direction) would be allowed or denied by NSGs
- Returns which NSG rule allowed/denied it
- Use for: "Why can't VM A reach VM B on port 443?"

**Next hop**

- Shows the next hop type and IP for traffic from a VM to a destination IP
- Returns: Virtual network, Internet, Virtual appliance, VPN gateway, None (dropped)
- Use for: "Where does traffic from VM A actually go when it tries to reach 8.8.8.8?"

**Connection troubleshoot**

- Tests TCP connectivity from a source VM/endpoint to a destination IP:port
- Reports: Reachable, Unreachable, or Unknown
- Shows the path and latency
- Use for: "Can VM A actually reach SQL server on port 1433?"

**Connection Monitor**

- Continuous monitoring of network connections between endpoints
- Monitors latency, packet loss, and reachability over time
- Generates alerts when thresholds are breached
- Use for: ongoing SLA monitoring, not one-off troubleshooting

**NSG flow logs**

- Logs all network flows that hit an NSG (allowed and denied)
- Stored in an Azure Storage Account (JSON format)
- Visualised with Traffic Analytics in Azure Monitor
- Useful for security auditing and traffic pattern analysis

**Packet capture**

- Captures network packets on a VM
- Requires Network Watcher Agent VM extension on the VM
- Output: `.cap` or `.pcap` file stored in Storage Account or locally

**VPN troubleshoot**

- Diagnoses VPN Gateway and connection health
- Returns status and log files to a Storage Account

### Common troubleshooting scenarios

**Cannot RDP to a VM:**

1. IP flow verify: check if NSG allows TCP 3389 inbound
2. Check VM is running
3. Check VM has a public IP or is accessible via Bastion/VPN
4. Check Windows Firewall inside the VM

**VM cannot reach the internet:**

1. Next hop: should show "Internet" for 8.8.8.8; if "None" → route is dropping it
2. Check for a UDR with `0.0.0.0/0 → None` black-holing traffic
3. Check NSG outbound rules

**VM cannot reach another VM in same VNet:**

1. IP flow verify (both directions)
2. Check NSG on both source NIC/subnet and destination NIC/subnet
3. Verify VNet address spaces don't have weird overlaps

**Cannot reach a PaaS service:**

1. Check Service Endpoint or Private Endpoint configuration
2. Check the PaaS resource's firewall rules (is the subnet/IP allowed?)
3. Check DNS resolution (nslookup inside the VM — resolving to public IP or private IP?)

---

## Section 13 — Key Services from AZ-700 Scope (AZ-104 Context)

The following services appear in the AZ-104 networking domain but are covered in more depth in AZ-700. Below is the AZ-104-relevant summary.

### NAT Gateway

Provides scalable, deterministic SNAT for private subnets. Prevents SNAT port exhaustion.

- Attach to subnets; all outbound traffic from those subnets uses NAT GW
- Up to 16 public IPs = up to 1,024,000 SNAT ports
- Cannot be used on GatewaySubnet or AzureBastionSubnet
- Overrides instance-level public IPs for outbound

### Azure Firewall

Managed stateful firewall for east-west and north-south traffic control.

- Requires `AzureFirewallSubnet` (/26 minimum)
- Rule processing order: DNAT → Network → Application
- Force tunnel all internet traffic through Firewall via UDR: `0.0.0.0/0 → Virtual appliance → Firewall private IP`

### VPN Gateway

Connects on-prem to Azure via IPsec/IKEv2 over the internet.

- Requires `GatewaySubnet` (/27 minimum, /26 recommended)
- Site-to-site (S2S): on-prem network ↔ Azure
- Point-to-site (P2S): individual client VPN
- VNet-to-VNet: encrypted tunnel between two Azure VNets
- Deployment takes 30–45 minutes

### Azure Bastion

Browser-based RDP/SSH without public IPs on VMs. Covered in full in Section 6.

---

## Section 14 — Combination Patterns and Architecture

### Hub-Spoke with Centralised Security

```
On-Prem ──── VPN/ER Gateway (GatewaySubnet)
                    │
             Azure Firewall (AzureFirewallSubnet)  ← UDR: 0.0.0.0/0 → Firewall from all spokes
             Azure Bastion  (AzureBastionSubnet)   ← Standard SKU for cross-spoke access
                /    │    \
          Spoke1   Spoke2   Spoke3
          UDR: 0.0.0.0/0 → Firewall
          NSG: restrict per tier
```

### Three-Tier Web Application

```
Internet
   │
   ▼
Public Load Balancer (Standard)
   │ frontend: public IP
   │ backend pool: web tier VMs
   │ NSG: allow 80/443 from Internet
   ▼
Web Tier (Subnet 10.0.1.0/24)
   │ NSG: allow 8080 from LB, deny all else
   │
   ▼
Internal Load Balancer
   │ frontend: private IP 10.0.2.10
   │ backend pool: app tier VMs
   ▼
App Tier (Subnet 10.0.2.0/24)
   │ NSG: allow 8080 from WebTier ASG only
   │
   ▼
Database Tier (Subnet 10.0.3.0/24)
   │ NSG: allow 1433 from AppTier ASG only
   │ Private Endpoint for Azure SQL (if PaaS)
```

### Private PaaS Access Pattern

```
VM (10.1.0.4)
   │
   │ DNS query: mystorageaccount.blob.core.windows.net
   ▼
Private DNS Zone: privatelink.blob.core.windows.net
   │ A record: mystorageaccount → 10.1.0.10
   ▼
Private Endpoint NIC (10.1.0.10) in subnet
   │
   ▼
Azure Storage Account (public endpoint disabled)
```

---

## Section 15 — Decision Framework

### Which service answers which need?

```
Need inbound traffic distribution?
  ├─ HTTP/HTTPS, URL-based routing, WAF → Application Gateway
  └─ TCP/UDP, any port → Azure Load Balancer

Need outbound internet?
  ├─ Fixed public IPs, no inspection → NAT Gateway
  └─ FQDN/policy filtering → Azure Firewall

Need to connect to on-premises?
  ├─ Private, high-bandwidth → ExpressRoute
  └─ Encrypted over internet → VPN Gateway (S2S)

Need to secure access to PaaS?
  ├─ Simple, free, no private IP → Service Endpoints
  └─ Private IP, strict isolation → Private Endpoints

Need admin VM access without public IP?
  └─ Azure Bastion

Need to filter traffic between subnets/VNets?
  └─ NSGs (stateless rules) + Azure Firewall (stateful, FQDN-aware)

Need to resolve names privately?
  └─ Azure Private DNS Zones (linked to VNet)

Need to route traffic to an NVA/Firewall?
  └─ User-Defined Routes (UDRs) on subnets

Need VNets to communicate?
  ├─ Same region or cross-region → VNet Peering
  └─ Need transitivity across many VNets → Azure Virtual WAN
```

### Load balancer comparison (exam favourite)

|Scenario|Use|
|---|---|
|Distribute HTTP traffic, SSL termination|Application Gateway|
|Distribute HTTP traffic globally|Azure Front Door|
|Distribute TCP/UDP traffic, public-facing|Azure Load Balancer (Public, Standard)|
|Distribute TCP/UDP traffic, internal|Azure Load Balancer (Internal, Standard)|
|HA pair of NVAs|Internal Load Balancer + HA Ports rule|
|Single-IP access to many VMs (RDP)|LB Inbound NAT rules|

---

## Section 16 — Quick Reference Tables

### Reserved subnet names and sizes

|Name|Required for|Minimum size|
|---|---|---|
|`GatewaySubnet`|VPN Gateway, ExpressRoute Gateway|/27 (recommend /26)|
|`AzureFirewallSubnet`|Azure Firewall|/26|
|`AzureBastionSubnet`|Azure Bastion|/26|
|`RouteServerSubnet`|Azure Route Server|/27|

### NSG rule evaluation cheat sheet

```
Priority   Action   Meaning
-------    ------   -------
100–199    Allow    Early explicit allows (specific trusted sources)
200–499    Allow    Application-level allows
500–999    Deny     Explicit denies (block specific bad actors)
1000–3999  Allow    Broad allows (backup rules)
65000      Allow    AllowVnetInBound (cannot be deleted)
65001      Allow    AllowAzureLoadBalancerInBound (cannot be deleted)
65500      Deny     DenyAllInBound (cannot be deleted)
```

### DNS zone types and purpose

|Zone Type|Purpose|Accessible From|
|---|---|---|
|Public DNS zone|Internet-resolvable records|Anywhere|
|Private DNS zone (autoregistration)|Internal VM name registration|Linked VNets|
|Private DNS zone (privatelink.*)|Private endpoint DNS resolution|Linked VNets|

### Network Watcher tool selection

|Problem|Tool|
|---|---|
|Is this NSG rule blocking my traffic?|IP flow verify|
|Where does my traffic actually go?|Next hop|
|Can VM reach this endpoint:port right now?|Connection troubleshoot|
|Monitor connection health continuously|Connection Monitor|
|What traffic is hitting my NSG over time?|NSG flow logs|
|Capture raw packets from a VM|Packet capture|
|Why is my VPN tunnel down?|VPN troubleshoot|

---

## Section 17 — AZ-104 Exam Watch-Outs

### NSG priority

- **Lower number = higher priority** — this trips up almost every first-time candidate
- A rule at priority 100 overrides one at priority 200
- Default rules (65000, 65001, 65500) cannot be deleted but can be overridden with lower-priority-number custom rules

### VNet peering

- **Non-transitive** — A↔B and B↔C does not enable A↔C
- Must create peerings in **both directions** to get a "Connected" state
- Address spaces must be **non-overlapping** — this is checked at peering time
- Peering across subscriptions requires permissions on **both** subscriptions

### Standard vs Basic everywhere

- Standard public IP, Standard LB, Standard App Gateway v2 are all the current defaults
- Basic is being deprecated — do not design new solutions with it
- Standard LB **requires NSGs** to allow traffic; Basic does not (open by default)

### Service Endpoints vs Private Endpoints

- Service Endpoints: free, no private IP, traffic stays on backbone but PaaS has public endpoint
- Private Endpoints: cost money, give PaaS a private IP, require DNS configuration
- Exam will test which one to use for a given scenario — look for words like "private IP", "no public endpoint", "compliance" → Private Endpoint

### DNS gotchas

- CNAME records **cannot** be used at the zone apex — use Alias records
- Private DNS zones must be **linked to a VNet** for resolution to work — creating the zone alone is not enough
- Auto-registration only works for **VMs**, not App Services or other PaaS
- For private endpoints, DNS must resolve to the **private IP** not the public IP — use `privatelink.*` private DNS zones

### Load balancer health probes

- Health probe source is `168.63.129.16` — **must be allowed** in NSGs on backend VMs
- HTTP probes check for a `200` response — any other code = unhealthy
- A backend instance is only removed from rotation if health probe **fails consistently** (not on a single failure)

### Azure Bastion

- Basic SKU cannot access VMs in **peered VNets**
- NSG on `AzureBastionSubnet` **must** allow `GatewayManager` service tag inbound on 443
- Bastion does **not** bypass NSGs on target VM subnets

### UDR / routing

- UDRs are associated with **subnets**, not VNets or NICs
- To route through an NVA, **IP forwarding must be enabled** on the NVA's NIC
- "Propagate gateway routes" = disabled means on-prem routes are NOT auto-added to the subnet's route table

---

## Section 18 — Lab Skills Checklist

The AZ-104 exam includes scenario questions that expect you to have done these tasks:

### VNet and subnet

- [ ] Create a VNet with multiple subnets in the portal and via CLI/PowerShell
- [ ] Add an address space to an existing VNet
- [ ] Create VNet peering between two VNets (portal and CLI)
- [ ] Verify effective routes on a VM NIC

### NSGs

- [ ] Create an NSG with custom rules
- [ ] Associate an NSG to a subnet and to a NIC
- [ ] View effective security rules on a VM NIC
- [ ] Create an ASG, assign VM NICs to it, use it in NSG rules

### DNS

- [ ] Create a public DNS zone, add A and CNAME records
- [ ] Delegate a domain to Azure DNS nameservers
- [ ] Create a private DNS zone, link it to a VNet with autoregistration
- [ ] Create a privatelink DNS zone for a private endpoint

### Load Balancer

- [ ] Create a Standard public Load Balancer with backend pool, health probe, and LB rule
- [ ] Create an Internal Load Balancer with private frontend IP
- [ ] Add VMs to a backend pool
- [ ] Create an inbound NAT rule for direct VM access

### Troubleshooting

- [ ] Use IP flow verify to test NSG rules
- [ ] Use Next hop to trace routing
- [ ] Use Connection troubleshoot to test VM-to-endpoint connectivity
- [ ] Enable NSG flow logs and view in Storage Account

### Private/Service Endpoints

- [ ] Enable a Service Endpoint on a subnet and configure Storage account firewall
- [ ] Create a Private Endpoint for a Storage account
- [ ] Create a private DNS zone for privatelink.blob.core.windows.net and verify name resolution

### Bastion

- [ ] Create AzureBastionSubnet (/26)
- [ ] Deploy Azure Bastion (Basic or Standard)
- [ ] Connect to a VM via Bastion in the portal
- [ ] Configure required NSG rules on AzureBastionSubnet

---

_Tags: #azure #az104 #networking #nsg #vnet #dns #loadbalancer #bastion #serviceendpoints #privateendpoints #udr #peering #networkwatcher_
# Azure Network Services — AZ-700 Study Notes

> **Exam context:** AZ-700 (Azure Network Engineer Associate) — this topic covers the full networking stack: ingress, egress, hybrid connectivity, routing control, security enforcement, and administrative access.

---

## Mental Models First

Before memorizing individual services, lock in these four lenses:

### 1. Traffic Direction

|Direction|Primary Services|
|---|---|
|Inbound (L7 HTTP/S)|Application Gateway|
|Inbound (Admin RDP/SSH)|Azure Bastion|
|Outbound (internet egress)|NAT Gateway, Azure Firewall|
|East-west (VNet ↔ VNet, subnet ↔ subnet)|Azure Firewall, NVA|
|Hybrid (on-prem ↔ Azure)|VPN Gateway, ExpressRoute|

### 2. Control Plane vs Data Plane

- **Route Server** is _control plane only_ — it exchanges BGP routing information but never forwards packets itself.
- Everything else operates on the data plane (actual packet forwarding).
- Exam trap: Route Server does not replace a firewall or NVA — it just removes the need for manual UDRs when NVAs speak BGP.

### 3. Layer of Operation

|Layer|Service|
|---|---|
|L3 (IP routing/NAT)|NAT Gateway, VPN Gateway, ExpressRoute GW, Route Server|
|L4 (TCP/UDP stateful)|Azure Firewall (Standard), NVA|
|L7 (HTTP/HTTPS, FQDN)|Application Gateway, Azure Firewall (Premium), NVA|
|Admin plane|Azure Bastion|

### 4. The Hub-Spoke Pattern

Almost all complex Azure network architectures use hub-spoke. The hub VNet contains shared services; spokes peer to the hub and get access to everything in it.

```
[On-Prem] ──── VPN/ER Gateway (hub)
                     │
              Azure Firewall (hub)
              Route Server (hub)
              Azure Bastion (hub)
                /    │    \
         Spoke1  Spoke2  Spoke3
```

Spokes route `0.0.0.0/0` via a UDR to the Firewall's private IP in the hub. This forces all inter-spoke and outbound traffic through centralised inspection.

---

## Service Reference

---

### Application Gateway

**Layer:** L7 (HTTP/HTTPS) **Direction:** Inbound

#### What it does

A regional, managed HTTP/HTTPS load balancer with optional Web Application Firewall (WAF). It understands HTTP — meaning it can make routing decisions based on URL paths, hostnames, and headers, not just IP and port.

#### Core features

- **Multi-site hosting** — one gateway can serve multiple hostnames (SNI), routing each to a different backend pool
- **URL path-based routing** — `/api/*` → API pool, `/images/*` → static pool
- **SSL termination** — decrypt TLS at the gateway, send plain HTTP to backends (or re-encrypt)
- **SSL end-to-end** — decrypt, inspect, re-encrypt to backend
- **Cookie-based session affinity** — keep a user's requests going to the same backend instance
- **WAF (SKU: WAF_v2)** — OWASP CRS rules, bot protection, custom rules, rate limiting
- **Autoscaling (v2 SKU)** — scales instance count automatically based on traffic
- **Health probes** — HTTP probes to each backend; unhealthy instances are removed from rotation
- **Rewrite rules** — modify request/response headers on the fly
- **Redirect** — HTTP → HTTPS, or any path redirect

#### When NOT to use

- Non-HTTP traffic (TCP/UDP) → use Azure Load Balancer (L4) instead
- Pure outbound or east-west flows
- Global (multi-region) load balancing → use Azure Front Door instead

#### Key SKUs

|SKU|Use case|
|---|---|
|Standard_v2|L7 load balancing, no WAF|
|WAF_v2|L7 + WAF (OWASP rule sets)|

#### Exam tips

- App Gateway is **regional** — for global, use Front Door
- WAF can run in **Detection** (log only) or **Prevention** (block) mode
- Backend pools can be VMs, VMSS, App Services, IP addresses, or FQDNs
- Requires its own dedicated subnet

---

### NAT Gateway

**Layer:** L3 (SNAT) **Direction:** Outbound only

#### What it does

Provides scalable, deterministic Source Network Address Translation (SNAT) for outbound internet traffic from private subnets. Solves SNAT port exhaustion that occurs when many VMs share a single Load Balancer public IP.

#### Core features

- **Up to 16 public IPs** (or prefixes) per NAT Gateway, giving up to 1,024,000 SNAT ports
- **Subnet-level association** — attach to one or more subnets; all outbound traffic from those subnets uses the NAT Gateway
- **Fully managed** — no VMs to patch, no HA configuration needed
- **Zone-redundant or zonal** deployment options
- **TCP idle timeout** configurable (4–120 minutes)

#### When NOT to use

- Inbound traffic (NAT Gateway is outbound-only)
- Routing between VNets
- Stateful inspection of traffic — use Azure Firewall for that

#### How it interacts with other outbound paths

If a subnet has:

- A NAT Gateway → NAT Gateway wins for outbound
- A public IP on the VM + no NAT Gateway → public IP is used
- Neither → Azure default SNAT (unpredictable, not production-suitable)

#### Exam tips

- NAT Gateway **overrides** instance-level public IPs and Load Balancer outbound rules for subnets it's attached to
- Does **not** require UDRs — it's applied at subnet level automatically
- Cannot be used on gateway subnets or Azure Bastion subnets

---

### Azure Firewall

**Layer:** L3–L7 **Direction:** Inbound (DNAT), outbound, east-west

#### What it does

A managed, cloud-native, stateful firewall with built-in high availability and unrestricted cloud scalability. The centralised network security control plane for most Azure architectures.

#### Rule types (processed in order)

1. **DNAT rules** — translate inbound public IP:port to private IP:port (e.g. expose SSH on VM without public IP)
2. **Network rules** — L3/L4 allow/deny by source IP, destination IP, port, protocol
3. **Application rules** — L7 allow/deny by FQDN (e.g. `*.microsoft.com`), URL category, or TLS inspection

#### SKU comparison

|Feature|Standard|Premium|
|---|---|---|
|FQDN filtering|✓|✓|
|Threat intelligence|✓|✓|
|TLS inspection|✗|✓|
|IDPS (signature-based)|✗|✓|
|URL filtering (full path)|✗|✓|
|Web categories|✗|✓|

#### Firewall Policy

- A separate ARM resource that holds rule collections
- Can be hierarchical: **Base policy** (inherited by child policies) — useful for enforcing org-wide rules while allowing team-level customisation
- Policies can be shared across multiple firewall instances

#### Deployment pattern

- Deploy in a **dedicated subnet** called `AzureFirewallSubnet` (minimum /26)
- Has a **private IP** (used as next hop in UDRs) and one or more **public IPs**
- Spokes set `0.0.0.0/0` UDR → Firewall private IP to force all traffic through it

#### When NOT to use

- High-throughput L4-only workloads (NVA may be more cost-effective)
- If your organisation mandates a specific third-party vendor (use NVA instead)

#### Exam tips

- Azure Firewall is **not zone-redundant by default** in all regions — check at deployment
- Firewall does **not speak BGP** — use Route Server + NVA for dynamic routing
- DNAT rules **automatically create a corresponding network rule** to allow the translated traffic
- Threat intelligence can be set to Alert or Alert + Deny

---

### Virtual Network Gateway

**Layer:** L3 (tunnelling/routing) **Direction:** Hybrid (on-prem ↔ Azure)

#### What it does

The Azure-side termination point for VPN tunnels and ExpressRoute circuits. Required to connect any VNet to on-premises networks.

#### Two gateway types

**VPN Gateway**

- Uses IPsec/IKEv2 tunnels over the public internet
- Supports Site-to-Site (S2S), Point-to-Site (P2S), and VNet-to-VNet
- SKUs: Basic → VpnGw1–5 (higher = more throughput + connections)
- Active-active mode: two public IPs, two BGP peers, higher availability
- BGP support: dynamic route exchange with on-prem BGP routers

**ExpressRoute Gateway**

- Private circuit via a connectivity provider (not over internet)
- Attach to an ER circuit; must match circuit bandwidth/SKU
- SKUs: Standard, HighPerformance, UltraPerformance, ErGw1AZ–3AZ (zone-redundant)

#### VPN Gateway SKUs (key ones)

|SKU|Max throughput|Max S2S tunnels|
|---|---|---|
|VpnGw1|650 Mbps|30|
|VpnGw2|1 Gbps|30|
|VpnGw3|1.25 Gbps|30|
|VpnGw1AZ|650 Mbps|30 (zone-redundant)|

#### VPN + ExpressRoute coexistence

- A single VNet can have **both** a VPN Gateway and an ER Gateway
- Common pattern: ER as primary path, VPN as failover
- Requires separate gateway subnets — actually, both share `GatewaySubnet` but are separate gateway resources

#### Exam tips

- Gateway subnet must be named exactly `GatewaySubnet` — no other name works
- Basic SKU does **not** support BGP, active-active, or zone redundancy
- Deployment takes 30–45 minutes — plan for this in lab exercises
- P2S supports IKEv2, OpenVPN, and SSTP protocols

---

### Service Endpoints

**Layer:** L3 (routing optimisation) **Direction:** Outbound to Azure PaaS

#### What it does

Extends the VNet's identity to specific Azure PaaS services (Storage, SQL, Key Vault, etc.) over the Azure backbone network. Traffic routes optimally — it doesn't traverse the public internet — but the PaaS service still has a public IP.

#### How it works

1. Enable a Service Endpoint on a subnet (e.g. `Microsoft.Storage`)
2. Add a VNet/subnet rule to the PaaS resource's firewall
3. Traffic from that subnet to the PaaS service routes via the backbone, with the subnet's VNet identity presented

#### Supported services

Storage, SQL Database, SQL Data Warehouse, Cosmos DB, Key Vault, Service Bus, Event Hubs, App Service, Container Registry, Cognitive Services

#### Service Endpoint Policies

- Further restrict which specific resources within a service a subnet can access
- Example: allow access to `storageaccount-prod` only, not any storage account

#### Service Endpoints vs Private Endpoints

|Feature|Service Endpoint|Private Endpoint|
|---|---|---|
|Private IP in VNet|✗|✓|
|Traffic path|Azure backbone (source IP = VNet)|Fully private|
|DNS changes needed|✗|✓ (private DNS zone)|
|Cost|Free|~$7/month per endpoint|
|Cross-region support|Limited|✓|
|Data exfiltration protection|Partial (policies)|Strong|
|Use when|Simple/cheap VNet-to-PaaS|Strict isolation required|

#### Exam tips

- Service Endpoints do **not** give the PaaS resource a private IP — that's Private Endpoints
- Enabling a Service Endpoint on a subnet adds a route to the routing table automatically
- You still need to configure the PaaS resource's firewall to allow the subnet

---

### ExpressRoute

**Layer:** L2/L3 (private circuit) **Direction:** Hybrid (on-prem ↔ Azure, private)

#### What it does

A private, dedicated connection from your on-premises network to Azure via a connectivity provider (telco or colocation partner). Traffic never traverses the public internet.

#### Circuit components

```
On-Prem Router ──── Provider Edge ──── Microsoft Edge ──── Azure VNet
                  (Peering location)
```

- **Circuit:** The logical connection, provisioned by your provider
- **Peering location:** Microsoft's edge routers at partner colocation facilities
- **Virtual Network Gateway (ER type):** Attaches a VNet to the circuit

#### Peering types

|Type|Purpose|
|---|---|
|**Azure Private Peering**|Access Azure VNets (VMs, ILBs)|
|**Microsoft Peering**|Access Microsoft 365, Azure PaaS public endpoints|

_(Public Peering is deprecated — replaced by Microsoft Peering)_

#### SKUs and bandwidth

|SKU|Bandwidth options|
|---|---|
|Local|Up to 1 Gbps, only local Azure region|
|Standard|50 Mbps – 10 Gbps, one geopolitical region|
|Premium|50 Mbps – 100 Gbps, global reach|

#### ExpressRoute Global Reach

- Connect two on-premises locations through Azure's backbone (on-prem A ↔ Azure ↔ on-prem B)
- Requires Premium circuit SKU

#### FastPath

- Bypasses the ER Gateway for data plane traffic (still needs gateway for control plane)
- Reduces latency for high-throughput scenarios
- Requires UltraPerformance or ErGw3AZ gateway SKU

#### Exam tips

- ER circuits are **not encrypted by default** — use MACsec (L2) or IPsec over ER (L3) for encryption
- ER Gateway is **required** to connect a VNet to an ER circuit — it's a separate resource from a VPN Gateway
- Billing: circuit port + data transfer (Local SKU includes data transfer)
- ER + VPN coexistence: VPN can be failover path; requires both gateway types in same VNet

---

### Network Virtual Appliance (NVA)

**Layer:** L3–L7 (vendor-dependent) **Direction:** Any (as configured)

#### What it does

A VM (or VMSS) running third-party network software — Palo Alto, Cisco, Fortinet, Check Point, F5, etc. — or custom routing/security logic. You bring the software; Azure provides the compute.

#### Use cases vs Azure Firewall

|Scenario|Choose|
|---|---|
|Standard firewall + FQDN filtering|Azure Firewall|
|Advanced IDS/IPS with vendor signatures|NVA|
|SD-WAN termination|NVA|
|Existing on-prem vendor requirement|NVA|
|BGP-speaking router in Azure|NVA|
|Custom protocol handling|NVA|

#### HA patterns

- **Active-passive:** Two NVA VMs behind an Internal Load Balancer; health probes detect failure and shift traffic
- **Active-active:** Both NVAs process traffic, ILB distributes between them; requires stateful session sync (vendor-specific)
- **VMSS:** Some vendors support scaling NVA instances via VM Scale Sets

#### Routing to NVAs

NVAs require **User Defined Routes (UDRs)** unless Route Server is used:

```
Route: 0.0.0.0/0 → Next hop: NVA private IP (or ILB frontend IP)
```

#### Exam tips

- NVA HA requires careful UDR + ILB design — a common exam scenario
- IP forwarding must be **enabled on the NVA's NIC** in Azure — it's off by default (Azure blocks traffic not destined for the NIC's own IP)
- NVAs can speak BGP with Route Server — this is the key integration point
- NVAs are your responsibility to patch, update, and scale

---

### Route Server

**Layer:** Control plane (BGP) **Direction:** N/A (routing information only)

#### What it does

A managed Azure service that enables BGP route exchange between NVAs (or ExpressRoute/VPN gateways) and the Azure Software-Defined Network. Eliminates the need to manually maintain UDRs when routes change.

#### How it works

```
NVA ←─── BGP peering ───→ Route Server ←──→ Azure SDN
           (routes)              (injects routes into VNet routing table)
```

1. NVA peers with Route Server via eBGP
2. NVA advertises routes (e.g. on-prem prefixes it has learned)
3. Route Server injects those routes into the VNet's effective routing table
4. NVA also learns Azure VNet prefixes from Route Server

#### Key properties

- **ASN:** Route Server uses ASN 65515
- **Branch-to-branch:** Optional setting that allows Route Server to exchange routes _between_ peered NVAs (enables transit routing)
- **VNet peering propagation:** Routes can propagate across peered VNets
- **Does not forward traffic** — it is purely a routing control plane service

#### Route Server vs manual UDRs

||Manual UDRs|Route Server|
|---|---|---|
|Updates when routes change|Manual|Automatic (BGP)|
|Scale|Poor (UDR limit per subnet)|Good|
|Requires BGP-capable NVA|No|Yes|
|Complexity|Low for simple scenarios|Higher initial setup|

#### Exam tips

- Route Server **does not replace** Azure Firewall — they serve different functions
- You **cannot** peer Route Server directly with on-prem without an NVA or Gateway in between
- Route Server is deployed in its own dedicated subnet: `RouteServerSubnet`
- Supports **up to 8 BGP peers**
- Route Server + NVA is the pattern for dynamic SD-WAN / branch routing in Azure

---

### Azure Bastion

**Layer:** Admin access plane **Direction:** Inbound (browser → VM, no public IP on VM)

#### What it does

A managed PaaS service that provides secure RDP and SSH access to Azure VMs directly through the Azure portal (or native client) — without requiring public IPs on VMs, without exposing ports 22 or 3389 to the internet.

#### How it works

```
User browser ──── HTTPS (443) ──── Azure Bastion ──── RDP/SSH (private) ──── VM
                                   (AzureBastionSubnet)
```

- Bastion has a public IP (for users to reach it via portal/HTTPS)
- VMs have **no public IP required**
- Traffic from Bastion to VM travels entirely within Azure's network

#### SKU comparison

|Feature|Basic|Standard|
|---|---|---|
|RDP/SSH in browser|✓|✓|
|Native client (RDP/SSH app)|✗|✓|
|File transfer|✗|✓|
|Shareable links|✗|✓|
|IP-based connection|✗|✓|
|VNet peering support|✗|✓|
|Scale units|2|2–50|

#### Subnet requirements

- Dedicated subnet named exactly `AzureBastionSubnet`
- Minimum size: **/26** (recommended /26 or larger for scale units)
- NSG on AzureBastionSubnet must allow:
    - Inbound: HTTPS from internet, Gateway Manager from `GatewayManager` service tag
    - Outbound: RDP/SSH (3389/22) to VNet, HTTPS to `AzureCloud`

#### Hub-spoke pattern

- Deploy Bastion in hub VNet
- Standard SKU required for cross-peering access to VMs in spokes
- One Bastion instance serves all spokes — cost-efficient

#### Exam tips

- Bastion does **not** replace a VPN or ExpressRoute for general connectivity — it's admin access only
- You still need NSGs on VM subnets — Bastion doesn't bypass them; it arrives from the VNet internally
- Diagnostic logs → Log Analytics: captures who connected to which VM and when
- Basic SKU cannot access VMs in peered VNets — Standard SKU required

---

## Combination Patterns

### Pattern 1: Hub-Spoke with Centralised Firewall

**Services:** Azure Firewall + VNet Gateway + Azure Bastion + Route Tables

```
On-Prem ──── VPN/ER Gateway (GatewaySubnet, hub)
                    │ UDR: 0.0.0.0/0 → Firewall
             Azure Firewall (AzureFirewallSubnet, hub)
             Azure Bastion  (AzureBastionSubnet, hub)
                /    │    \
          Spoke1  Spoke2  Spoke3
          (each with UDR: 0.0.0.0/0 → Firewall)
```

**Use when:** Standard enterprise hub-spoke. Firewall enforces all inter-spoke and outbound policy.

---

### Pattern 2: WAF Sandwich (App Gateway + Azure Firewall)

**Services:** Application Gateway (WAF) + Azure Firewall

```
Internet ──── App Gateway (WAF) ──── Azure Firewall ──── Backend VMs
```

**Traffic flow:**

1. App Gateway terminates TLS, applies WAF rules, routes by URL path
2. Azure Firewall applies L4/L7 network rules before traffic hits backends

**Use when:** Web-facing workloads needing both L7 WAF protection and L3/L4 east-west control.

> **Note:** Azure Firewall goes between App GW and backends — not in front of App GW for inbound web traffic. The firewall's DNAT is not used here; App GW is the public-facing entry point.

---

### Pattern 3: NVA with Route Server (Dynamic BGP Routing)

**Services:** NVA + Route Server + (optionally) VPN Gateway

```
On-Prem ──── VPN GW ──── Route Server ←── BGP ──── NVA (SD-WAN/firewall)
                                    routes injected into VNet
```

**Use when:** You need dynamic route learning from on-prem or between branches, without maintaining UDRs. NVA speaks BGP with Route Server; Route Server propagates routes into Azure SDN automatically.

---

### Pattern 4: Private Architecture (No Public IPs on Workloads)

**Services:** Azure Bastion + Private Endpoints + Azure Firewall + ExpressRoute

```
On-Prem ──── ExpressRoute ──── Azure Firewall ──── Private VMs
                                                     (no public IPs)
Users ──── Azure Bastion ──────────────────────────↗
App services ──── Private Endpoints (private IPs for Storage, SQL, etc.)
```

**Use when:** Regulated industries (finance, healthcare) requiring no public internet exposure.

---

### Pattern 5: Scalable Outbound Egress

**Services:** NAT Gateway + (optionally) Azure Firewall

**Option A — NAT Gateway only:**

- Simple, cheap, predictable public IPs for outbound
- No traffic inspection

**Option B — Azure Firewall only:**

- Full FQDN/policy-based filtering
- Firewall's public IPs are used for SNAT

**Option C — Both:**

- Azure Firewall enforces policy
- NAT Gateway handles SNAT with a fixed IP pool
- Route: subnet → Firewall → NAT Gateway → Internet

> Exam note: If both are present on the same subnet, NAT Gateway takes precedence for SNAT over the Firewall's built-in SNAT.

---

### Pattern 6: ExpressRoute + VPN Failover

**Services:** ER Gateway + VPN Gateway (coexistence on same VNet)

```
On-Prem ──── ExpressRoute (primary) ──┐
                                       ├── Same VNet (GatewaySubnet)
On-Prem ──── VPN S2S (failover)   ──┘
```

- Both gateways coexist in `GatewaySubnet` of the same VNet
- Requires ExpressRoute circuit + VPN device on-premises
- BGP enables automatic failover when ER path becomes unavailable

---

## Decision Flowchart

```
Need to expose a web app to the internet?
  ├─ Yes, with WAF/URL routing ────────────────── Application Gateway (WAF_v2)
  └─ Yes, globally across regions ──────────────── Azure Front Door (not in this set)

Need to connect to on-premises?
  ├─ Private, high-bandwidth, low-latency ──────── ExpressRoute
  └─ Over internet, encrypted ─────────────────── VPN Gateway (S2S)

Need to inspect/filter traffic?
  ├─ Managed, FQDN-aware, Azure-native ─────────── Azure Firewall
  └─ Vendor-specific / BGP / advanced IDS/IPS ──── NVA

Need outbound internet egress?
  ├─ Fixed public IPs, no inspection needed ────── NAT Gateway
  └─ Policy-based filtering ────────────────────── Azure Firewall

Need to access PaaS services (Storage, SQL)?
  ├─ Simple, no private IP needed ──────────────── Service Endpoints
  └─ Strict isolation, private IP required ─────── Private Endpoints

Need admin access to VMs?
  └─ No public IPs on VMs ──────────────────────── Azure Bastion

NVA needs routes to propagate automatically?
  └─ BGP-based, no UDR maintenance ─────────────── Route Server
```

---

## Quick Reference: Subnet Requirements

|Service|Required Subnet Name|Min Size|
|---|---|---|
|Application Gateway|Any (dedicated)|/26|
|Azure Firewall|`AzureFirewallSubnet`|/26|
|VPN/ER Gateway|`GatewaySubnet`|/27 (recommend /26)|
|Azure Bastion|`AzureBastionSubnet`|/26|
|Route Server|`RouteServerSubnet`|/27|
|NAT Gateway|Any (attached at subnet level)|No constraint|
|NVA|Any (dedicated recommended)|No constraint|

---

## Exam Watch-Outs

- **Route Server is not a router** — it distributes routes, it does not forward packets
- **Azure Firewall does not speak BGP** — use NVA + Route Server for that
- **NAT Gateway overrides** instance-level public IPs and LB outbound rules on subnets it's attached to
- **Service Endpoints ≠ Private Endpoints** — Service Endpoints do not give PaaS a private IP
- **ExpressRoute circuits are not encrypted by default** — add MACsec or IPsec over ER
- **App Gateway is regional** — use Azure Front Door for global L7 load balancing
- **Bastion Standard SKU** required for cross-peered VNet VM access
- **IP forwarding must be enabled** on NVA NICs in Azure or traffic will be dropped
- **GatewaySubnet** is shared by both VPN and ER gateways in the same VNet
- **Basic VPN SKU** does not support BGP, active-active, zone redundancy, or P2S with IKEv2

---

_Tags: #azure #az700 #networking #hub-spoke #firewall #vpn #expressroute #nva_