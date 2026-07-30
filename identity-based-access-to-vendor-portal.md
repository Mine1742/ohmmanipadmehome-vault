# 🎯 Identity-Based Access for One User to a Vendor Portal (Any IP)

## ✅ Objective

Allow **one specific user** in your Microsoft Entra tenant to access a **foreign-hosted vendor portal** from **any IP address**, based **only on their verified identity**, using Conditional Access.

---

## 🛠️ Step-by-Step Setup

### 1. ✅ Confirm Vendor Portal Supports Entra ID Login

Ensure the vendor portal:
- Supports **SAML, OIDC, or OAuth** authentication
- Can be added as an **Enterprise Application** in Entra ID

📍 Navigate to:  
**Entra Admin Center > Enterprise applications > New application**

---

### 2. ✅ Create a Conditional Access Policy (Allow for One User)

📍 Location:  
**Entra Admin Center > Protection > Conditional Access**

#### 🎛️ Policy Settings:

- **Users or workload identities**:  
  - Select the **specific user** who needs access

- **Cloud apps or actions**:  
  - Select the **vendor portal** enterprise app

- **Conditions**:  
  - Skip **location** (this allows access from any IP)
  - Optionally configure **device platform** or **sign-in risk**

- **Grant Controls**:  
  - ✅ Require **multi-factor authentication (MFA)**
  - ✅ Optionally require compliant or hybrid-joined device

- **Session Controls** (optional):  
  - Use **sign-in frequency** or **app enforced restrictions** if needed

- **Enable Policy**: ✅ On

---

### 3. ❌ Create a Deny-All Policy for Others (Optional but Recommended)

To block access for all other users in your tenant:

- **Users**: Select **All users**, then **exclude** the allowed user
- **App**: Select the same **vendor portal app**
- **Grant**: Block access
- **Enable**: ✅ On

---

## 🔐 Optional Enhancements

| Feature                      | Purpose                                   |
|------------------------------|-------------------------------------------|
| Sign-in Risk Policy          | Blocks suspicious sign-in attempts       |
| Named Locations + MFA        | Extra trust from known IPs               |
| PIM (Privileged Identity Mgmt) | Time-limited role elevation             |
| Identity Protection Policies | Automate access restrictions             |

---

## 🧠 Summary

| Goal                              | Solution                                |
|-----------------------------------|-----------------------------------------|
| One user access from any IP       | Identity-based Conditional Access       |
| Identity verification             | Require MFA                             |
| Restrict tenant-wide access       | Block policy for other users            |

---

## 🏷️ Tags
#entra #conditionalaccess #identitywhitelisting #azuread #vendorportal #mfa #obsidian-note

## 🌐 External Links
- [Conditional Access Overview](https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/overview)
- [Enterprise App Setup](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application)
- [Identity Protection](https://learn.microsoft.com/en-us/azure/active-directory/identity-protection/overview)
