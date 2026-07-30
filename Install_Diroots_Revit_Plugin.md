---
title: "Installing Diroots Plugin for Revit"
created: 2025-05-06
tags: [revit, diroots, plugins, installation, IT-setup]
aliases: [Add Diroots Plugin to Revit, Revit Plugin Setup]
---
[[Revit]]

# 🛠 How to Update Revit Accounts with Diroots Plugin

## 🔍 Prerequisites
- Autodesk Revit must be installed (2021 or later recommended)
- Internet connection
- Admin privileges (local or domain)

## 🧩 Step-by-Step Instructions

### 1. Download the Plugin
- Visit the official Diroots website: [https://diroots.com](https://diroots.com)
- Navigate to the **Products** tab and select the desired plugin (e.g., SheetLink, TableGen, etc.)
- Click **Download** for the version compatible with your Revit version.

### 2. Install the Plugin
- Run the installer as an administrator.
- Follow the prompts to complete installation.
- By default, it installs to:
  ```
  C:\ProgramData\Autodesk\Revit\Addins\<Year>\
  ```

### 3. Verify Installation
- Open Revit.
- Navigate to the **Add-Ins** tab.
- You should see a new section labeled **Diroots**.
- Launch a plugin (e.g., SheetLink) to verify it loads properly.

### 4. Repeat for All User Profiles (if multi-user machine)
If the machine has multiple local user profiles:
- Ensure the installer is run for **each user** or install system-wide using a script with administrative rights.

## 🧪 Troubleshooting
- **Plugin not showing?**
  - Check Revit version compatibility.
  - Reinstall plugin and restart Revit.
- **Missing .addin file?**
  - Copy the `.addin` file to the corresponding folder:
    ```
    C:\ProgramData\Autodesk\Revit\Addins\<Year>\
    ```

## 📦 Optional: Automate with PowerShell (for IT Admins)
```powershell
Start-Process -FilePath "D:\Installers\DirootsPlugin.exe" -ArgumentList "/S" -Verb RunAs
```


If DiRoots software is unable to connect to its licensing server, it could be due to a few common issues related to network connectivity, software components, or licensing server configuration. Based on general troubleshooting steps for similar software and licensing errors, you can try the following:

1. Network/Firewall issues

- Ensure the client machine (where DiRoots is installed) has a stable network connection.
- Temporarily disable any firewall or antivirus software to check if they are blocking the connection.
- If using a network license, ensure the necessary ports are open on the server's firewall, particularly TCP 2080 and 27000-27009 for Autodesk Network License Manager related connections, as this is often used with Autodesk products that might interact with DiRoots. 

2. DiRoots or Autodesk component updates and reinstallation

- Ensure the Autodesk Desktop Licensing Service (ADLS) is running and up-to-date. If not, consider uninstalling and reinstalling it as administrator.
- For versions 2020-2023, check if the Autodesk Single Sign-On Component (AdSSO) is up-to-date and consider reinstalling it.
- For versions 2024 and newer, check if the Autodesk Identity Manager is up-to-date and consider reinstalling it. 

3. DiRoots license and product activation

- Confirm that a valid license has been assigned to the user.
- If the issue persists, try resetting the product license and reactivating it. 

4. Addressing specific error messages (if applicable)

- If you see "Licensing Error. A licensing error occurred..." check the licensing server status and consider uninstalling/reinstalling Autodesk Desktop Licensing Service and the Autodesk Identity Manager or Single Sign-On Component.
- If you encounter "Trial expired" or "Your trial has ended", verify correct license and product assignments and consider resetting and reactivating the license.
- For "Cannot connect to License Server", check for network problems or interference from security software or firewalls. 

5. Contacting DiRoots support

- If the issue remains unresolved after trying the previous troubleshooting steps, consider contacting DiRoots technical support for assistance. They can be reached via email at info@diroots.com. 

Remember to restart your computer after making any changes to ensure they are properly applied.