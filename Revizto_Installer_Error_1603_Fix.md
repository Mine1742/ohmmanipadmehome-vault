#apps #software [[Software]][[Revizto]]
# 🛠 Fixing Revizto Installation Error 1603

**Error Message:**
```
Installation success or error status: 1603
```

This error typically indicates a fatal issue during installation. In this case, the logs show that a **required prerequisite is missing**.

---

## ❗ Root Cause

The installer is missing a required runtime:
```
AI_MISSING_PREREQS = .NET 8.0 Desktop Runtime (v8.0.8) - Windows x64 Installer
```

---

## ✅ Resolution Steps

### 1. Download the .NET 8.0.8 Desktop Runtime

- Visit: [https://dotnet.microsoft.com/en-us/download/dotnet/8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)
- Scroll down to **".NET Desktop Runtime 8.0.x"**
- Download and install the **x64 version** of `.NET Desktop Runtime`

### 2. (Optional) Reboot the Machine

After installing the runtime, restart your machine to ensure environment variables and registry changes take effect.

### 3. Re-run the Revizto Installer

Launch the installer again. It should now detect all prerequisites and complete successfully.

---

## 🧰 Optional: Install the Runtime Manually From Local Path

If the installer has already downloaded the runtime, you can install it manually:

```text
C:\Users\greg.rodriguez\AppData\Roaming\Revizto SA\Revizto5\prerequisites\.NET 8 Runtime\windowsdesktop-runtime-8.0.8-win-x64.exe
```

Double-click this `.exe` file to install the runtime, then restart the Revizto setup.

---

## 💡 Notes

- The error `1603` is a generic Windows Installer error but often points to missing dependencies or permission issues.
- Always check the installer logs for missing prerequisites or failed actions.

---

If issues persist, check for:
- Administrator permissions during install
- Antivirus or endpoint protection blocking the installer
