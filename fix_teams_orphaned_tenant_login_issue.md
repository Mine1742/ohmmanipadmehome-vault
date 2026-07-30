# 🛠 Resolving Orphaned Tenant Issues in Microsoft Teams (New Teams v2)

**Last Updated:** 2025-07-24

---

## 🔍 Overview

This guide outlines the comprehensive steps to resolve a Microsoft Teams login issue related to an **orphaned organization account** (e.g., Parsons Electric) that causes Teams to loop login attempts or throw errors — especially when the user can no longer authenticate against the old org.

---

## 🧠 Root Cause

This issue is commonly caused by:
- Orphaned Azure AD tenant references
- Web Account Manager (WAM) token corruption
- Residual Microsoft authentication tokens
- Incomplete profile cleanup
- Conflicts between new Teams and previous org login states

---

## 🧼 Step-by-Step Resolution Guide

### 🔹 Step 1: Quit Teams Completely

- Right-click the Teams icon in the system tray > **Quit**
- Or open Task Manager (`Ctrl + Shift + Esc`) and end any **Teams** process

---

### 🔹 Step 2: Delete Teams Cache and App Data

#### For **new Teams (Store version)**:

Delete the following directories:

```plaintext
%LocalAppData%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache
%LocalAppData%\Packages\MSTeams_8wekyb3d8bbwe\TempState
%LocalAppData%\Packages\MSTeams_8wekyb3d8bbwe\Settings
%LocalAppData%\Packages\MSTeams_8wekyb3d8bbwe\AC
```

#### (Optional) Classic Teams:

```plaintext
%AppData%\Microsoft\Teams
```

---

### 🔹 Step 3: Purge Credential Manager Entries

1. Open **Credential Manager**
2. Go to **Windows Credentials**
3. Delete all entries related to:
   - `msteams`
   - `aad`
   - `live`
   - `MicrosoftOffice16_Data`
   - Anything related to **Parsons Electric**, `aadg.windows.net`, `teams.microsoft.com`

---

### 🔹 Step 4: Disconnect Azure AD or WAM Orgs

1. Go to:
   ```plaintext
   Settings > Accounts > Access Work or School
   ```
2. **Remove/Disconnect** the orphaned organization (e.g., Parsons Electric)
3. If this fails, use:
   ```cmd
   sysdm.cpl > Advanced > User Profiles > Settings
   ```
   and remove stale profiles.

---

### 🔹 Step 5: Run WAM Cleanup via PowerShell

Open **PowerShell as Administrator** and run:

```powershell
dsregcmd /leave
```

⚠️ **Caution**: This will disconnect the machine from Azure AD if joined. Use only if tenant disconnection is required.

---

### 🔹 Step 6: Reboot and Re-authenticate

1. Restart the PC
2. Launch Teams
3. Login using **valid org credentials** only (e.g., `INRS Enterprises LLC`)
4. Confirm **Parsons Electric** is no longer shown under profiles

---

## 🧪 Optional Troubleshooting Step

### Create a new local user profile and test login

This will help verify if the issue is limited to a corrupted user profile.

---

## 📎 Related Tags
#Teams #Microsoft365 #TenantCleanup #WAM #HelpDesk #Intune #AzureAD #TeamsLoginError

## 🔗 External Resources
- [Leave an Azure AD organization](https://myaccount.microsoft.com/organizations)
- [Microsoft Teams Troubleshooting Docs](https://learn.microsoft.com/en-us/microsoftteams/troubleshoot)

