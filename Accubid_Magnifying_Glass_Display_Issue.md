[[Accubid Hub]]
# 🛠 Accubid Display Issue: Random Magnifying Glasses

**Issue:**  
Users are seeing random magnifying glasses all over the Accubid display. The issue persists across restarts and reboots.

---

## ✅ Troubleshooting Steps

### 1. Check for Stuck Zoom or View Mode
- In Accubid, press **Esc** to cancel active tools.
- Look for toolbar buttons related to **Zoom**, **Magnify**, or **Fit to Screen**.
- Disable any active zoom tools.

---

### 2. Reset Accubid Workspace or Layout Files
Corrupted layout files can cause persistent UI artifacts.

#### Steps:
1. Close Accubid completely.
2. Navigate to your user settings folder:
   ```
   C:\Users\<YourUsername>\AppData\Roaming\Trimble\Accubid
   ```
3. Locate files like:
   - `layout.config`
   - `user.config`
   - `UI.config`
4. Rename them (e.g., `layout.config.backup`), or delete them.
5. Reopen Accubid. It will regenerate default layout files.

> ⚠️ This will reset toolbars and custom layout settings.

---

### 3. Turn Off Windows Magnifier
To rule out system-wide magnification:

- Press `Windows + Esc` to toggle Magnifier off.
- Or go to **Settings > Accessibility > Magnifier** and disable it.

---

### 4. Update or Reinstall Graphics Drivers
1. Open **Device Manager**.
2. Expand **Display Adapters**.
3. Right-click your GPU and select **Update driver**.
4. Optionally, reinstall using the latest version from the GPU vendor (Intel, AMD, NVIDIA).

---

### 5. Adjust Compatibility Mode
1. Right-click the Accubid shortcut.
2. Go to **Properties > Compatibility** tab.
3. Check **"Disable display scaling on high DPI settings"**.
4. Apply and restart Accubid.

---

### 6. Reinstall Accubid (If All Else Fails)
If the issue persists:
- Fully uninstall Accubid.
- Download a clean installer or contact Trimble support for assistance.
- Reinstall and test.

---

## 🧠 Tip:
Always back up any custom layouts or templates before deleting user config files.

---

Let your IT support team know if the issue continues after trying all steps.
