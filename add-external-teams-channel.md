[[Teams Hub]]
# 🌐 How to Add an External Teams Channel to Your Channel List

## ✅ Overview

To add an external Microsoft Teams channel to your Teams interface, you must be **invited to a shared channel** from another organization via **Teams Connect**. This shared channel appears automatically in your Teams app—**no manual addition required**.

---

## 🧾 Prerequisites

| Requirement | Description |
|-------------|-------------|
| Microsoft 365 Account | Must be licensed for Microsoft Teams |
| Shared Channels Enabled | Both orgs must enable shared channels in Teams policies |
| Cross-Tenant Access | Must be configured in Microsoft Entra ID for B2B Direct Connect |
| Channel Invitation | You must be invited by the external team/channel owner |

---

## 👣 Steps to Add an External Shared Channel

### 🔗 Step 1: Receive an Invitation
- The external team/channel owner invites you to a shared channel using your email address.

### 📩 Step 2: Accept the Invitation
- Accept the invite via email or Teams prompt (if required).

### 📥 Step 3: View the Channel
- The external channel appears in your **Teams sidebar**, labeled with the **external org name**.
- You can chat, share files, and collaborate **without switching tenants**.

---

## 🛠️ How to Configure Cross-Tenant Access in Entra ID

> This must be done by a Microsoft 365 administrator **in both organizations**.

### 🔧 Steps:
1. Go to **Microsoft Entra Admin Center**:  
   [https://entra.microsoft.com](https://entra.microsoft.com)

2. Navigate to:  
   `External Identities > Cross-tenant access settings`

3. Select **“Default settings”** or configure **“Organizational settings”** for a specific tenant.

4. Under **B2B direct connect**, do the following:
   - Enable **inbound access** (allow external users from the other tenant)
   - Enable **outbound access** (allow your users to connect to theirs)
   - Under **Applications**, allow **Microsoft Teams** access

5. Under **Trust Settings**, configure MFA and device compliance settings as needed.

6. Click **Save** to apply the policy.

> ✅ Repeat the process on the external organization’s side for bidirectional sharing.

---

## 🔍 Identifying Shared Channels

- Shared channels show in the Teams list with:
  - A **link icon** or **“external”** label
  - The **external organization’s name** underneath

---

## 🚫 Limitations

| Limitation | Details |
|------------|---------|
| Manual Add | You cannot manually add external shared channels |
| Tenant Switching | Not required for shared channels (only for guest access) |
| Channel Type | Only **shared channels** support cross-org embedding |

---

## 🧠 Tips

- Ask your IT admin to verify **Teams policy** allows shared channels.
- Confirm the external org’s **cross-tenant access settings** are properly configured.
- Use **Entra logging** to troubleshoot B2B access issues.

---

## 🏷️ Tags
#teams #externalchannel #sharedchannels #entra #microsoft365 #crossorgcollaboration #b2b

## 🌐 External Links
- [Microsoft Docs – Shared Channels](https://learn.microsoft.com/en-us/microsoftteams/shared-channels)
- [Microsoft Docs – Cross-Tenant Access](https://learn.microsoft.com/en-us/azure/active-directory/external-identities/cross-tenant-access-overview)
