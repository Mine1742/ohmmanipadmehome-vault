# 🧰 Help Desk: Unlocking Microsoft Entra (Azure AD) Accounts via PowerShell

## 🧾 Issue
User account is locked due to:
- Too many failed sign-in attempts
- MFA-related lockouts
- Risk-based conditional access blocks

---

## ✅ What You Can Do via PowerShell

### 1. 🔑 Reset the User’s Password
This can **automatically unlock** the account.

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All"
Update-MgUser -UserId user@domain.com -PasswordProfile @{ Password = "NewPassword123!"; ForceChangePasswordNextSignIn = $true }
```

> 💡 Requires Microsoft Graph PowerShell module (`Microsoft.Graph.Users`)

---

### 2. 🚫 Dismiss User Risk (If Locked via Identity Protection)

```powershell
Connect-MgGraph -Scopes "IdentityRiskyUser.ReadWrite.All"

# Check if the user is marked risky
Get-MgRiskyUser -UserId user@domain.com

# Dismiss the risk to allow login
Update-MgRiskyUser -UserId user@domain.com -RiskState "none"
```

> 💡 Requires `Microsoft.Graph.Identity.SignIns` module.

---

### 3. 🔄 Revoke Sign-In Sessions
Helps when the user is stuck due to token or MFA session issues.

```powershell
Revoke-MgUserSignInSession -UserId user@domain.com
```

---

## 🛑 What You Cannot Do via PowerShell

- ❌ You **cannot override smart lockout timers** (e.g., 10 failed password attempts locks account for 60 seconds).
- ❌ You **cannot force-unlock** MFA lockout timers directly.
- ❌ You **cannot disable Conditional Access blocks** tied to risk unless policies are adjusted.

---

## 🧪 Reset MFA in Microsoft Entra Admin Center

> 🔧 Not currently available via PowerShell.

1. Go to: [https://entra.microsoft.com](https://entra.microsoft.com)
2. Navigate to **Users** > Select the user.
3. Click **Authentication methods**.
4. Choose **Require re-register MFA**.

---

## 🔗 Useful Links
- [Dismiss risky users using PowerShell](https://learn.microsoft.com/en-us/entra/id-protection/howto-identityprotection-unblock)
- [Microsoft Graph PowerShell SDK Docs](https://learn.microsoft.com/en-us/powershell/microsoftgraph/overview)

---

## 🏷 Tags
#entra #azuread #powershell #unlock #smartlockout #mfa #helpdesk #identity
