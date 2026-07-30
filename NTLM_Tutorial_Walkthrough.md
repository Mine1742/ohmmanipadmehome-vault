
[[Authentication Issues]]
# 🔐 NTLM Authentication Protocol: Full Tutorial & Walkthrough

## 📘 What is NTLM?

**NTLM** (NT LAN Manager) is a legacy **authentication protocol** used by Microsoft for client/server authentication.

- Introduced in **Windows NT 3.1** (1993)
- Replaced the even older **LAN Manager (LM)** protocol
- Still supported for **backward compatibility**, especially in mixed or legacy systems

---

## 🧠 Core Concepts

| Term                 | Description                                                           |
|----------------------|------------------------------------------------------------------------|
| **Challenge/Response** | NTLM uses a challenge–response mechanism to authenticate a user       |
| **Hash-based**       | Uses password hashes, not plain-text, but lacks strong encryption     |
| **Stateless**        | No ticket caching like Kerberos — each session reauthenticates       |
| **No mutual auth**   | NTLM authenticates client to server, but **not** server to client     |

---

## ⚙️ NTLM Authentication Flow

### Step-by-Step:

```
1. Client → Server: Negotiation request (supported NTLM version)
2. Server → Client: Challenge (random nonce)
3. Client → Server: Response (encrypted challenge using password hash)
4. Server → DC: Validate client response using stored hash
```

---

## 🔒 NTLM Versions

| Version | Notes                                     |
|---------|-------------------------------------------|
| **LM**  | Very weak (uses DES, 14-character max)     |
| **NTLMv1** | Stronger than LM but still weak (MD4-based) |
| **NTLMv2** | Strongest of the NTLM family, adds HMAC and nonce protection |

> ✅ NTLMv2 is the only recommended version today. LM and NTLMv1 should be disabled.

---

## 🔍 Where is NTLM Still Used?

- Legacy applications or OS that don’t support Kerberos
- Workgroup computers (not joined to a domain)
- When the SPN (Service Principal Name) is missing
- When **time synchronization fails** (Kerberos fails back to NTLM)
- Cross-forest or non-trusted domain scenarios

---

## ⚠️ Why NTLM Is Risky

| Risk Factor           | Explanation                                                  |
|------------------------|--------------------------------------------------------------|
| **No mutual auth**     | Susceptible to man-in-the-middle attacks                    |
| **Pass-the-Hash**      | Reuse of captured hashes can impersonate users              |
| **Replay attacks**     | Challenge/response can be intercepted and reused            |
| **No encryption**      | NTLM doesn't encrypt traffic — just authentication exchange |

---

## 🛡 How to Audit or Reduce NTLM Usage

### 🔎 Audit NTLM in your network (Windows Event Logs):

- Enable logging: Event ID `4624` with `Authentication Package: NTLM`
- Use **Advanced Threat Analytics (ATA)** or **Defender for Identity**

### 🚫 Block NTLM (if Kerberos is available):

1. Group Policy:
   ```
   Computer Config > Windows Settings > Security Settings > Local Policies > Security Options
   ```
   - **Network security: Restrict NTLM**

2. Registry:
   - `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LmCompatibilityLevel`

---

## 🛠 Tools to Investigate NTLM Usage

- `nltest /SC_QUERY:domain` — Check secure channel
- `klist` — Confirm Kerberos tickets are used (lack of ticket = possible NTLM fallback)
- Packet capture: Look for `NTLMSSP_NEGOTIATE` headers in SMB/HTTP traffic

---

## 🔐 NTLM vs Kerberos

| Feature            | NTLM                             | Kerberos                          |
|--------------------|-----------------------------------|-----------------------------------|
| Encryption         | Hash-based (MD4, no session key) | Strong encryption (AES, RC4)      |
| Mutual Authentication | ❌ No                           | ✅ Yes                             |
| Performance        | Slow (per-request auth)           | Fast (ticket reuse)               |
| Scalability        | Poor                              | Excellent (built for AD)          |
| Security           | Weaker (susceptible to hash reuse)| Stronger with replay protection   |

---

## 🔗 External Resources

- [Microsoft: NTLM Overview](https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/ntlm-overview)
- [Pass-the-Hash Attack (MITRE ATT&CK)](https://attack.mitre.org/techniques/T1550/002/)
- [Disable NTLM in Active Directory](https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/network-security-restrict-ntlm-ntlm-authentication-in-this-domain)

---

## 🏷️ Tags

#NTLM #Authentication #LegacyProtocols #Security #ActiveDirectory #Windows #KerberosComparison