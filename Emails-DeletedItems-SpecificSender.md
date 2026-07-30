# Emails from Specific Sender Going to Deleted Items

## Issue  
Some emails from `nromano@borderstates.com` are being automatically moved to the **Deleted Items** folder, even though no Outlook rules are configured by the user.

---

## Root Causes to Check  

1. **Hidden or Server-Side Rules**
   - Outlook (Desktop):  
     `File → Manage Rules & Alerts → Check rules`
   - Outlook on the Web (OWA):  
     `Settings → Mail → Rules`  
     Look for server-side rules.

2. **Sweep Rules (OWA only)**
   - `Settings → Mail → Sweep`  
   - Sweep rules may silently move or delete emails.

3. **Junk Email / Blocked Senders**
   - OWA: `Settings → Mail → Junk Email`  
   - Ensure the address/domain is not listed under **Blocked Senders**.  
   - Add the sender/domain to **Safe Senders**.

4. **Retention / Folder Policies**
   - Retention tags may automatically move or delete messages.  
   - Check mailbox retention policies in OWA or with IT admin.

5. **Exchange Transport Rules (Admin Level)**
   - IT Admin: `Exchange Admin Center → Mail Flow → Rules`  
   - A server-side transport rule may be moving/deleting messages from `@borderstates.com`.

6. **Add-Ins / Security Tools**
   - Third-party services (Proofpoint, Mimecast, Barracuda, etc.) can auto-move flagged mail.  

---

## Quick Fix  

- Add `nromano@borderstates.com` to **Safe Senders** list (desktop & OWA).  
- Test by having the sender email a plain-text message.  

---

## Escalation  

If emails are still moved:
- Escalate to IT to review **Exchange transport rules**.  
- Request a review of any **security filtering policies** that may apply to this sender or domain.  

---

## References  
- [Microsoft: Block or allow (junk email settings)](https://support.microsoft.com/en-us/office/block-or-allow-junk-email-settings-d917d1e0-3a93-4aca-a2c5-dccc6a70fc3a)  
- [Microsoft: Inbox rules in Outlook on the web](https://support.microsoft.com/en-us/office/manage-email-messages-by-using-rules-in-outlook-on-the-web-8400435c-f14e-4272-9004-1548bb1848f2)  

---

## Tags  
#email #outlook #exchange #troubleshooting #rules  
