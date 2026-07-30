# Outlook Opens in Small Window or Disappears When Minimized – Window State Repair

## Symptoms
- Outlook opens only in a small window instead of full screen.
- When minimized, the Outlook window and icon disappear from the taskbar.
- After several seconds or minutes, Outlook reappears on the taskbar.

These symptoms typically indicate corruption in Outlook's window state cache or issues with GPU hardware acceleration.

---

## Root Causes
1. **Window position cache corruption** – Outlook stores the last window size and screen coordinates in the registry; these values can become invalid.
2. **Hardware acceleration glitches** – GPU rendering delays can make Outlook appear to close when minimized.
3. **Multi-monitor issues** – If a monitor configuration changed, Outlook may be opening off-screen.
4. **Taskbar refresh lag** – Windows Explorer may delay refreshing Outlook’s taskbar entry.

---

## Resolution Steps

### 1. Reset Outlook Navigation Pane and Window State
Close Outlook completely and open **Run** (`Win + R`):
```
outlook /resetnavpane
```
This resets Outlook’s navigation and window layout to default.

If the issue persists, open:
```
outlook /safe
```
If it opens correctly in Safe Mode, disable add-ins:
- Go to **File → Options → Add-ins**.
- At the bottom, choose **COM Add-ins → Go**.
- Uncheck all add-ins and restart Outlook.

---

### 2. Delete Window Geometry from Registry
1. Close Outlook.
2. Press `Win + R` → type `regedit` → press Enter.
3. Navigate to:
   ```
   HKEY_CURRENT_USER\Software\Microsoft\Office\16.0\Outlook\Office Explorer
   ```
   *(Replace `16.0` with your version, e.g., 15.0 for Outlook 2013.)*
4. Delete these keys if present:
   - `Frame`
   - `FrameLeft`
   - `FrameTop`
   - `FrameWidth`
   - `FrameHeight`
5. Restart Outlook. It will rebuild default window sizing.

---

### 3. Disable Hardware Graphics Acceleration
In Outlook:
1. Go to **File → Options → Advanced**.
2. Scroll to the **Display** section.
3. Check the box: ✅ **Disable hardware graphics acceleration**.
4. Restart Outlook.

---

### 4. Refresh Windows Explorer and Taskbar
If Outlook still hides when minimized:
1. Open **Task Manager** (`Ctrl + Shift + Esc`).
2. Find **Windows Explorer**.
3. Right-click → **Restart**.
4. Relaunch Outlook.

---

### 5. Verify Outlook Process Persistence
If Outlook disappears after minimizing:
1. Open **Task Manager**.
2. Look for `Outlook.exe` under **Processes**.
   - If it remains, the icon may just be hidden in the tray.
   - If it disappears, check **Event Viewer → Application Logs** for Outlook crashes.

---

### 6. Reset Outlook Profile (if issue persists)
1. Open **Control Panel → Mail → Show Profiles**.
2. Click **Add**, create a new profile.
3. Choose **Prompt for a profile to be used**.
4. Start Outlook with the new profile.

---

## Verification
- Outlook opens full screen or in a consistent window size.
- The taskbar icon remains visible when minimized.
- Outlook restores immediately from the taskbar.

---

### References
- [Microsoft Support: Outlook command-line switches](https://learn.microsoft.com/en-us/outlook/troubleshoot/user-interface/command-line-switches)
- [Microsoft 365: Disable hardware graphics acceleration](https://learn.microsoft.com/en-us/office/troubleshoot/excel/disable-hardware-graphics-acceleration)

---

**Tags:** #outlook #windows #troubleshooting #registry #display #microsoft365