# Calendar Delegation in Microsoft 365 (Exchange Online)
**Last updated:** 2025-08-27

## Quick steps (OWA)
1. Outlook on the web → Calendar → **Share** (or **… → Sharing and permissions**).  
2. Add the person → choose: **Can view when I’m busy**, **Can view titles and locations**, **Can view all details**, **Can edit**, or **Delegate** → **Share**.

## Quick steps (Outlook Desktop)
1. Outlook → Calendar → right-click **Calendar** → **Sharing Permissions…** (or **Properties → Permissions**).  
2. **Add** user → choose Permission Level (Owner/Publishing Editor/Editor/Publishing Author/Author/NonEditingAuthor/Reviewer/Contributor/LimitedDetails/AvailabilityOnly).  
3. (Optional) **Delegate Access…** → check **Delegate can see my private items** and/or **Receive meeting-related messages**.

## PowerShell script
See `Set-CalendarDelegation.ps1` below (handles localized Calendar names, add/update/remove, optional SendOnBehalf/FullAccess).

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$MailboxPrimarySmtp,
    [Parameter(Mandatory=$true)]
    [string]$DelegateUserPrincipalName,
    [ValidateSet('Owner','PublishingEditor','Editor','PublishingAuthor','Author','NonEditingAuthor','Reviewer','Contributor','LimitedDetails','AvailabilityOnly','None')]
    [string]$AccessRights = 'Editor',
    [switch]$GrantSendOnBehalf,
    [switch]$GrantFullAccess,
    [switch]$WhatIf
)
try { Disconnect-ExchangeOnline -Confirm:$false -ErrorAction SilentlyContinue } catch {}
Connect-ExchangeOnline -ShowBanner:$false
$calFolderIdentity = (Get-MailboxFolderStatistics -Identity $MailboxPrimarySmtp -FolderScope Calendar |
    Where-Object { $_.FolderType -eq 'Calendar' -and $_.Name -ne 'Birthdays' } |
    Select-Object -First 1 -ExpandProperty Identity)
if (-not $calFolderIdentity) { throw "Could not resolve default Calendar folder for $MailboxPrimarySmtp." }
$existing = Get-MailboxFolderPermission -Identity $calFolderIdentity -ErrorAction SilentlyContinue |
    Where-Object { $_.User -and $_.User.ToString().Trim().ToLower() -eq $DelegateUserPrincipalName.ToLower() }
if ($AccessRights -eq 'None') {
    if ($existing) {
        if ($WhatIf) {
            Write-Host "[WhatIf] Remove-MailboxFolderPermission -Identity `"$calFolderIdentity`" -User `"$DelegateUserPrincipalName`""
        } else {
            Remove-MailboxFolderPermission -Identity $calFolderIdentity -User $DelegateUserPrincipalName -Confirm:$false
        }
    }
} else {
    if ($existing) {
        if ($WhatIf) {
            Write-Host "[WhatIf] Set-MailboxFolderPermission -Identity `"$calFolderIdentity`" -User `"$DelegateUserPrincipalName`" -AccessRights $AccessRights"
        } else {
            Set-MailboxFolderPermission -Identity $calFolderIdentity -User $DelegateUserPrincipalName -AccessRights $AccessRights
        }
    } else {
        if ($WhatIf) {
            Write-Host "[WhatIf] Add-MailboxFolderPermission -Identity `"$calFolderIdentity`" -User `"$DelegateUserPrincipalName`" -AccessRights $AccessRights"
        } else {
            Add-MailboxFolderPermission -Identity $calFolderIdentity -User $DelegateUserPrincipalName -AccessRights $AccessRights
        }
    }
}
if ($GrantSendOnBehalf) {
    if ($WhatIf) {
        Write-Host "[WhatIf] Set-Mailbox -Identity `"$MailboxPrimarySmtp`" -GrantSendOnBehalfTo @{Add=`"$DelegateUserPrincipalName`"}"
    } else {
        Set-Mailbox -Identity $MailboxPrimarySmtp -GrantSendOnBehalfTo @{Add=$DelegateUserPrincipalName}
    }
}
if ($GrantFullAccess) {
    if ($WhatIf) {
        Write-Host "[WhatIf] Add-MailboxPermission -Identity `"$MailboxPrimarySmtp`" -User `"$DelegateUserPrincipalName`" -AccessRights FullAccess -AutoMapping:$true"
    } else {
        Add-MailboxPermission -Identity $MailboxPrimarySmtp -User $DelegateUserPrincipalName -AccessRights FullAccess -AutoMapping:$true -InheritanceType All
    }
}
Get-MailboxFolderPermission -Identity $calFolderIdentity | Format-Table -AutoSize
```