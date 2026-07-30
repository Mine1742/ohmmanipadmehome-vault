[[Powershell Hub]] [[O365]]

# Export and Apply Distribution Group Memberships in Exchange Online

## Scenario
You need to copy distribution group memberships from one user to another in Microsoft 365 Exchange Online (e.g., when someone takes over a role).

---

## ✅ Prerequisites

- Exchange Online PowerShell module installed:
  ```powershell
  Install-Module ExchangeOnlineManagement -Scope CurrentUser -Force
  ```
- Import the module and connect:
  ```powershell
  Import-Module ExchangeOnlineManagement
  Connect-ExchangeOnline -UserPrincipalName your.email@archkey.com
  ```

---

## 🔹 Step 1: Export Source User's Group Memberships

```powershell
$sourceUser = "samantha.schnell@archkey.com"

$groups = Get-DistributionGroup -ResultSize Unlimited | Where-Object {
    (Get-DistributionGroupMember -Identity $_.Identity -ResultSize Unlimited |
     Where-Object { $_.PrimarySmtpAddress -eq $sourceUser })
}

$groups | Select-Object Name | Export-Csv -Path "$env:USERPROFILE\Desktop\sourceUserGroups.csv" -NoTypeInformation
```

- This creates a CSV on your Desktop listing all groups the source user is a member of.

---

## 🔹 Step 2: Apply Those Groups to a New User

```powershell
$targetUser = "new.user@archkey.com"
$groupList = Import-Csv -Path "$env:USERPROFILE\Desktop\sourceUserGroups.csv"

foreach ($group in $groupList) {
    Add-DistributionGroupMember -Identity $group.Name -Member $targetUser
}
```

---

## 🔎 Notes and Tips

- If you get ambiguous group name errors (e.g., `Estimating` matches multiple entries), use full email addresses:
  ```powershell
  Get-DistributionGroupMember -Identity "estimating@archkey.com"
  ```

- You may increase result size visibility with:
  ```powershell
  Get-DistributionGroup -ResultSize Unlimited
  ```

- Always validate group names before mass-adding users to avoid misplacement.

---

## 🧼 Cleanup

After confirming the new user is added to all necessary groups, you can disconnect:
```powershell
Disconnect-ExchangeOnline
```
