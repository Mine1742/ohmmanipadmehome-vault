[[Entra]]
# 🔄 Changing a User's UPN in Entra ID (Azure AD)

## 🧾 Summary
Changing a user's **User Principal Name (UPN)** in Microsoft Entra ID (formerly Azure AD) is possible via the Entra admin portal. However, the change may not propagate to all associated services automatically, and there are key differences between **cloud-only** and **hybrid** environments.

---

## ✅ What Changes Automatically
- The UPN (`username@domain.com`) becomes the new **sign-in name**.
- The Entra ID login syncs across Microsoft 365 services.
- Email **aliases typically remain unchanged** (but primary email does not automatically update).

---

## ⚠️ What Does *Not* Automatically Change
| Affected Item         | Behavior |
|-----------------------|----------|
| 📧 Primary Email Address | May remain unchanged unless updated in **Exchange Online** |
| 📁 OneDrive URL         | Retains **original UPN** in path |
| 💻 Windows Login (Hybrid) | Can cause login issues if not updated via **on-prem AD** |
| 🔗 SharePoint / Teams   | May still reference **old UPN** |
| 🔄 Synced Accounts      | Must be changed in **on-prem AD**, not directly in Entra |

---

## 🛠 Best Practices

### 🔹 For Cloud-Only Accounts
1. Go to **Entra admin center** → **Users**.
2. Select the user and click **Edit username**.
3. Change UPN to desired value.
4. Save changes.

✅ UPN is updated for sign-in.  
❗ Manually update Exchange Online aliases if needed.

---

### 🔸 For Hybrid (Synced) Accounts
> 🔥 Do **not** change UPN in Entra ID.

Instead:
1. Open **Active Directory Users and Computers (ADUC)**.
2. Update the `userPrincipalName` attribute.
3. Let **Entra Connect** sync the change.

---

## 📌 Post-Change Checklist
- [ ] Notify user about the new login.
- [ ] Update **email aliases** or **primary SMTP** if needed.
- [ ] Confirm **OneDrive/SharePoint** access is unaffected.
- [ ] Reconfigure affected apps or Power Automate flows.
- [ ] MFA may require **re-authentication**.

---

## 🔗 External Links
- [Change a UPN in Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity/users/change-user-name)
- [How UPN changes affect OneDrive and Teams](https://learn.microsoft.com/en-us/onedrive/user-name-changes)

---

## 🏷 Tags
#entra #azuread #upn #hybrid #cloudonly #identity #m365 #troubleshooting
