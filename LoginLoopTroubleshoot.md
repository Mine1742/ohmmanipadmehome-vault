[[Windows Hub]]

# Windows Login Loop Troubleshooting Guide

Below is a systematic guide to troubleshoot and recover from a Windows login loop (progress circle spins and returns to the password screen without error).

---

## 1. Force a Full Power-Off, Then Boot into WinRE

Because the laptop didn’t properly sleep and got hot, the file system or user profile may be corrupted. Use Windows Recovery Environment (WinRE):

1. **Force Power Off**  
   - Press and hold the power button for 8–10 seconds until the machine fully shuts off (screen dark, fans stop).  
2. **Disconnect Peripherals**  
   - Unplug USB drives, external monitors, etc., then connect AC power.  
3. **Boot into WinRE**  
   - Power on and immediately tap **F11** (or **F8** on some models).  
   - If F11/F8 doesn’t work, power on, as soon as you see Windows or manufacturer logo, hold **Shift** and select **Restart** (from Power icon on login screen).  
4. On the **Choose an option** screen, navigate:  
   ```
   Troubleshoot → Advanced options → Startup Settings → Restart
   ```
5. After reboot, press **4** (or **F4**) for **Safe Mode** or **5/F5** for **Safe Mode with Networking**.

---

## 2. Try Logging in Under Safe Mode

1. Once booted into Safe Mode (you’ll see a simplified desktop and “Safe Mode” watermark), enter your usual login credentials.  
   - **If successful**: the issue is likely a driver/service or corrupted system file that Safe Mode bypasses.  
   - **If still bounced**: proceed to Section 4 (System Restore or Startup Repair).

---

## 3. If Safe Mode Login Succeeds, Purge or Repair the Likely Culprit

### A. Run System File Checker (SFC) and DISM

1. Open **Command Prompt (Admin)**:  
   - Press **Windows key + X** → select **Windows Terminal (Admin)** or **Command Prompt (Admin)**.  
2. Run the following commands one at a time (waiting for each to finish):

   ```powershell
   sfc /scannow
   DISM /Online /Cleanup-Image /RestoreHealth
   ```
   - **sfc /scannow** checks for corrupted/missing Windows system files and repairs them.  
   - **DISM /Online /Cleanup-Image /RestoreHealth** repairs the component store if deeper issues exist.

3. After completion, reboot normally (no Safe Mode) and test login.

### B. Run Check Disk on C:

1. In the same elevated prompt, type:
   ```powershell
   chkdsk C: /f /r
   ```
   - You’ll be prompted: “Schedule this volume to be checked at next restart? (Y/N).”  
   - Type **Y** and press **Enter**.  
   - **Reboot**: Windows will run CHKDSK before loading.  
2. After CHKDSK finishes, test login again.

### C. Remove Problematic Startup Items or Drivers

1. In Safe Mode, press **Windows + R**, type `msconfig`, and press **Enter**.  
2. Go to **Services** tab → check **Hide all Microsoft services** → click **Disable all**.  
3. Go to **Startup** tab → click **Open Task Manager** → disable any non-Microsoft/unknown entries.  
4. Reboot normally and test login.  
   - If login now works, re‐enable one group of services/startup items at a time to isolate the culprit.

---

## 4. If You Cannot Log in Under Safe Mode

Use WinRE tools:

### A. System Restore

1. In WinRE (refer to steps 1–3 in Section 1 to access WinRE):  
   ```
   Troubleshoot → Advanced options → System Restore
   ```
2. Select a restore point dated **before** May 30 (when login worked).  
3. Let the process complete and reboot.  
4. Test normal login.

> **Note**: System Restore works only if enabled and restore points exist.

### B. Startup Repair

1. In WinRE:  
   ```
   Troubleshoot → Advanced options → Startup Repair
   ```
2. Choose your Windows account, enter password if prompted, and let Windows attempt repairs.  
3. Reboot and test login.

### C. Enable Built-In Administrator or Create a New Local Admin (Last Resort)

1. In WinRE, navigate to:  
   ```
   Troubleshoot → Advanced options → Command Prompt
   ```
2. Enable the hidden Administrator account and create a new user:

   ```batch
   net user Administrator /active:yes
   net user NewUser Password123! /add
   net localgroup Administrators NewUser /add
   ```
   - Replace **NewUser** and **Password123!** with your desired username/password (ensure it meets complexity).  
3. Reboot normally. At login, select **Administrator** (no password unless set) or **NewUser**.  
4. If login succeeds, copy files from your old profile (`C:\Users\OldProfileName`) to an external drive or the new user’s Documents folder.

---

## 5. Once You Regain Access

1. **Disable Fast Startup** (prevents future sleep/wake issues):  
   - Control Panel → Power Options → “Choose what the power buttons do” → “Change settings that are currently unavailable” → uncheck **Turn on fast startup** → **Save changes**.  
2. **Update Drivers**:  
   - Open **Device Manager** → expand categories, look for devices with yellow warning icons → right-click → **Update driver**.  
   - Focus on **Display adapters**, **Network adapters**, and any “Unknown device.”  
3. **Check Event Viewer** for clues:  
   - Windows Logs → System → look for errors around boot/login time.  
4. **Run Windows Update** to install the latest patches and fixes.

---

### Summary Checklist

1. **WinRE → Safe Mode** → attempt login.  
2. If Safe Mode works:
   - Run **sfc /scannow** and **DISM RestoreHealth**.  
   - Run **chkdsk C: /f /r** on reboot.  
   - Disable suspicious startup apps/services.  
3. If Safe Mode still fails:
   - Perform **System Restore** (to a point before 5/30).  
   - Run **Startup Repair** from WinRE.  
   - As last resort, enable Default Administrator or create a new local admin via WinRE command prompt.  
4. After regaining access:  
   - Disable **Fast Startup**, update drivers, and apply Windows Updates.

Following these steps should resolve the login loop and allow you to recover your account. If you face issues at any stage, note the specific errors and revisit the corresponding section.
