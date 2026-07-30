# Taskbar Not Extending to All Monitors in Multi-Screen Setup

## Issue
In a multi-monitor setup, the Windows taskbar does not extend across all displays.  
After closing and reopening the laptop lid, the taskbar correctly appears on all monitors.

---

## Root Cause
- Windows relies on a **display topology refresh** when initializing multiple monitors.  
- Closing/reopening the laptop lid forces the GPU and Windows Explorer to renegotiate displays.  
- Initial glitches often occur due to **driver issues** or **Windows Explorer not fully applying multi-display settings**.

---

## Resolution Steps

1. **Confirm Taskbar Setting**
   - Go to: `Settings → Personalization → Taskbar → Multiple displays`.
   - Ensure **Show taskbar on all displays** is enabled.

2. **Restart Windows Explorer (instead of closing lid)**
   - Press **Ctrl + Shift + Right-click** on the taskbar → select *Exit Explorer*.
   - Open **Task Manager (Ctrl+Shift+Esc)** → *File* → *Run new task* → type `explorer.exe`.

3. **Update Drivers/Firmware**
   - Update GPU drivers (Intel / NVIDIA / AMD).
   - Update laptop BIOS and any docking station or USB-C/Thunderbolt firmware.

4. **Check Dock/Adapter**
   - If using a docking station or adapter, ensure the latest firmware is installed.

5. **Registry Reset (Last Resort)**
   - Open **Registry Editor**.
   - Navigate to:  
     `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer`
   - Delete the key: `StuckRects3`.
   - Reboot the system to rebuild taskbar configuration.

---

## Workaround
Closing and reopening the laptop lid forces Windows to reinitialize the display layout and reapply the multi-monitor taskbar setting.

---

## Quick PowerShell Fix
To restart Explorer without menus:

```powershell
Stop-Process -Name explorer -Force; Start-Process explorer
```

---

## Tags
#Windows #MultiMonitor #Taskbar #Troubleshooting #Display
