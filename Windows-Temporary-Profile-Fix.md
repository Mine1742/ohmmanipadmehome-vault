# Windows Temporary Profile Fix

When a user logs in and finds their desktop and settings reset to “new user” defaults, but some apps remain installed, Windows may have loaded them into a **temporary profile**.

---

## 🔎 Symptoms
- Desktop icons, files, and personalization are missing.  
- Notification may say *“You’ve been logged on with a temporary profile.”*  
- User folder shows as `C:\Users\TEMP` or `C:\Users\username.000`.  

---

## 📂 Cause
- Corrupted user profile (`NTUSER.DAT`).  
- Improper shutdown leaving profile locked.  
- Disk or antivirus interference.  
- Registry mismatch between real and temporary profile.  

---

## 🛠️ Resolution Steps

### 1. Quick Check
- Restart PC → sometimes reloads the correct profile.  
- Run basic disk and system checks:  
  ```cmd
  chkdsk /f
  sfc /scannow
  dism /online /cleanup-image /restorehealth
  ```

---

### 2. Registry Fix (Preferred)

1. Log in as **Administrator** or another account with admin rights.  
2. Open Registry Editor → navigate to:  
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList
   ```
3. Expand `ProfileList` → look for SIDs (`S-1-5-21-xxxxxxxxx`).  
   - One will have `.bak` at the end (the real profile).  
   - Another will be identical without `.bak` (temporary profile).  

4. Fix the entries:  
   - Rename the SID without `.bak` → add `.tmp` to the end.  
   - Rename the SID with `.bak` → remove `.bak`.  

5. Select the restored SID → check **ProfileImagePath**.  
   - Ensure it points to the correct folder:  
     ```
     C:\Users\username
     ```

6. Close Registry Editor → reboot → log the user back in.  

---

### 3. If No `.bak` Profile Exists
- Profile corruption may be deeper. Options:  
  - Run repair commands again (`sfc`, `dism`).  
  - Check Event Viewer (`Applications and Services Logs ➝ Microsoft ➝ Windows ➝ User Profile Service`).  
  - Create a new profile.  

---

### 4. Create a New Profile & Migrate Data
1. Create a new local/domain user account.  
2. Log in once to generate profile.  
3. Copy data from old profile folder:  
   ```
   C:\Users\oldusername
   ```
   into the new profile (`Documents`, `Desktop`, `Favorites`, Outlook PSTs if used).  
4. Reconfigure app settings.  

---

## ✅ Prevention
- Ensure user signs out before shutdown.  
- Regular backups (OneDrive, File History, or central storage).  
- Monitor Event Viewer for disk/profile errors.  

---

## 🔧 Resetting the Ngc Folder (Windows Hello PIN Container)

If PIN setup fails and you cannot delete the `Ngc` folder due to **Access Denied** errors, use these steps:

### Method 1 – Command-Line (Recommended)
Run these in an **elevated Command Prompt**:

```cmd
takeown /F "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Ngc" /R /D Y
icacls "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Ngc" /grant administrators:F /T
rmdir /s /q "C:\Windows\ServiceProfiles\LocalService\AppData\Local\Microsoft\Ngc"
```

Then reboot → go to **Settings → Accounts → Sign-in options** → Add a new PIN.

---

### Method 2 – Safe Mode
1. Boot into **Safe Mode with Networking**.  
2. Repeat the same `takeown`, `icacls`, and `rmdir` commands.  

---

### Method 3 – Built-in Administrator Account
1. Enable the hidden admin account:  
   ```cmd
   net user administrator /active:yes
   ```
2. Log in as **Administrator**.  
3. Delete contents of the Ngc folder.  
4. Log back in as your normal user → reset PIN.  
5. (Optional) Disable the admin account again:  
   ```cmd
   net user administrator /active:no
   ```

---

⚠️ Notes:
- Deleting the `Ngc` folder only clears the Hello PIN container. Users can still log in with their password.  
- On Azure AD joined devices, PIN setup will re-register with Entra ID after reset.  

---

## 🔗 References
- [Microsoft – Fix a corrupted user profile](https://support.microsoft.com/help/14039)  
- [Windows User Profile Service Event Logs](https://learn.microsoft.com/windows/client-management/mdm/user-profile-service-event-ids)  

---

### Tags
#troubleshooting #windows #userprofile #registry #kb #pin #teams #ngc  
