# Bluebeam PDF Printer Could Not Be Installed – Troubleshooting Guide

## Overview
This guide provides steps to fix the **“The PDF printer could not be installed”** error in Bluebeam Revu.  
This typically happens when the Bluebeam PDF printer driver is missing, corrupted, or blocked by insufficient permissions.

---

## Symptoms
- Error popup:  
  > The PDF printer could not be installed. Please check the settings in the Bluebeam Administrator and reinstall the printer to continue.
- Print attempt triggers **Bluebeam Administrator** requesting admin credentials.
- All open windows minimize before the error appears.

---

## Root Cause
- Missing or corrupted **Bluebeam PDF printer driver**.
- Insufficient permissions to install printer drivers.
- Conflict between **Revu 20** and **Revu 21** plugins or components.
- Printer driver not properly registered in Windows.

---

## Resolution Steps

### 1. Close Bluebeam Completely
1. Exit **Bluebeam Revu**.
2. Right-click the Bluebeam icon in the **system tray** and select **Exit**.

---

### 2. Run Bluebeam Administrator as Admin
1. Locate the **Bluebeam Administrator** shortcut in your Start Menu.
2. **Right-click → Run as administrator**.
3. Enter admin credentials if prompted.

---

### 3. Reinstall the PDF Printer
1. In **Bluebeam Administrator**, go to the **Printer** tab.
2. Click **Reinstall Printer**.
3. Wait for the success confirmation.

---

### 4. Verify the Printer in Windows
1. Open **Control Panel → Devices and Printers**.
2. Look for **Bluebeam PDF**.
3. If missing:
   - Click **Add a printer** and follow the prompts.
   - OR repeat Step 3 in Bluebeam Administrator.

---

### 5. Restart the Computer
This ensures the printer driver registers properly with the OS.

---

### 6. Test Printing
1. Open **Bluebeam Revu**.
2. Print any document to **Bluebeam PDF**.
3. Confirm the print process works without admin prompts.

---

## If the Issue Persists

### Option A – Repair Bluebeam Installation
1. Go to **Control Panel → Programs and Features**.
2. Find **Bluebeam Revu**.
3. Right-click → **Change** → **Repair**.
4. Restart after completion.

---

### Option B – Remove Version Conflicts
If both **Revu 20** and **Revu 21** plugins are present:
1. Uninstall **all** versions of Bluebeam Revu.
2. Restart the PC.
3. Reinstall only the version you need.
4. Run Bluebeam Administrator as admin and reinstall the printer.

---

## External Resources
- [Bluebeam Official PDF Printer Troubleshooting](https://support.bluebeam.com/articles/reinstall-bluebeam-pdf-printer/)
- [Bluebeam Administrator Overview](https://support.bluebeam.com/articles/bluebeam-administrator-overview/)


### For when the print to pdf will not save:

Step 1 – Check Bluebeam Printer Settings
1. Close Revit
2. Open the Start menu and type "Bluebeam Administrator" — run it as Administrator
3. Go to the Printer tab
4. Make sure "Prompt for File Name" is checked
5. Click Apply

Step 2 – Clear Stale Print Jobs
1. Still on the Printer tab in Bluebeam Administrator
2. Click "Clear Print Jobs"
3. If any old Save As dialogs pop up, cancel them

Step 3 – Restart the Windows Print Spooler
1. Open Command Prompt as Administrator
2. Run the following commands one at a time:
   net stop spooler
   net start spooler

Step 4 – Reinstall the Bluebeam PDF Printer
1. In Bluebeam Administrator > Printer tab
2. Click to uninstall the printer
3. Click "Reinstall Printer"
4. In the Port Monitor section (lower right), click Restart
5. Confirm the Status shows "Responding"
6. Click Apply and OK

Step 5 – Test
1. Open Revit and try printing a single sheet to the Bluebeam PDF printer
2. The Save As dialog should now appear

Alternative: If the above steps don't resolve the issue, try using the Bluebeam tab on the Revit ribbon instead of File > Print. This uses the Bluebeam plugin directly and bypasses the Windows print spooler.

---

## Tags
#bluebeam #pdf #printer #troubleshooting #windows #adminrights
