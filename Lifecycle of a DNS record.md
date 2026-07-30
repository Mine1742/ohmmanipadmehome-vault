#dns 
# DNS Record Lifecycle

## Stage 1 — Record Creation

Everything starts when an administrator creates or modifies a DNS record. This happens through the DNS provider's portal (Azure DNS, Cloudflare, GoDaddy) or programmatically via API/PowerShell.

```powershell
Add-DnsServerResourceRecordA `
  -ZoneName "archkey.com" `
  -Name "vpn" `
  -IPv4Address "203.0.113.50" `
  -TimeToLive 00:05:00
```

At this point, only the primary authoritative name server knows about the new record. No resolver or client anywhere on the internet has seen it yet.

---

## Stage 2 — Zone Transfer & Propagation to Secondary NS

The primary NS increments the zone's `SOA` serial number. Secondary name servers periodically poll the primary (based on the SOA refresh interval, typically 15–60 minutes) and request a zone transfer when they see a newer serial:

- **AXFR** — full zone transfer (entire zone file)
- **IXFR** — incremental zone transfer (only the deltas)

With cloud DNS providers (Azure DNS, Cloudflare, Route 53), this happens almost instantly since they use internal replication rather than traditional zone transfers.

With on-prem AD-integrated DNS zones, replication follows the AD replication topology — usually within 15 minutes intra-site, and governed by the inter-site replication schedule for cross-site. This is your propagation floor for internal records; the SOA refresh interval is irrelevant because AD replication handles it.

---

## Stage 3 — Global Propagation Delay

Even after all authoritative servers have the new record, the _old_ version may still be cached by recursive resolvers worldwide. This is the "DNS propagation" window.

The worst case is bounded by the **previous record's TTL**. If the old A record had a 3600s (1 hour) TTL, resolvers that cached it right before the change won't re-query for up to an hour.

There is no actual push mechanism. "DNS propagation" is really just "waiting for old TTL-bounded caches to expire." It is entirely pull-based.

### The pre-migration TTL playbook

1. Lower the TTL to 300s (or 60s) on the record you plan to change.
2. Wait one full cycle of the **old** TTL (if it was 3600s, wait an hour).
3. Make the actual change (new IP, new MX target, etc.).
4. Verify resolution from multiple vantage points.
5. Once confirmed, raise the TTL back to your normal operational value.

---

## Stage 4 — Client Query & Recursive Resolution

A client (workstation, phone, server) needs to reach `vpn.archkey.com`. The resolution path:

1. **Stub resolver** — the OS checks its local DNS cache first (Windows DNS Client service, `systemd-resolved` on Linux).
2. **Cache miss** — the stub resolver sends a recursive query to its configured resolver (ISP, `8.8.8.8`, the AD DNS server, etc.).
3. **Iterative walk** — the recursive resolver walks the DNS tree:

```
Step 1: Query root servers (.)
        → Referral: "Try the .com TLD servers"

Step 2: Query .com TLD servers
        → Referral: "Try the archkey.com authoritative NS"

Step 3: Query archkey.com authoritative NS
        → Answer: "vpn.archkey.com = 203.0.113.50, TTL=300"
```

Each intermediate answer (the NS referrals for `.com` and `archkey.com`) is also cached by the resolver. Subsequent queries for any `*.archkey.com` name skip steps 1–2 entirely.

### Recursion vs. iteration

- The **client → resolver** query is **recursive**: the client asks once and expects a final answer.
- The **resolver → authoritative** queries are **iterative**: the resolver follows referrals step by step on its own.

---

## Stage 5 — Caching & TTL Countdown

The recursive resolver caches the response and starts a TTL countdown. Every subsequent query for the same record from any client using that resolver gets the cached answer — no trip to the authoritative server required.

### Multiple cache layers

|Layer|Location|Typical behavior|
|---|---|---|
|Browser cache|Chrome, Firefox, Edge|~60s regardless of TTL (Chrome); varies by browser|
|OS stub resolver|Windows DNS Client, systemd-resolved|Honors TTL from the response|
|Recursive resolver|ISP, 8.8.8.8, AD DNS server|Honors TTL; serves all clients behind it|
|Intermediate NS referrals|Recursive resolver|Cached separately (NS for `.com`, NS for `archkey.com`)|

While cached, the record is "alive" in the network — fast to resolve, but potentially stale if the authoritative version has changed. There is no mechanism to remotely invalidate a resolver's cache.

### Flushing local caches

```powershell
# Windows — flush the OS DNS cache
Clear-DnsClientCache

# Verify a specific record
Resolve-DnsName -Name "vpn.archkey.com" -Type A -DnsOnly
```

```bash
# Linux (systemd-resolved)
sudo resolvectl flush-caches

# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

Flushing your local cache only affects your machine. It does not flush the upstream recursive resolver's cache.

---

## Stage 6 — TTL Expiry & Re-Query

When the TTL hits zero, the resolver evicts the cached entry. The next client query for that name triggers a fresh iterative resolution back to the authoritative servers — the cycle returns to Stage 4.

### TTL trade-offs

|TTL value|Propagation speed|Authoritative query load|Use case|
|---|---|---|---|
|60–300s|Fast (1–5 min)|High|Records you change often, pre-migration windows, failover|
|900–3600s|Moderate (15–60 min)|Medium|Standard operational records|
|86400s (1 day)|Slow (up to 24 hr)|Low|Stable records (MX, NS) that rarely change|

### Negative caching (NXDOMAIN)

When a queried name doesn't exist, the authoritative server returns `NXDOMAIN`. The resolver caches this negative response too, using the TTL from the SOA record's **minimum** field. This prevents repeated lookups for names that don't exist, but it also means that after you _create_ a new record, resolvers that recently got an NXDOMAIN for that name won't re-query until the negative cache TTL expires.

---

## Stage 7 — Record Update or Deletion

### Update

When you modify a record (change the IP, update the TTL, add a new MX entry), the lifecycle restarts from Stage 1. Old cached copies persist worldwide until their individual TTL expires — you cannot force remote resolvers to flush.

### Deletion

When you delete a record, the same TTL-bounded propagation window applies. After deletion:

- Queries return `NXDOMAIN` if no records of any type remain at that name.
- Queries return `NODATA` if other record types still exist at that name (e.g., you deleted the A record but a TXT record remains).
- The negative result is cached per the SOA minimum TTL.

### Critical change playbook (IP migration, MX cutover)

```
1. Lower TTL to 300s (or 60s)
2. Wait one full old-TTL cycle
3. Make the change
4. Verify from multiple locations (dig, Resolve-DnsName, online checkers)
5. Monitor for stragglers (clients with aggressive local caching)
6. Raise TTL back to operational value
```

---

## Key Concepts Summary

- **There is no DNS push mechanism.** All propagation is pull-based, bounded by TTL.
- **TTL is the single most important operational lever.** It controls propagation speed, query load, and staleness risk.
- **Multiple cache layers exist** (browser, OS, resolver), each with independent behavior.
- **Negative caching matters.** Creating a brand-new record can be delayed by NXDOMAIN caches from the SOA minimum TTL.
- **AD-integrated zones replicate via AD replication**, not zone transfers. Propagation timing follows site topology, not SOA refresh.
- **Pre-change TTL reduction** is the standard operational pattern for any planned DNS change.