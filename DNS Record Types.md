# DNS Record Types Breakdown
#dns 
## Core / Most Common Records

### A (Address)

- **Purpose:** Maps a hostname to an IPv4 address.
- **Example:** `server1.archkey.com → 203.0.113.50`
- **Notes:** The most fundamental DNS record. Every publicly reachable host needs one (or a CNAME pointing to one). TTL is typically 300–3600s.

### AAAA (IPv6 Address)

- **Purpose:** Maps a hostname to an IPv6 address.
- **Example:** `server1.archkey.com → 2001:0db8:85a3::8a2e:0370:7334`
- **Notes:** Identical function to A, but for IPv6. Dual-stack environments publish both A and AAAA records.

### CNAME (Canonical Name)

- **Purpose:** Creates an alias that points to another hostname (the canonical name).
- **Example:** `www.archkey.com → archkey.com`
- **Notes:** Cannot coexist with other record types at the same name (no CNAME + MX at zone apex). Cannot be placed at the zone apex in standard DNS — use ALIAS/ANAME if your provider supports it. Adds an extra lookup hop.

### MX (Mail Exchange)

- **Purpose:** Directs email to the mail server(s) for a domain.
- **Example:** `archkey.com → 10 archkey-com.mail.protection.outlook.com`
- **Notes:** Priority value (lower = preferred). For M365 environments, typically points to `*.mail.protection.outlook.com`. Must point to an A/AAAA record, never a CNAME.

### TXT (Text)

- **Purpose:** Stores arbitrary text; heavily used for verification and email security.
- **Common uses:**
    - **SPF** — `v=spf1 include:spf.protection.outlook.com -all`
    - **DKIM** — Public key for email signing (often via CNAME to provider's key).
    - **DMARC** — `v=DMARC1; p=reject; rua=mailto:dmarc@archkey.com`
    - **Domain verification** — Entra ID, Google Workspace, third-party SaaS.
- **Notes:** 255-char limit per string, but multiple strings can be concatenated in a single TXT record. Wrap long SPF records carefully to avoid lookup limits (10 DNS lookups max for SPF).

### NS (Name Server)

- **Purpose:** Delegates a domain or subdomain to specific authoritative name servers.
- **Example:** `archkey.com → ns1.provider.com, ns2.provider.com`
- **Notes:** Set at the registrar for the zone apex. Used for subdomain delegation (e.g., delegating `lab.archkey.com` to a different DNS provider or Azure DNS zone).

### SOA (Start of Authority)

- **Purpose:** Contains zone metadata — primary NS, admin email, serial number, refresh/retry/expire timers, negative caching TTL.
- **Example:** `archkey.com SOA ns1.provider.com admin.archkey.com 2024010101 3600 900 604800 86400`
- **Notes:** One per zone. The serial number must increment on every zone change (YYYYMMDDNN format is common). The minimum TTL field controls how long NXDOMAIN responses are cached.

---

## Service Discovery & Connectivity

### SRV (Service Locator)

- **Purpose:** Specifies the host and port for a specific service.
- **Format:** `_service._protocol.domain TTL IN SRV priority weight port target`
- **Example:** `_sip._tls.archkey.com → 10 60 5061 sipserver.archkey.com`
- **Common uses:**
    - Active Directory domain controller location (`_ldap._tcp.dc._msdcs.domain.com`)
    - SIP/VoIP, XMPP
    - Microsoft Teams/Skype for Business autodiscover
- **Notes:** Priority works like MX (lower = preferred). Weight allows load distribution among same-priority targets.

### PTR (Pointer)

- **Purpose:** Reverse DNS — maps an IP address back to a hostname.
- **Example:** `50.113.0.203.in-addr.arpa → server1.archkey.com`
- **Notes:** Lives in the `in-addr.arpa` (IPv4) or `ip6.arpa` (IPv6) zone. Required for mail servers to pass reverse DNS checks. Typically managed by your ISP or hosting provider. Must match the A record's forward lookup for FCrDNS (Forward-Confirmed Reverse DNS).

---

## Email Authentication & Security

### SPF (via TXT)

- **Purpose:** Declares which IP addresses/hosts are authorized to send email for a domain.
- **Mechanism:** Receiving server looks up the sender domain's TXT record for `v=spf1 ...`.
- **Key modifiers:** `include:`, `ip4:`, `ip6:`, `a`, `mx`, `redirect=`, `~all` (soft fail), `-all` (hard fail).
- **Gotcha:** 10 DNS lookup limit — nested `include:` chains count. Use `ip4:/ip6:` to flatten if hitting the limit.

### DKIM (via CNAME or TXT)

- **Purpose:** Publishes the public key used to verify DKIM signatures on outbound email.
- **Format:** `selector._domainkey.domain` → TXT record with `v=DKIM1; k=rsa; p=<base64-public-key>`
- **Notes:** M365 uses two selectors (`selector1`, `selector2`) published as CNAMEs pointing to Microsoft's key infrastructure. Rotate keys periodically.

### DMARC (via TXT)

- **Purpose:** Tells receiving servers what to do when SPF and DKIM both fail alignment, and where to send aggregate/forensic reports.
- **Record name:** `_dmarc.domain.com`
- **Example:** `v=DMARC1; p=reject; rua=mailto:dmarc-reports@archkey.com; pct=100`
- **Policies:** `none` (monitor), `quarantine` (junk), `reject` (drop).

---

## Security & Trust

### TLSA (DANE)

- **Purpose:** Associates a TLS certificate (or its public key/hash) with a domain, enabling certificate pinning via DNS.
- **Requires:** DNSSEC on the zone.
- **Use case:** Securing SMTP (MTA-STS alternative), HTTPS certificate pinning.

### CAA (Certification Authority Authorization)

- **Purpose:** Specifies which Certificate Authorities are allowed to issue certificates for the domain.
- **Example:** `archkey.com CAA 0 issue "letsencrypt.org"`
- **Tags:** `issue` (standard certs), `issuewild` (wildcard certs), `iodef` (violation reporting URL/email).
- **Notes:** CAs are required to check CAA before issuance. Helps prevent misissuance.

### SSHFP (SSH Fingerprint)

- **Purpose:** Publishes the fingerprint of an SSH server's host key in DNS.
- **Use case:** Automated SSH host key verification (requires DNSSEC or a trusted resolver).

### DNSSEC Records

|Record|Purpose|
|---|---|
|**DNSKEY**|Zone's public signing key|
|**DS**|Delegation Signer — hash of child zone's DNSKEY, published in parent zone|
|**RRSIG**|Digital signature over a record set|
|**NSEC/NSEC3**|Authenticated denial of existence (proves a name doesn't exist)|

---

## Aliasing & Redirection

### ALIAS / ANAME (Provider-Specific)

- **Purpose:** CNAME-like functionality at the zone apex.
- **Example:** `archkey.com ALIAS archkey.azurewebsites.net`
- **Notes:** Not an official RFC record type — implemented by providers like Cloudflare (CNAME flattening), Azure DNS, Route 53, etc. Resolves at query time and returns A/AAAA records to the client.

### DNAME (Delegation Name)

- **Purpose:** Redirects an entire subtree of the DNS namespace to another domain.
- **Example:** `old.archkey.com DNAME new.archkey.com` — any query for `x.old.archkey.com` is rewritten to `x.new.archkey.com`.
- **Notes:** Useful for domain migrations and renaming. Applies to all names below the DNAME record, not the name itself.

---

## Modern / Specialized Records

### HTTPS / SVCB (Service Binding)

- **Purpose:** Advertises connection parameters for HTTPS (or generic services) — including ALPN protocols, ECH keys, target name, port, and IP hints.
- **Example:** `archkey.com HTTPS 1 . alpn="h2,h3" ipv4hint=203.0.113.50`
- **Notes:** Enables browsers to connect via HTTP/3 on the first request (no Alt-Svc upgrade needed). Supports Encrypted Client Hello (ECH). Increasingly adopted — Cloudflare, Apple, and major browsers support it.

### NAPTR (Naming Authority Pointer)

- **Purpose:** Supports URI/service rewriting rules, used in ENUM (phone-number-to-SIP mapping) and SIP routing.
- **Notes:** Complex regex-based rewriting. Mostly relevant in telecom/VoIP environments.

### LOC (Location)

- **Purpose:** Stores geographic coordinates (latitude, longitude, altitude) for a domain.
- **Notes:** Rarely used in practice. Informational only.

### HINFO (Host Information)

- **Purpose:** Describes the CPU and OS of a host.
- **Notes:** Largely deprecated due to security concerns (information disclosure).

### OPENPGPKEY

- **Purpose:** Publishes a user's OpenPGP public key in DNS for email encryption discovery.
- **Format:** Hashed local-part of email address under `_openpgpkey.domain`.

---

## Microsoft / Active Directory Specific

These aren't unique DNS record _types_, but are critical record patterns in AD/Entra hybrid environments:

|Record|Purpose|
|---|---|
|`_ldap._tcp.dc._msdcs.domain.com` (SRV)|Domain controller locator|
|`_kerberos._tcp.domain.com` (SRV)|Kerberos KDC locator|
|`_gc._tcp.forest.com` (SRV)|Global Catalog locator|
|`_sip._tls.domain.com` (SRV)|Skype/Teams SIP federation|
|`autodiscover.domain.com` (CNAME)|Exchange/Outlook autodiscover|
|`lyncdiscover.domain.com` (CNAME)|Skype for Business/Teams discovery|
|`enterpriseregistration.domain.com` (CNAME)|Entra ID device registration (Workplace Join)|
|`enterpriseenrollment.domain.com` (CNAME)|Intune MDM auto-enrollment|
|`msoid.domain.com` (CNAME)|Microsoft Online ID verification|
|`selector1._domainkey.domain.com` (CNAME)|M365 DKIM key 1|
|`selector2._domainkey.domain.com` (CNAME)|M365 DKIM key 2|

---

## Quick Reference Table

|Type|Points To|Zone Apex?|Primary Use|
|---|---|---|---|
|A|IPv4 address|✅|Host resolution|
|AAAA|IPv6 address|✅|Host resolution (IPv6)|
|CNAME|Hostname|❌|Aliasing|
|MX|Mail server hostname|✅|Email routing|
|TXT|Text string|✅|SPF, DKIM, DMARC, verification|
|NS|Name server hostname|✅|Zone delegation|
|SOA|Zone metadata|✅|Zone authority|
|SRV|Host + port|✅|Service discovery|
|PTR|Hostname (reverse)|N/A|Reverse DNS|
|CAA|CA name|✅|Certificate issuance control|
|TLSA|Cert hash|✅|DANE / cert pinning|
|HTTPS/SVCB|Service params|✅|HTTP/3, ECH, connection hints|
|DNAME|Domain subtree|✅|Subtree redirection|
|ALIAS|Hostname (flattened)|✅|Apex CNAME workaround|
|NAPTR|Rewrite rule|✅|SIP/ENUM routing|

---

_Reference compiled May 2026._