[[Powershell Hub]] [[shared mailbox]] 
#powershell 
# 📄 PowerShell Script: Extract Shared Mailbox Permissions for AP@ArchKey.com and APinvoices@ArchKey.com

This script extracts delegated permission information for the shared mailboxes `AP@ArchKey.com` and `APinvoices@ArchKey.com` using the Exchange Online PowerShell module.

---

## ✅ Purpose

Identify and display:
- Full Access permissions
- Send As permissions
- Send on Behalf permissions

---

## 📜 PowerShell Script

```powershell
# Connect to Exchange Online (Modern Authentication)
Connect-ExchangeOnline -UserPrincipalName your_admin_account@ArchKey.com

# List of shared mailboxes to inspect
$sharedMailboxes = @("AP@ArchKey.com", "APinvoices@ArchKey.com")

# Loop through each shared mailbox
foreach ($mailbox in $sharedMailboxes) {
    Write-Output "`n=== Permissions for $mailbox ===`n"

    # Get mailbox-level permissions (Full Access, etc.)
    Get-MailboxPermission -Identity $mailbox |
        Where-Object { $_.User -notlike "NT AUTHORITY*" -and $_.IsInherited -eq $false } |
        Select-Object Identity, User, AccessRights, Deny | 
        Format-Table -AutoSize

    # Get send-as permissions
    Write-Output "`n-- Send As Permissions --"
    Get-RecipientPermission -Identity $mailbox |
        Where-Object { $_.Trustee -notlike "NT AUTHORITY*" } |
        Select-Object Trustee, AccessRights |
        Format-Table -AutoSize

    # Get send-on-behalf permissions
    Write-Output "`n-- Send on Behalf Permissions --"
    $mbx = Get-Mailbox -Identity $mailbox
    if ($mbx.GrantSendOnBehalfTo) {
        $mbx.GrantSendOnBehalfTo | ForEach-Object {
            Write-Output "SendOnBehalfTo: $_"
        }
    } else {
        Write-Output "No SendOnBehalfTo permissions configured."
    }
}

# Disconnect session when done
Disconnect-ExchangeOnline -Confirm:$false
```

---

## ⚙️ Requirements

- Install Exchange Online PowerShell Module:
```powershell
Install-Module ExchangeOnlineManagement
```

- Ensure you have delegated admin rights to view mailbox permissions.

---

## 🔗 External Resources

- [Exchange Online PowerShell v2 Module](https://learn.microsoft.com/en-us/powershell/exchange/connect-to-exchange-online-powershell)
- [Managing Mailbox Permissions](https://learn.microsoft.com/en-us/exchange/permissions-exo/mailbox-permissions)

---

## 🏷️ Tags

#PowerShell #ExchangeOnline #SharedMailbox #Permissions #ArchKey #Admin #Audit