
# Removing Local Admin Rights in Windows (Local & Azure Hybrid)

## 1. Local Machine Method

### Check Current Local Administrators
```
net localgroup Administrators
```

### Remove a User from Local Administrators
```
net localgroup Administrators DOMAIN\username /delete
```
or for local users:
```
net localgroup Administrators username /delete
```

If the user reappears after reboot, another system (Azure, Intune, GPO, Autopilot) is re-adding them.

---

## 2. Azure Hybrid / Entra ID Method

Local admin rights in a hybrid environment may be coming from one or more centralized sources. Use these steps to permanently remove them.

---

### Step 1 — Check Azure AD "Device Administrators"

Go to:
Entra Admin Center → Devices → Device Settings → Additional local administrators on Azure AD joined devices

Remove the user if listed.

Reboot device.

---

### Step 2 — Check Intune Local Admin Policies

Go to:
Intune → Endpoint Security → Account Protection → Local user group membership

OR:

Intune → Devices → Configuration Profiles

Look for any policy that assigns users/groups to the Administrators group.

Remove user or group.

---

### Step 3 — Check Group Policy (On‑Prem AD)

Run:
```
gpresult /r
```

Look under:
Restricted Groups
Managed Local Groups

If a domain group contains the user and is applied to Administrators, edit GPO:

GPO → Computer Config → Windows Settings → Security Settings → Restricted Groups

Remove the assignment or user.

---

### Step 4 — Check Autopilot Profiles

Go to:
Intune → Devices → Enroll Devices → Deployment Profiles

If “User Account Type” is set to Administrator, the first user who signs in becomes a local admin.

Change to Standard if needed.

---

## Summary Table

| Source of Admin Rights | How to Remove |
|------------------------|----------------|
| Local Administrators group | Remove via `net localgroup` command |
| Azure AD Device Administrator | Remove from Entra Device Administrator role |
| Intune Local Admin assignment | Adjust Endpoint Security/Configuration profile |
| Group Policy Restricted Groups | Remove membership in GPO |
| Autopilot Profile | Change user account type |
