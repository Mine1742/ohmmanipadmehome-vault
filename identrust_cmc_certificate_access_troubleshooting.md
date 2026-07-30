# 🔒 IdenTrust CMC – “You must use your certificate” Error

*Guide created 2025-07-26*

---

## 1  What the message means
The Certificate Management Center (CMC) requires **client‑certificate (mutual TLS)** authentication.  
If no certificate is presented during the handshake, the portal returns:

> **Status Screen**  
> You must use your certificate to access CMC.  

---

## 2  Likely causes

| Cause | Quick check |
|-------|-------------|
| **🔌 Token / smart‑card not detected** | USB token unplugged, PIN dialog dismissed, driver not running |
| **📜 Certificate expired or revoked** | Browser still offers an old cert |
| **🌐 Browser never prompted** | Chromium may suppress prompt if only one (invalid) cert found |
| **🔒 TLS inspection / proxy** | Corporate proxy strips the client‑cert request |

---

## 3  Fix‑it checklist

1. **Insert token / smart‑card** and wait for Windows to recognise it  
   *Device Manager → Smart card readers* shows the reader.

2. **Restart browser** completely (close all tabs & processes).  
   Re‑open **Edge/Chrome/Firefox**.

3. **Browse directly to**  
   ```
   https://secure.identrust.com/CMC
   ```  
   – When prompted, select the **current, valid certificate**.

4. **No prompt? Force it**  
   `edge://settings/certificates` → **Personal** → remove old/expired certs → retry.

5. **Check validity**  
   Double‑click cert → **Details → Valid to**.  
   If expired, **renew** or purchase a new certificate.

6. **Bypass SSL inspection**  
   Connect off‑network (mobile hotspot) to rule out proxy interference.

---

## 4  Still stuck?

| Next step | Details |
|-----------|---------|
| **IdenTrust Support** | support@identrust.com • +1‑888‑248‑4447 |
| **Re‑install middleware** | SafeNet Authentication Client / ActivClient |
| **Try another PC** | Confirms whether local cert store is corrupted |

---

### Tags
#IdenTrust #CMC #certificate #mutualTLS #EOFException #troubleshooting
