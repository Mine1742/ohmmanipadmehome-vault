# Bluebeam Revu 21 – Cannot Save to PC or OneDrive

## Description
User reports that they cannot save any files from **Bluebeam Revu 21** to either the **local PC** or **OneDrive**.

---

## Root Cause Possibilities
1. **Permissions issue** – User account lacks write access to the destination folder.  
2. **Bluebeam settings/config corruption** – Default save path is invalid or broken.  
3. **OneDrive sync conflict** – OneDrive paused, out of space, or restricted by company policies.  
4. **File path or character issues** – Long path names or restricted characters blocking save.  
5. **Application repair needed** – Bluebeam Revu installation corrupted.

---

## Troubleshooting & Fixes

### Step 1 – Local PC Save Test
- Attempt to save directly to `C:\Users\<username>\Documents\`.  
- If saving fails:
  - Check **NTFS permissions**.  
  - Verify **disk space availability**.  

### Step 2 – OneDrive Validation
- Ensure **OneDrive is signed in and running**.  
- Check the **sync status** in the system tray.  
- Confirm there is no OneDrive storage quota issue.  
- Test saving into `OneDrive\Documents` instead of root.

### Step 3 – Reset Bluebeam Save Settings
- In **Bluebeam Revu**:  
  - Go to **Revu > Preferences > General > File Access**.  
  - Reset or update the **default folder path**.

### Step 4 – Repair Bluebeam Revu
- Go to **Control Panel > Programs and Features**.  
- Select **Bluebeam Revu 21** → *Repair*.  

### Step 5 – Advanced Isolation
- Test **Save As > Desktop**.  
  - If this works, issue is isolated to **OneDrive folder permissions**.  
  - If it still fails, reinstall Bluebeam Revu or check for endpoint security blocking file writes.

---

## References
- [Bluebeam Revu File Access Guide](https://support.bluebeam.com/articles/revu-file-access/)  
- [Microsoft OneDrive Restrictions & Limitations](https://learn.microsoft.com/en-us/sharepoint/sync-restrictions-limitations)  

---

## Tags
#bluebeam #onedrive #filesave #troubleshooting #permissions
