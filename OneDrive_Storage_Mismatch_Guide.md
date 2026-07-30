
# 📦 OneDrive Storage Mismatch – Why Reported Size Is Larger Than Actual Files

If OneDrive reports you're using **950 GB** of space but you only see **97 GB** of files, here's what could be happening and how to investigate.

---

## 🧠 Common Causes of Storage Discrepancy

### 🗑 1. Deleted Files Still in Recycle Bin
OneDrive retains deleted files in its **cloud recycle bin**, which still consumes space.

🔍 **Check**:  
[https://onedrive.live.com/?id=RecycleBin](https://onedrive.live.com/?id=RecycleBin)

---

### 🕐 2. Version History Accumulation
OneDrive keeps **multiple versions** of files like Word or Excel. Large files that are edited often can take up significant space.

🔍 **Check**:  
Right-click a file in OneDrive Web > **Version History**

---

### 👥 3. Shared Files from Others
Files shared with you and added via **"Add shortcut to My files"** can count against **your storage quota**.

🔍 **Check**:  
Go to OneDrive Web > **My Files** and look for folders with a “shared” icon.

---

### 👻 4. Hidden or System Files
Temporary, sync, or configuration files may not appear in File Explorer but still take up space.

💡 **Tool Suggestion**:  
Use **TreeSize Free** or **WinDirStat** to scan disk usage.

---

### 🔐 5. Files in Personal Vault
Files in the **Personal Vault** don’t always appear in regular folders but still count toward storage.

🔍 **Check**:  
Open OneDrive Web > Navigate to “Personal Vault”

---

### 🔄 6. Pending Uploads or Sync Issues
OneDrive may be stuck syncing large or corrupt files. These can reserve space but won’t appear visibly.

🔍 **Check**:  
Click the OneDrive icon > **View sync problems**

---

### 👤 7. Multiple Accounts or Linked Storage
Files across **work and personal accounts** may be displayed or counted together incorrectly if both are connected.

---

## ✅ How to Troubleshoot and Reclaim Space

| Step | Action |
|------|--------|
| 🧹 Recycle Bin | Empty your OneDrive Recycle Bin |
| 🗂 Storage Manager | Visit [Manage Storage](https://onedrive.live.com/options/ManageStorage) |
| 📦 Disk Audit | Use tools like TreeSize or WinDirStat to view real file sizes |
| ⚠️ Sync Problems | Check for stuck or failed syncs |
| 🔒 Personal Vault | Ensure it's not holding unseen files |

---

## 📎 Quick Links

- 🔗 [OneDrive Recycle Bin](https://onedrive.live.com/?id=RecycleBin)
- 🔗 [Manage OneDrive Storage](https://onedrive.live.com/options/ManageStorage)
- 🔗 [OneDrive Help Center](https://support.microsoft.com/en-us/onedrive)

---
