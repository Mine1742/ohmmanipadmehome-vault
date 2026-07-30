[[Networking]][[DNS not resolving]]
# How to Flush DNS Cache on Windows

## Steps

### 1. Open Command Prompt as Administrator

- Press **Start**
- Type: `cmd`
- Right-click **Command Prompt → Run as administrator**

---

### 2. Run the DNS Flush Command

```
ipconfig /flushdns
```

You should see confirmation like:

```
Windows IP Configuration

Successfully flushed the DNS Resolver Cache.
```

---

## Why You Might Want to Flush DNS Cache

| Reason | Explanation |
|---|---|
| Fix website not loading issues | If a site has changed IP but your PC cached the old one |
| After DNS server changes | Like moving from Google DNS to Cloudflare |
| After network troubleshooting | Helps rule out stale DNS entries |

---

## Optional: View DNS Cache Before and After Flush

Run this command:

```
ipconfig /displaydns
```

This will list all currently cached DNS records.

---

## Notes

If you need instructions for Linux or macOS, refer to OS-specific DNS documentation.
