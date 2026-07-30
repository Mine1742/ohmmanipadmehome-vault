[[Onedrive]][[Sharepoint Hub]]
# SharePoint and OneDrive Sync Troubleshooting Guide

This document outlines steps to troubleshoot when documents are not syncing between a SharePoint folder and your OneDrive folder.

## Common Causes

- Sync not properly initialized
- File path or name issues
- Conflicting files
- OneDrive account mismatches
- Storage limits

---

## 1. Confirm the Folder Is Synced

- Go to the **SharePoint document library** in your browser.
- Click **“Sync”** in the toolbar (requires OneDrive client).
- Confirm that OneDrive prompts you that syncing has begun.

---

## 2. Check OneDrive Status

- Click the **OneDrive cloud icon** in the system tray.
- Interpret the icons:
  - ✅ Green check mark: Files are synced.
  - 🔄 Blue icon: Sync is in progress.
  - ❌ Red icon: There is a sync error.

> Use “View sync problems” or go to **Help & Settings > View online** for more info.

---

## 3. Review File Path & Length Limits

- Ensure **no file path exceeds 400 characters**.
- Remove special characters like: `: * ? " < > |`.

---

## 4. Check for Duplicate or Conflict Files

- Look for filenames like `filename (computername).ext`.
- These are **conflict copies**. Resolve manually, then delete the duplicate.

---

## 5. Confirm You’re Signed Into the Correct Account

- Right-click the OneDrive icon > **Help & Settings > Settings > Account** tab.
- Ensure your **Work or School account** tied to SharePoint is listed and active.

---

## 6. Check Storage Quotas

- In SharePoint:
  - Click the **gear icon > Site Information > View all site settings > Storage Metrics**.
- In OneDrive:
  - Go to [onedrive.live.com](https://onedrive.live.com) and check available storage.

---

## 7. Restart OneDrive

- Right-click the OneDrive icon > **Help & Settings > Close OneDrive**.
- Reopen it from the Start Menu.

---

## 8. Unlink and Re-Sync the Folder (If Needed)

1. Go to **OneDrive > Settings > Account**.
2. Click **“Stop sync”** next to the affected SharePoint folder.
3. Revisit the SharePoint library in your browser and click **“Sync”** again.

---

Let IT know if these steps don’t resolve the issue. Additional scripts and logs may be needed.


Troubleshooting OneDrive Sync

Purpose: 

This document provides standardized procedures for IT Helpdesk personnel to diagnose and resolve OneDrive sync issues on Windows devices. It is essential to follow these instructions precisely. Failure to do so may result in the synchronization of incorrect or outdated data into SharePoint document libraries. 

 Step 1: Preliminary Checks 

1. Verify Network Connectivity Ensure the device is connected to a stable internet connection. 
    
2. Check OneDrive Status 
    
    - Locate the OneDrive icon in the system tray. 
        
    - Hover over the icon to view sync status. 
        
    - If syncing is paused or an error is displayed, attempt to resume syncing or note the error message. 
        
3. Confirm Software Updates 
    
    - Ensure Windows is fully updated. 
        
    - Confirm that the latest version of OneDrive is installed. 
        

Step 2: Reset OneDrive 

If the issue persists after basic checks, reset the OneDrive client. This process reinitializes the sync engine without deleting local files. 

- Important: Improperly resetting OneDrive can result in the synchronization of incorrect data to SharePoint libraries. Follow the official Microsoft instructions exactly. 
    
- Reset Instructions: [https://support.microsoft.com/en-us/office/reset-onedrive-34701e00-bf7b-42db-b960-84905399050c](https://support.microsoft.com/en-us/office/reset-onedrive-34701e00-bf7b-42db-b960-84905399050c) 
    

Step 3: Reinstall OneDrive (if reset is unsuccessful) 

1. Uninstall OneDrive 
    
2. Reinstall OneDrive 
    

 Step 4: Post-Resolution Validation 

- Confirm that OneDrive is syncing without errors. 
    
- Verify that all expected files and folders are present. 
    
- Ensure that SharePoint libraries are syncing correctly and no data discrepancies are observed in the user's OneDrive files or synced libraries. 
    

 Escalation: 

If the issue remains unresolved after completing all steps, escalate the case to "Chiappetta, Paul" <[paul.chiappetta@archkey.com](mailto:paul.chiappetta@archkey.com)> and "Alexander Silva" <[asilva@adaptivedge.com](mailto:asilva@adaptivedge.com)>.