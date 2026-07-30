
================================================================================
TEAMS AUDIO/MOUSE CUTOUT FIX - TROUBLESHOOTING GUIDE
================================================================================

--------------------------------------------------------------------------------
BLUETOOTH MOUSE FIXES
--------------------------------------------------------------------------------

1. UPDATE BLUETOOTH DRIVERS
   - Open Device Manager (Win + X → Device Manager)
   - Expand "Bluetooth"
   - Right-click your Bluetooth adapter → Update driver
   - Choose "Search automatically for drivers"
   - Restart PC

2. DISABLE BLUETOOTH POWER MANAGEMENT
   - Open Device Manager
   - Expand "Bluetooth"
   - Right-click your Bluetooth **adapter** → Properties
   - Go to "Power Management" tab
   - Uncheck "Allow the computer to turn off this device to save power"
   - Click OK

3. ENABLE BLUETOOTH/WIFI COEXISTENCE
   - Open Device Manager
   - Expand "Network adapters"
   - Right-click your WiFi adapter → Properties
   - Go to "Advanced" tab
   - Look for "Bluetooth Collaboration" or "Bluetooth Coexistence"
   - Set to "Enabled"
   - **In that same Advanced tab, look for and adjust:**

1. **Preferred Band** → Set to **"5GHz"** or **"Prefer 5GHz"**
    - This keeps WiFi off 2.4GHz, reducing Bluetooth interference
2. **Dynamic MIMO Power Save** → Set to **"Disabled"**
    - Prevents WiFi power fluctuations
3. **Idle Power Down Restriction** → Set to **"Enabled"** (if available)
    - Stops the adapter from going to sleep
4. Scroll down and look for anything with **"Power"** or **"Roaming"** → set power-related ones to max performance / disabled

**Then check the Power Management tab:**

- Click on the **Power Management** tab (next to Resources)
- Uncheck "Allow the computer to turn off this device to save power"

**Also try this in Power Options:**

```
Control Panel → Power Options → Change plan settings → 
Change advanced power settings → 
Wireless Adapter Settings → Power Saving Mode → Maximum Performance
```

Setting Preferred Band to 5GHz is probably the most impactful fix for your Bluetooth mouse issue—it directly addresses the WiFi/Bluetooth 2.4GHz conflict.



4. SWITCH TO 5GHZ WIFI
   - Open your router settings or WiFi connection
   - Connect to your 5GHz network instead of 2.4GHz
   - This eliminates interference with Bluetooth (which uses 2.4GHz)

--------------------------------------------------------------------------------
USB SPEAKERS FIXES
--------------------------------------------------------------------------------

1. DISABLE USB SELECTIVE SUSPEND
   - Open Control Panel → Power Options
   - Click "Change plan settings" next to your active plan
   - Click "Change advanced power settings"
   - Expand "USB settings"
   - Expand "USB selective suspend setting"
   - Set to "Disabled"
   - Click OK
#### for the speaker issue the advanced power options does not have a usb setting
That happens sometimes—Windows hides certain options. Let's unhide them or use alternatives:
**Option 1: Unhide USB settings via Registry**
Open PowerShell as Admin and run:
powershell
```powershell
# Unhide USB selective suspend setting
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\2a737441-1930-4402-8d77-b2bebba308a3\48e6b7a6-50f5-4782-a5d4-53bb8f07e226" /v Attributes /t REG_DWORD /d 2 /f

# Unhide Wireless Adapter settings
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\19cbb8fa-5279-450e-9fac-8a3d5fedd0c1\12bbebe6-58d6-4636-95bb-3217ef867c1a" /v Attributes /t REG_DWORD /d 2 /f
```

Then close and reopen Power Options—USB settings should appear.
**Option 2: Disable USB suspend via PowerShell directly**
powershell

````powershell
powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /SETDCVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /SETACTIVE SCHEME_CURRENT
```

**Option 3: Device Manager method (still valid)**
```
Device Manager → Universal Serial Bus controllers → 
Right-click each USB Root Hub → Properties → Power Management → 
Uncheck "Allow the computer to turn off this device"
````

Try Option 1 first, then reopen Power Options and check if USB settings and Wireless Adapter Settings now appear.

1. DISABLE USB POWER MANAGEMENT
   - Open Device Manager
   - Expand "Universal Serial Bus controllers"
   - Right-click each "USB Root Hub" → Properties
   - Go to "Power Management" tab
   - Uncheck "Allow the computer to turn off this device to save power"
   - Click OK
   - Repeat for all USB Root Hubs

3. SET SPEAKERS AS DEFAULT COMMUNICATION DEVICE
   - Right-click the speaker icon in system tray
   - Click "Sounds" (or "Sound settings" → "More sound settings")
   - Go to "Playback" tab
   - Right-click your USB speakers
   - Select "Set as Default Device"
   - Right-click again → "Set as Default Communication Device"
   - Click OK

4. DISABLE AUDIO ENHANCEMENTS
   - Right-click speaker icon → Sounds
   - Go to "Playback" tab
   - Right-click your USB speakers → Properties
   - Go to "Advanced" tab
   - Uncheck "Enable audio enhancements"
   - Click OK

--------------------------------------------------------------------------------
TEAMS SETTINGS
--------------------------------------------------------------------------------

1. LOCK IN AUDIO DEVICES
   - Open Teams → Settings (gear icon) → Devices
   - Set Speaker to your specific USB speakers (not "Auto")
   - Set Microphone to your specific device (not "Auto")
   - Turn OFF "Automatically adjust mic sensitivity"

--------------------------------------------------------------------------------
AFTER ALL CHANGES: RESTART YOUR PC
--------------------------------------------------------------------------------