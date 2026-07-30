# EXO Calendar Delegation — Folder Identity Normalization (Fix)
**Last updated:** 2025-08-27

## Symptom
Running `Add-MailboxFolderPermission` or `Get-MailboxFolderPermission` with an Identity like:
```
Brian.Douglas@archkey.com:/Calendar
```
returns:
```
The mailbox folder identity ... isn't in the correct format. The correct format should look like this: "<MailboxIdentity>:\<FolderPath>"
```

## Cause
`Get-MailboxFolderStatistics` returns **FolderPath** as `/Calendar` (forward slash). Exchange expects a **backslash** after the colon, e.g. `Mailbox:\Calendar`. Passing `Mailbox:/Calendar` fails.

## Quick Fix (copy/paste)
```powershell
# Inputs
$MailboxPrimarySmtp = 'Brian.Douglas@archkey.com'
$DelegateUserPrincipalName = 'John.simm@archkey.com'

# 1) Get the calendar folder path (localization-safe)
$calPath = Get-MailboxFolderStatistics -Identity $MailboxPrimarySmtp -FolderScope Calendar |
  Where-Object { $_.FolderType -eq 'Calendar' -and $_.Name -ne 'Birthdays' } |
  Select-Object -First 1 -ExpandProperty FolderPath    # e.g. /Calendar

# 2) Normalize: forward -> backslash, trim leading slashes
$normPath = ($calPath -replace '/', '').TrimStart('')  # -> Calendar

# 3) Build canonical EXO folder identity
$folderId = '{0}:\{1}' -f $MailboxPrimarySmtp, $normPath  # -> Brian.Douglas@archkey.com:\Calendar
$folderId  # sanity check

# 4) Grant & verify
Add-MailboxFolderPermission -Identity $folderId -User $DelegateUserPrincipalName -AccessRights Editor
Get-MailboxFolderPermission -Identity $folderId
```

## Drop‑in Script (Delegate_Cal_Normalized.ps1)
```powershell
param(
  [Parameter(Mandatory=$true)] [string]$MailboxPrimarySmtp,
  [Parameter(Mandatory=$true)] [string]$DelegateUserPrincipalName,
  [ValidateSet('Owner','PublishingEditor','Editor','PublishingAuthor','Author','NonEditingAuthor','Reviewer','Contributor','LimitedDetails','AvailabilityOnly','None')]
  [string]$AccessRights = 'Editor',
  [switch]$WhatIf
)

Import-Module ExchangeOnlineManagement -ErrorAction SilentlyContinue | Out-Null
try { Disconnect-ExchangeOnline -Confirm:$false -ErrorAction SilentlyContinue } catch {}
Connect-ExchangeOnline -ShowBanner:$false

# Resolve calendar folder path (localization-safe)
$calPath = Get-MailboxFolderStatistics -Identity $MailboxPrimarySmtp -FolderScope Calendar |
  Where-Object { $_.FolderType -eq 'Calendar' -and $_.Name -ne 'Birthdays' } |
  Select-Object -First 1 -ExpandProperty FolderPath

if (-not $calPath) { throw "Could not resolve a Calendar folder for $MailboxPrimarySmtp." }

# Normalize path and build identity
$normPath = ($calPath -replace '/', '').TrimStart('')
$folderId = '{0}:\{1}' -f $MailboxPrimarySmtp, $normPath
Write-Host "Using folder identity: $folderId"

# Add/Update/Remove
$existing = Get-MailboxFolderPermission -Identity $folderId -ErrorAction SilentlyContinue |
  Where-Object { $_.User -and $_.User.ToString().Trim().ToLower() -eq $DelegateUserPrincipalName.ToLower() }

if ($AccessRights -eq 'None') {
  if ($existing) {
    if ($WhatIf) { Write-Host "[WhatIf] Remove-MailboxFolderPermission -Identity `"$folderId`" -User `"$DelegateUserPrincipalName`"" }
    else { Remove-MailboxFolderPermission -Identity $folderId -User $DelegateUserPrincipalName -Confirm:$false }
  } else { Write-Host "No existing permission to remove." }
} else {
  if ($existing) {
    if ($WhatIf) { Write-Host "[WhatIf] Set-MailboxFolderPermission -Identity `"$folderId`" -User `"$DelegateUserPrincipalName`" -AccessRights $AccessRights" }
    else { Set-MailboxFolderPermission -Identity $folderId -User $DelegateUserPrincipalName -AccessRights $AccessRights }
  } else {
    if ($WhatIf) { Write-Host "[WhatIf] Add-MailboxFolderPermission -Identity `"$folderId`" -User `"$DelegateUserPrincipalName`" -AccessRights $AccessRights" }
    else { Add-MailboxFolderPermission -Identity $folderId -User $DelegateUserPrincipalName -AccessRights $AccessRights }
  }
}

Get-MailboxFolderPermission -Identity $folderId | Format-Table -AutoSize
```

## Verify
```powershell
Get-MailboxFolderStatistics -Identity $MailboxPrimarySmtp -FolderScope Calendar |
  ft Name,FolderType,FolderPath

$folderId
Get-MailboxFolderPermission -Identity $folderId
```

## References
- Microsoft Docs – Add-MailboxFolderPermission: https://learn.microsoft.com/powershell/module/exchange/add-mailboxfolderpermission
- Microsoft Docs – Get-MailboxFolderStatistics: https://learn.microsoft.com/powershell/module/exchange/get-mailboxfolderstatistics

## Tags
#KB/ExchangeOnline #KB/Outlook #KB/Calendar #Delegation #PowerShell #Troubleshooting