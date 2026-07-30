[[O365]] [[Windows Hub]]
# 🛠️ How to Repair Microsoft 365 (Office 365) on Windows

Follow these steps to repair Microsoft 365 if you're experiencing issues like app crashes, failed updates, or missing features.

---

## ✅ Method 1: Repair Microsoft 365 via Control Panel (Recommended)

1. Press `Windows + R`, type:
   ```
   appwiz.cpl
   ```
   and press **Enter** to open *Programs and Features*.

2. Locate **Microsoft 365 Apps for enterprise** (or your version of Office).

3. Right-click it and choose **Change**.

4. Choose:
   - 🔧 **Quick Repair** – Fast and doesn't require internet.
   - 🌐 **Online Repair** – More thorough and reinstalls Office. Requires internet.

5. Click **Repair** and follow the prompts.

---

## 🛠 Method 2: Repair via Command Line (Advanced)

For IT pros using deployment tools:

```cmd
setup.exe /repair user displaylevel=true
```

> ⚠️ Requires:
> - `setup.exe` from the [Office Deployment Tool](https://www.microsoft.com/en-us/download/details.aspx?id=49117)
> - A valid `configuration.xml` file

---

## 🧪 Optional: Reset Office App Data (User-Level Fix)

1. Navigate to:
   ```
   %localappdata%\Microsoft\Office\
   ```

2. Rename or delete the folder `16.0` (or your installed version).

3. Restart any Office app. Settings will regenerate.

> ⚠️ This removes custom settings, recent files, and ribbon customizations.

---

## 🔁 After Repairing

- Restart your computer.
- Open any Office app (e.g., Word, Excel).
- Sign in again with your Microsoft 365 credentials if prompted.

---

Let me know if you'd like a `.bat` file or PowerShell script to automate repair steps.
