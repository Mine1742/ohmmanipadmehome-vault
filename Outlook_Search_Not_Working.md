[[Outlook Hub]]
# Outlook Search Not Working 

This document provides troubleshooting steps for when Outlook search stops working, especially after changes in network environment or travel.

## Common Symptoms

* Outlook search yields no results.
* Search is very slow or incomplete.
* Error messages related to indexing or search.

## Troubleshooting Steps

### 1. Basic Checks (Always Start Here)

* **Restart Outlook:** Close Outlook completely and reopen it.
* **Restart Your Computer:** Perform a full system restart.
* **Check Internet Connection:** Ensure stable internet access (less likely for local search, but good to verify).
* **Cached Exchange Mode:**
    * Go to `File > Account Settings > Account Settings`.
    * Double-click your email account.
    * Ensure "Use Cached Exchange Mode" is **checked**.
    * If you change this setting, restart Outlook and allow time for your mailbox to re-sync.

### 2. Rebuild the Search Index (Most Common Fix)

Outlook search relies on the Windows Search Index. This is frequently the cause of search issues.

1. **Open Indexing Options:**
    * Type `Indexing Options` in the Windows Start menu search bar and select it.
2. **Modify Indexed Locations:**
    * In the Indexing Options window, click **"Modify"**.
    * Ensure the checkbox next to **"Microsoft Outlook"** is selected. If not, check it and click "OK."
3. **Rebuild the Index:**
    * In the Indexing Options window, click **"Advanced"**.
    * Under "Troubleshooting," click **"Rebuild"**.
    * Confirm the warning. This process can take a long time (hours to overnight) depending on the size of your Outlook data. Search results may be incomplete until finished.

### 3. Check Outlook Search Scope

Ensure the search scope is correctly set.

* When in the Outlook search bar, check options like "Current Mailbox," "Current Folder," or "All Outlook Items" and select the appropriate scope for your search.

### 4. Check Outlook Add-ins

Faulty add-ins can interfere with Outlook's functionality.

1. **Start Outlook in Safe Mode:**
    * Press `Win + R` to open the Run dialog.
    * Type `outlook.exe /safe` and press `Enter`.
    * If search works in Safe Mode, an add-in is likely the cause.
2. **Disable Add-ins (if Safe Mode works):**
    * Go to `File > Options > Add-ins`.
    * Next to "Manage: COM Add-ins," click **"Go..."**.
    * Uncheck add-ins one by one, restart Outlook normally, and test search after each until you identify the problematic one.

### 5. Repair Office Installation

A corrupted Office installation can cause various problems.

1. **Close all Office applications.**
2. Go to `Windows Start > Settings > Apps > Apps & features`.
3. Find your **Microsoft 365** or **Microsoft Office** installation.
4. Click on it, then select **"Modify"**.
5. Try **"Quick Repair"** first. If that doesn't resolve it, try **"Online Repair"** (requires internet and takes longer).

### 6. Check the Windows Search Service

Ensure the Windows Search service is running correctly.

1. Type `services.msc` in the Start menu search bar and open "Services."
2. Scroll down and find **"Windows Search"**.
3. Right-click on it and select **"Properties"**.
4. Ensure "Startup type" is set to **"Automatic (Delayed Start)"** or **"Automatic"**.
5. If "Service status" is not "Running," click **"Start"**.
6. Click "OK."

### 7. Update Outlook/Office

Keep your Office suite up to date for the latest fixes.

* In Outlook, go to `File > Office Account > Update Options > Update Now`.

---

**Important Note:** After performing an index rebuild (Step 2), allow significant time for the indexing process to complete before expecting full search functionality. This can take hours, especially for large mailboxes.
