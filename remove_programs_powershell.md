[[Powershell Hub]]
Shell Script to Remove Installed Programs

## 🧾 Overview
Use PowerShell to uninstall traditional Win32 applications or Microsoft Store (UWP) apps. This guide includes sample scripts and notes for help desk or IT support use.

---

## ✅ 1. Remove Traditional Win32 Applications

```powershell
# Run PowerShell as Administrator
$programName = "Program Name Here"

$uninstallKey = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall"
$uninstallKey64 = "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"

$keys = Get-ChildItem $uninstallKey, $uninstallKey64

foreach ($key in $keys) {
    $displayName = (Get-ItemProperty $key.PSPath).DisplayName
    $uninstallString = (Get-ItemProperty $key.PSPath).UninstallString
    if ($displayName -like "*$programName*") {
        Write-Output "Uninstalling: $displayName"
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c $uninstallString" -Wait
    }
}
```

> 🔁 Replace `"Program Name Here"` with all or part of the program's name.

---

## ✅ 2. Remove Microsoft Store / UWP Apps

```powershell
# Run PowerShell as Administrator
Get-AppxPackage *partOfAppName* | Remove-AppxPackage
```

> Example:
```powershell
Get-AppxPackage *xbox* | Remove-AppxPackage
```

---

## ⚠️ Notes

- Not all uninstallers support **silent mode** — prompts may appear.
- Protected or system-critical apps may not be removable via PowerShell.
- Always test scripts in a **non-production environment** first.

---

## 🧩 For Enterprise Deployments

- Consider **Intune**, **SCCM**, or **PDQ Deploy** for remote or mass removal.
- Monitor uninstall logs for compliance and rollback.

---

## 🏷 Tags
#powershell #helpdesk #uninstall #windows #scripts #automation
