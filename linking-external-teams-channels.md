[[Teams Hub]]
# 🔗 Linking External Teams Channels in Intune + Entra Enterprise Environments

## 🧭 Overview

In an **Intune + Entra ID (formerly Azure AD)** enterprise environment, users cannot directly “link” an external Microsoft Teams channel to an internal organization’s channel. However, Microsoft provides secure ways to collaborate across organizations via **Shared Channels**, **Guest Access**, and **External Access**.

---

## ✅ Supported Ways to Collaborate

### 1. **Shared Channels (Teams Connect)**

Best option for channel-level collaboration across organizations.

#### 🔧 Setup Steps
1. **Enable cross-tenant access** in Entra ID:
   - Go to **Entra Admin Center > External Identities > Cross-tenant access settings**
   - Allow **B2B collaboration** and **B2B direct connect**

2. **Enable Shared Channels** in Teams Admin Center:
   - Go to **Teams > Teams policies > Shared channels** and turn it **On**
   - Assign this policy to required users

3. **Share the Channel**:
   - In Teams, go to a channel > “...” > **Share channel**
   - Invite external users by email

> 🔐 **Note**: Entra Cross-tenant access settings and Intune compliance policies still apply.

---

### 2. **Guest Access (B2B Collaboration)**

Invite external users as guests to internal teams (standard channels only).

#### 🔧 Setup Steps
1. Enable **Guest Access**:
   - **Teams Admin Center > Org-wide settings > Guest access**
2. Allow invitations in Entra ID:
   - **External Identities > External collaboration settings**
3. Add external users to a Team:
   - In Teams > **Add member** > Enter external email

> 🛑 Guests **must switch tenants** and cannot access shared/private channels.

---

### 3. **External Access (Federation)**

Allows chat and meetings with external domains, **not channel access**.

- Use for **1:1 chats**, meetings, and calls only.
- No access to Teams or channels.

---

## ❌ Limitations

| Method             | Channel Linking | Same Interface | File Sharing | Admin Setup Required |
|-------------------|------------------|----------------|--------------|-----------------------|
| Shared Channels   | ✅ Yes           | ✅ Yes         | ✅ Yes       | ✅ Yes                |
| Guest Access      | ❌ No            | ❌ Tenant Switch | ✅ Yes     | ✅ Yes                |
| External Access   | ❌ No            | ✅ Same Tenant | ❌ No        | ✅ Partial            |

---

## 🏷️ Tags
#intune #entra #microsoftteams #sharedchannels #externalcollaboration #azuread #b2b

## 🌐 External Links
- [Microsoft Docs – Shared Channels](https://learn.microsoft.com/en-us/microsoftteams/shared-channels)
- [Microsoft Docs – Guest Access](https://learn.microsoft.com/en-us/microsoftteams/teams-dependencies#guest-access)
- [Microsoft Docs – Cross-Tenant Access](https://learn.microsoft.com/en-us/azure/active-directory/external-identities/cross-tenant-access-overview)
