# Excel Freezing Issue - User Specific

When an Excel workbook freezes for one user but works fine for others, the problem is usually environment-specific.  

---

## Common Causes and Fixes

### 1. Excel Add-ins (COM or Excel Add-ins)
- Problematic add-ins may interfere with cell entry or recalculation.
- **Fix:**  
  - Open Excel in Safe Mode: Run `excel /safe`  
  - If freezing stops, disable add-ins:  
    - Go to **File > Options > Add-ins**  
    - Manage **COM Add-ins** → uncheck all  
    - Restart Excel, re-enable one by one to find culprit.

---

### 2. Corrupted Excel User Profile / Cache
- Excel profile or cached settings can become corrupted.
- **Fix:**  
  - Close Excel  
  - Delete contents of `%appdata%\Microsoft\Excel` and `%temp%`  
  - Reopen and test file.

---

### 3. Hardware Acceleration or Display Drivers
- GPU drivers may cause Excel to hang.
- **Fix:**  
  - Go to **File > Options > Advanced > Display**  
  - Enable **Disable hardware graphics acceleration**  
  - Restart Excel.

---

### 4. Excel/Office Installation Issues
- Local install may be damaged or outdated.
- **Fix:**  
  - Go to **Control Panel > Programs > Office > Change > Quick Repair**  
  - If still failing → run **Online Repair**  
  - Ensure updates: **File > Account > Update Options**.

---

### 5. Security / Antivirus Software
- AV may scan Excel’s temp files and cause lockups.
- **Fix:**  
  - Temporarily disable AV and test Excel  
  - If confirmed, whitelist Excel and its temp directories.

---

## Recommended Troubleshooting Order
1. Open in **Safe Mode** → test.  
2. Toggle **Disable hardware acceleration** → test.  
3. Clear **Excel cache** → test.  
4. Run **Quick Repair** on Office.  
5. If still stuck → check AV exclusions.  

---

## External References
- [Microsoft: Excel not responding, hangs, freezes](https://support.microsoft.com/en-us/office/excel-not-responding-hangs-freezes-or-stops-working-37e7d3c9-9e84-40bf-a805-4ca6853a1ff4)
- [Microsoft: Repair an Office application](https://support.microsoft.com/en-us/office/repair-an-office-application-7821d4b6-7c1d-4205-aa0e-a6b40c5bb88b)

---

## Tags
#Excel #Troubleshooting #Office #KB
