# Active Directory – Account Lockout Troubleshooting

## Meaning of Greyed-Out "Account is locked out" Checkbox
In ADManager:
- If the **"Account is locked out"** checkbox is **greyed out**, the account is **not currently locked out**.
- The checkbox only becomes available when AD has flagged the account as locked due to failed login attempts.
- You cannot manually lock an account here; you can only **unlock** it.

---

## PowerShell Commands for Account Lockouts

### 1. Check if a user is locked out
```powershell
Get-ADUser -Identity username -Properties LockedOut | 
Select-Object SamAccountName, LockedOut
```
- Replace `username` with the user’s **samAccountName**.
- `LockedOut = True` means the account is locked.

---

### 2. Unlock a locked account
```powershell
Unlock-ADAccount -Identity username
```
- Clears the lockout state immediately.

---

### 3. Check failed password attempts and lockout time
```powershell
Get-ADUser -Identity username -Properties BadPwdCount, LockoutTime | 
Select-Object SamAccountName, BadPwdCount, LockoutTime
```
- **BadPwdCount** → Number of failed logins since last success.
- **LockoutTime** → AD timestamp of when lockout occurred.

---

## Common Causes of Repeated Lockouts
- **Stale credentials** on mobile devices (email, Wi-Fi, VPN apps).
- **Mapped drives** or scheduled tasks using old passwords.
- **Remote Desktop sessions** left running with cached credentials.
- **Service accounts** tied to the user’s credentials.

---

## Resolution Workflow
1. Verify lockout status using PowerShell.  
2. Unlock if necessary.  
3. Check **BadPwdCount** and **LockoutTime** for context.  
4. Investigate devices/services with cached credentials.  
5. Reset password and update across all devices/services if repeated lockouts occur.  

---

## References
- [Microsoft Docs – Unlock-ADAccount](https://learn.microsoft.com/powershell/module/activedirectory/unlock-adaccount)  
- [Microsoft Docs – Get-ADUser](https://learn.microsoft.com/powershell/module/activedirectory/get-aduser)  

---

#tags/ActiveDirectory #tags/Troubleshooting #tags/PowerShell
