
## Problem

Needed to restart the directprint.io application (dpio.exe) but `Restart-Service` failed:

powershell

```powershell
Restart-Service -Name 'dpio.exe' -Force
```

**Error:** `Cannot find any service with service name 'dpio.exe'`

---

## Root Cause

**dpio.exe is NOT a Windows Service** — it's a regular application built on NW.js (Node.js + Chromium framework for desktop apps).

- Location: `C:\Program Files (x86)\directprint.io\dpio.exe`
- Type: Application (.exe), not a service
- Framework: NW.js v0.60.0, Node v17.3.0, Chromium 97.0.4692.71

---

## Failed Attempts

### 1. Using Restart-Service

powershell

```powershell
Restart-Service -Name 'dpio.exe' -Force
# Error: NoServiceFoundForGivenName
```

### 2. Launching dpio.exe directly

powershell

```powershell
Start-Process 'C:\Program Files (x86)\directprint.io\dpio.exe'
```

**Result:** Opens NW.js splash screen instead of the actual application — missing proper initialization.

### 3. Adding WorkingDirectory parameter

powershell

```powershell
Start-Process 'C:\Program Files (x86)\directprint.io\dpio.exe' -WorkingDirectory 'C:\Program Files (x86)\directprint.io'
```

**Result:** Still shows NW.js splash screen.

---

## Solution

### Discovery: Check the Start Menu Shortcut

Found shortcuts at:

- `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\directprint.io.lnk`
- `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\directprint.io.lnk`

Inspected shortcut properties:

powershell

```powershell
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\directprint.io.lnk")
$shortcut | Select-Object TargetPath, Arguments, WorkingDirectory
```

**Key Finding:** The shortcut uses **`dpio-launcher.exe`**, not `dpio.exe` directly!

### Working Command

powershell

```powershell
Stop-Process -Name 'dpio' -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Start-Process 'C:\Program Files (x86)\directprint.io\dpio-launcher.exe' -WorkingDirectory 'C:\Program Files (x86)\directprint.io'
```

---

## Scheduled Task Configuration

### Action Tab

|Field|Value|
|---|---|
|Action|Start a program|
|Program/script|`powershell.exe`|
|Add arguments|See below|
|Start in|`C:\Program Files (x86)\directprint.io`|

### Arguments String

```
-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -Command "Stop-Process -Name 'dpio' -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2; Start-Process 'C:\Program Files (x86)\directprint.io\dpio-launcher.exe' -WorkingDirectory 'C:\Program Files (x86)\directprint.io'"
```

### Parameter Explanation

|Parameter|Purpose|
|---|---|
|`-NoProfile`|Faster startup, skips loading PowerShell profile|
|`-WindowStyle Hidden`|Runs silently without visible window|
|`-ExecutionPolicy Bypass`|Ensures command runs without policy blocks|
|`-ErrorAction SilentlyContinue`|Won't error if dpio isn't already running|
|`Start-Sleep -Seconds 2`|Brief pause for clean shutdown before restart|
### Triggers

The task needs two triggers to restart DPIO both at login and after screen unlock:

|Trigger|Setting|
|---|---|
|**At log on**|Specific user: DENPRO\Albert.Smith|
|**On workstation unlock**|Specific user: DENPRO\Albert.Smith|
### Recommended Task Settings

**Conditions tab:**

- Uncheck "Start the task only if the computer is on AC power" (if laptops involved)

**Settings tab:**

- Check "Run task as soon as possible after a scheduled start is missed"
- Set "If the task is already running" to "Do not start a new instance"

---

## Key Lessons Learned

1. **Check application type first** — Not everything is a Windows Service; use Task Manager or file properties to verify
2. **NW.js apps often need launchers** — Direct execution may show framework splash instead of the app
3. **Inspect existing shortcuts** — They contain the correct launch parameters the vendor intended
4. **PowerShell parameters differ by context** — `-NoProfile`, `-WindowStyle` are for calling PowerShell externally, not from within PowerShell

---

## Related Commands

### Find services matching a pattern

powershell

```powershell
Get-Service | Where-Object { $_.DisplayName -match 'print|coreza|direct' }
```

### Inspect shortcut properties

powershell

```powershell
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("path\to\shortcut.lnk")
$shortcut | Select-Object TargetPath, Arguments, WorkingDirectory
```

### Find shortcuts by name

powershell

```powershell
Get-ChildItem "C:\ProgramData\Microsoft\Windows\Start Menu" -Recurse -Filter "*appname*" | Select-Object FullName
Get-ChildItem "$env:APPDATA\Microsoft\Windows\Start Menu" -Recurse -Filter "*appname*" | Select-Object FullName
```

---

## Tags

#troubleshooting #windows #powershell #scheduled-tasks #directprint #nwjs #msp