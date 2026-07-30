[[Windows Hub]]
# 🚀 How to Change Startup Apps in Windows 11/10

Control which applications launch when your computer starts to improve boot speed and reduce clutter.

---

## 🟦 Method 1: Use Task Manager (Quickest)

1. **Right-click** the taskbar and select **Task Manager**
2. Click **"More details"** if the simplified view appears
3. Go to the **Startup apps** tab
4. **Right-click** any app and choose:
   - **Disable** – prevents the app from launching at startup
   - **Enable** – allows the app to launch automatically

---

## 🟩 Method 2: Use Windows Settings

1. Press **`Windows + I`** to open **Settings**
2. Navigate to **Apps > Startup**
3. Toggle the switch **on/off** for each app you want to control

---

## 🟨 Method 3: Use File Explorer (Advanced)

1. Press **`Windows + R`**, type:
   ```shell
   shell:startup
   ```
   and hit **Enter**

2. This opens:
   ```
   C:\Users\<YourName>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```

3. Add or remove shortcuts here to manage which programs launch on boot

---

## 🧠 Tips

- **Disabling an app here does not uninstall it**
- Use **Startup Impact** info in Task Manager to prioritize
- Avoid disabling security or driver-related programs

---
