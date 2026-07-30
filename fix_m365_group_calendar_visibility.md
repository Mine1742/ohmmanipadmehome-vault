# 🛠 Fix: Microsoft 365 Group Calendar Not Visible in Outlook

## 📋 Overview
This guide explains why a Microsoft 365 Group calendar may not appear in Outlook and how to fix the issue.  
Typical error message:
> “Cannot display the folder. The server mailbox cannot be opened because this address book entry is not a mail user.”

---

## 🧠 Root Cause
This happens when:
1. The group isn’t fully provisioned with an Exchange mailbox.
2. The user is an **Owner** but not a **Member** of the group.
3. Outlook is caching a stale directory entry.
4. The group was created in Entra/Teams but not directly in Exchange.

Exchange Online permissions treat **Owners** and **Members** separately:
- **Owners** can manage settings.
- **Members** can access the mailbox and calendar.

> Even if you’re an owner, you won’t see the group’s calendar until you’re also added as a member.

---

## 🧩 Verify the Group Type

First, connect to Exchange Online PowerShell:
```powershell
Install-Module ExchangeOnlineManagement -Force
Import-Module ExchangeOnlineManagement
Connect-ExchangeOnline -UserPrincipalName yourname@yourdomain.com
```

Then check if the group is a Unified (Microsoft 365) Group:
```powershell
Get-UnifiedGroup -Identity "Fire & Life Safety Fire Alarm Service" | fl DisplayName,PrimarySmtpAddress,AccessType
```
If no SMTP address is returned, the Exchange mailbox hasn’t been created yet.

---

## 🧱 Check Group Membership

List all owners:
```powershell
Get-UnifiedGroupLinks -Identity "Fire & Life Safety Fire Alarm Service" -LinkType Owners
```

List all members:
```powershell
Get-UnifiedGroupLinks -Identity "Fire & Life Safety Fire Alarm Service" -LinkType Members
```

---

## 🔧 Fix: Add Owners as Members

If you’re an owner but not listed as a member, run:
```powershell
Add-UnifiedGroupLinks -Identity "Fire & Life Safety Fire Alarm Service" -LinkType Members -Links "yourname@domain.com"
```

To automate for all owners:
```powershell
$Owners = (Get-UnifiedGroupLinks -Identity "Fire & Life Safety Fire Alarm Service" -LinkType Owners).PrimarySmtpAddress
foreach ($owner in $Owners) {
    Add-UnifiedGroupLinks -Identity "Fire & Life Safety Fire Alarm Service" -LinkType Members -Links $owner -ErrorAction SilentlyContinue
}
```

After this, all owners will also be members and will see the group’s calendar and mailbox in Outlook.

---

## 💻 Refresh Outlook
1. Close and reopen Outlook.
2. Remove the cached group entry:
   - **File → Options → Mail → Send Messages → Empty Auto-Complete List**
3. Add the group again:
   - **Calendar → Add Calendar → From Address Book → [Group Name]**

The group should now appear under **Groups → Calendar**.

---

## 🧠 Summary

| Role | Can Manage Group | Can Access Calendar | Must Be Member |
|------|------------------|---------------------|----------------|
| Owner only | ✅ Yes | ❌ No | ✅ Yes |
| Member only | ❌ No | ✅ Yes | N/A |
| Owner + Member | ✅ Yes | ✅ Yes | ✅ Ideal combo |

---

## 🔗 References
- [Microsoft Docs – Manage Microsoft 365 Groups in Exchange Online](https://learn.microsoft.com/en-us/powershell/module/exchange/set-unifiedgroup)
- [Troubleshoot missing group calendars in Outlook](https://learn.microsoft.com/en-us/microsoft-365/admin/create-groups/manage-groups)
- [Exchange Online PowerShell Module](https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell-v2)

---

**Internal Tags:**  
#O365 #ExchangeOnline #Calendar #UnifiedGroup #PowerShell #Troubleshooting
