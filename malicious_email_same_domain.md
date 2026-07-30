# Detecting and Preventing Malicious Email From Your Own Domain

## Overview
Emails appearing to come from your own domain can be the result of **spoofing**, **internal account compromise**, or **third-party service abuse**. Even with an NGFW and Exchange, these attacks can slip through without proper email authentication and filtering.

---

## 1. Understanding SPF, DKIM, and DMARC

### SPF (Sender Policy Framework)
- **Purpose:** Ensures the sending server is authorized to send for your domain.
- **Stops:** Spoofed domains using unauthorized mail servers.
- **Bypassed if:** SPF is missing, misconfigured, or set to "softfail".

### DKIM (DomainKeys Identified Mail)
- **Purpose:** Validates message integrity and that it was authorized by your domain.
- **Stops:** Forged messages without a valid DKIM signature.
- **Bypassed if:** DKIM not implemented, or attacker has a valid signing key (e.g., compromised sending system).

### DMARC (Domain-based Message Authentication, Reporting, and Conformance)
- **Purpose:** Instructs receivers what to do if SPF/DKIM fail and ensures the visible From: aligns with them.
- **Stops:** Spoofed emails when SPF/DKIM fail and policy is `quarantine` or `reject`.
- **Bypassed if:** DMARC policy is `none` or too lenient; compromised accounts pass SPF/DKIM.

---

## 2. Common Attack Scenarios

| Scenario                      | SPF Result | DKIM Result | DMARC Result | Outcome |
|--------------------------------|-----------|-------------|--------------|---------|
| **Domain Spoofing**            | Fail      | Fail        | Fail → Reject (if strict) | Blocked if strict DMARC |
| **Compromised Internal Account**| Pass      | Pass        | Pass         | Delivered unless malware filter catches it |
| **Third-Party Service Abuse**  | Pass      | Pass        | Pass         | Delivered unless sandbox detects malicious file |

---

## 3. Immediate Detection & Investigation Steps
1. **Check Message Headers** – Confirm source IP, SPF/DKIM/DMARC results.
2. **Correlate with Logs** – In Exchange message trace, confirm sending server.
3. **Run SIEM Query** – Search for similar messages in last 7–14 days.
4. **Scan Attachments** – Use sandbox detonation (Safe Attachments, NGFW AV).
5. **Audit User Accounts** – Look for impossible travel, forwarding rules, suspicious logins.

---

## 4. Prevention & Hardening Checklist

### Email Authentication
- [ ] Publish and maintain **SPF** with only authorized sending IPs/hosts.
- [ ] Enable **DKIM** signing for outbound mail.
- [ ] Enforce **DMARC** policy to `quarantine` or `reject`.

### Filtering Enhancements
- [ ] Apply attachment scanning to **all messages**, including internal-to-internal.
- [ ] Enable **Safe Attachments** and **Safe Links** in Microsoft Defender for Office 365.
- [ ] Configure NGFW SMTP inspection and sandboxing for inbound/outbound.

### Account Security
- [ ] Enforce MFA for all users.
- [ ] Monitor for unusual sign-ins and auto-forward rules.
- [ ] Review delegated permissions regularly.

### Monitoring & Reporting
- [ ] Enable DMARC aggregate and forensic reports.
- [ ] Use tools like [MXToolbox DMARC Analyzer](https://mxtoolbox.com/DMARC.aspx) to monitor compliance.

---

## 5. External Resources
- [SPF Record Setup Guide](https://dmarcian.com/create-spf-record/)
- [DKIM Setup for Microsoft 365](https://learn.microsoft.com/en-us/microsoft-365/security/office-365-security/use-dkim-to-validate-outbound-email)
- [DMARC Policy Documentation](https://dmarc.org/overview/)

---

## Internal Tags
#email-security #spf #dkim #dmarc #exchange #ngfw #threat-prevention #kb
