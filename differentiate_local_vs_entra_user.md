# Differentiate Local vs Entra User in PowerShell

## Overview
In a Microsoft Entra + Intune-managed environment, you may sign in to Windows using one identity (your local or domain account) and to Microsoft Graph using another (your Entra ID account). PowerShell treats these as **two separate identity contexts**.

- **Local or Domain Identity** → Used by Windows for file access and system rights.
- **Cloud (Entra) Identity** → Used for Microsoft Graph, Azure AD, Intune, and other cloud APIs.

Because of this separation, `whoami` and Microsoft Graph may show different users.

---

## 1. Check Current Local or Domain User (Windows Context)

Use any of the following commands:

```powershell
whoami
```
Outputs `DOMAIN\username`, e.g.:
```
denpro\albert.smith
```

Or check the environment variables:
```powershell
$env:USERNAME
$env:USERDOMAIN
```

For detailed information including SID and authentication type:
```powershell
[System.Security.Principal.WindowsIdentity]::GetCurrent()
```

---

## 2. Check Current Entra ID (Microsoft Graph Context)

After connecting to Microsoft Graph with:
```powershell
Connect-MgGraph -Scopes "User.Read.All"
```
You can verify which cloud identity is active:
```powershell
(Get-MgContext).Account
```
Example output:
```
albert.smith@archkey.com
```
This shows the signed-in Entra user for Microsoft Graph, which may differ from your local Windows login.

---

## 3. Switch Accounts in PowerShell

To sign out and connect as another Entra user:
```powershell
Disconnect-MgGraph
Connect-MgGraph -Scopes "User.Read.All" -ForceRefresh
```
When prompted, choose **Use another account** and sign in with the desired credentials.

To verify again:
```powershell
(Get-MgContext).Account
```

For switching Windows accounts, use:
```powershell
runas /user:DOMAIN\another.user "powershell"
```
Or to elevate:
```powershell
Start-Process powershell -Verb RunAs
```

---

## 4. Verify Through Entra Portal (GUI)

1. Go to [https://mysignins.microsoft.com/security-info](https://mysignins.microsoft.com/security-info)
2. Review your **current sign-in session**, including the Entra ID account used.
3. If managing multiple tenants or identities, you can also check:
   [https://entra.microsoft.com/#view/Microsoft_AAD_IAM/UsersManagementMenuBlade/~/Overview](https://entra.microsoft.com)
   → Top right corner → Account avatar → Shows signed-in user.
4. To switch users, sign out and reauthenticate using the desired Entra credentials.

---

## 5. Key Takeaways
- `whoami` = Windows/Domain user context.
- `(Get-MgContext).Account` = Entra/Graph user context.
- They are independent and can differ.
- Use `-ForceRefresh` when reconnecting to Graph to override cached sessions.

---

## References
- [Microsoft Graph PowerShell Docs](https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview)
- [Entra Admin Center](https://entra.microsoft.com)
- [Check Your Sign-Ins](https://mysignins.microsoft.com/security-info)

---

**Tags:** #entra #intune #powershell #graphapi #mfa #admin #troubleshooting