[[Onedrive]] [[O365]] [[Excel Hub]]
# 🛠 OneDrive + Excel Sync Troubleshooting Guide

If you're seeing missing content (e.g., a line item like `MCP-076`) or Excel shows **"Saved to this PC"** while OneDrive claims files are synced, you may be experiencing a **local desync issue**.

---

## 🧠 Problem Summary

- Excel file opened appears **incomplete** or missing recent data.
- Message says **"Saved to this PC"**, not to OneDrive.
- OneDrive icon says **"Your files are synced"**, but changes from other devices aren’t visible.

---

## ✅ Step-by-Step Fix

### 🔹 1. Confirm File Path in Excel

- Go to **File > Info**
- Check the file path:
  - ✅ Should be something like:  
    `C:\Users\<YourName>\OneDrive - Company\...`
  - ❌ If it says: `This PC > Documents` → you’re working locally, not in OneDrive

---

### 🔹 2. Reopen File from OneDrive Sync Folder

1. Open File Explorer
2. Navigate to:  
   `C:\Users\<YourName>\OneDrive - Your Organization`
3. Locate and open the Excel file from this directory

---

### 🔹 3. Force OneDrive to Resync

1. Right-click the **OneDrive cloud icon** in the system tray
2. Select **"Pause syncing"** for 2 minutes
3. Then click **"Resume syncing"**
4. Watch for sync animations or warnings

---

### 🔹 4. Check for Version Conflicts

1. In Excel: **File > Info > Version History**
2. Review prior versions to see if the missing entry (like `MCP-076`) is in an earlier save
3. You can **restore or copy** content from older versions

---

### 🔹 5. Upload Local Copy to Cloud (If Needed)

1. Save the current file to your Desktop
2. Reopen the correct cloud version from OneDrive folder
3. Copy missing data (like `MCP-076`) from the desktop file into the cloud file
4. Save the cloud file and ensure it now syncs properly

---

### 🧪 Optional: Reset OneDrive Sync

If sync still fails or is unreliable:

1. Press `Win + R`, then run:
   ```
   %localappdata%\Microsoft\OneDrive\onedrive.exe /reset
   ```

2. Restart OneDrive manually:
   ```
   %localappdata%\Microsoft\OneDrive\onedrive.exe
   ```

---

## 🧠 Tip

Always check file paths when working in Excel — OneDrive-synced files will reference the OneDrive directory. Files opened from "This PC" are local copies and may not sync.

---

For persistent issues, report to IT or log into [https://onedrive.live.com](https://onedrive.live.com) and confirm if the correct version is stored online.
