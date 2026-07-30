# Contractor SharePoint Link Blocked

## Description
User receives a link from a contractor’s SharePoint site containing RFI documentation.  
When attempting to open, the following error appears:  
**“Website blocked by your Company”**  

Additionally, the link text shows encoding issues such as:  
`Electrical RFI\u0027s` → `Electrical RFI's`

---

## Root Cause
- Company security policies often block access to **external SharePoint/OneDrive tenants**.  
- The `\u0027` is a Unicode escape sequence for an apostrophe (`'`) and is not the actual cause of the block.  
- The real issue is the company firewall/proxy or Entra conditional access blocking external tenant links.

---

## Troubleshooting & Fixes

### 1. Verify Access
- Test the link on a **mobile device using cellular data**.  
  - If it works, the block is enforced only on the company network.

### 2. Request Alternative File Delivery
- Ask the contractor to:
  - Send documents as **email attachments**.  
  - Upload to a **company-approved cloud storage** (internal SharePoint/OneDrive).  

### 3. Correct the Encoded Link
- If the link itself contains `\u0027`, replace with `'`.  
- Example: `Electrical RFI\u0027s` → `Electrical RFI's`.

### 4. Escalation / Whitelisting
- If ongoing access is required:
  - Submit the contractor’s **SharePoint domain** (`tenant.sharepoint.com` or custom domain) to IT/security.  
  - Request a **firewall/proxy exception** or **cross-tenant access policy** in Entra ID.

---

## References
- [Microsoft Docs – SharePoint External Sharing Overview](https://learn.microsoft.com/en-us/sharepoint/external-sharing-overview)  
- [Microsoft Docs – Configure Cross-Tenant Access](https://learn.microsoft.com/en-us/entra/external-id/cross-tenant-access-settings-b2b-collaboration)  

---

## Tags
#sharepoint #contractors #firewall #troubleshooting #external-sharing
