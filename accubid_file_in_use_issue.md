[[Accubid Hub]]
# Accubid 16 – 'File in Use' Error Troubleshooting

## 🧠 Root Causes

1. **Improper shutdown or crash**

   - Accubid did not close properly and left a lock file.

2. **Stale user session**

   - Accubid still sees your username as active in the project/database.

3. **Shared network drive lock**

   - A file on a network share remains locked even after closing.

4. **Permissions conflict**

   - Your account cannot override or remove the lock.

---

## 🛠️ Fixes and Workarounds

### ✅ 1. Ensure Accubid is Fully Closed

- Open Task Manager (Ctrl+Shift+Esc)
- End any related processes:
  - `Accubid.exe`
  - `Accubid16.exe`
  - `EstWin.exe`

---

### ✅ 2. Delete the Lock File Manually

- Go to the Accubid project or database folder
- Look for files ending in `.LDB` or `.LACCDB`
- Delete the lock file **only if no other users are using the database**

> ⚠️ Caution: Ensure no one else is accessing the file to avoid data corruption.

---

### ✅ 3. Restart the Server or Release File Share Locks

- If on a shared drive:
  - Open `compmgmt.msc` → Shared Folders → Open Files
  - Find and close the locked Accubid file
  Or use PowerShell:
  ```powershell
  Get-SmbOpenFile | Where-Object -Property Path -like "*Accubid*" | Close-SmbOpenFile -Force
  ```

---

### ✅ 4. SQL Environment: Clear Stuck User Session

- If your system uses a SQL backend, ask your admin to:

  ```sql
  KILL [session_id]  -- Replace with actual session ID
  ```

- This removes your stuck SQL session so you can reconnect cleanly.

---

## 📝 Tip

If this happens frequently, consider:

- Enabling auto-kick of inactive users (SQL)
- Improving network drive reliability
- Updating Accubid or backend database for stability improvements

