# Bluebeam Revu Settings Storage

This note documents where Bluebeam Revu stores its configuration, preferences, and resources.

---

## 📂 File System Locations

### 1. User-Specific Settings
```
%AppData%\Bluebeam Software\Bluebeam Revu\
```
Expands to:
```
C:\Users\<username>\AppData\Roaming\Bluebeam Software\Bluebeam Revu\<version>\
```
- Stores user preferences, profiles, tool sets, stamps, and custom settings.

### 2. Application Data (Shared Across Users)
```
%ProgramData%\Bluebeam Software\Bluebeam Revu\
```
Expands to:
```
C:\ProgramData\Bluebeam Software\Bluebeam Revu\<version>\
```
- Contains shared resources, such as default tool sets and stamps available to all users.

### 3. Temporary & Logs
```
%LocalAppData%\Bluebeam\Revu\
```
Expands to:
```
C:\Users\<username>\AppData\Local\Bluebeam\Revu\
```
- Used for temporary data, logs, and cache files.

---

## 🗝️ Registry Keys

### 1. User Settings
```
HKEY_CURRENT_USER\Software\Bluebeam Software\Bluebeam Revu\
```
- Controls user-specific settings and preferences.

### 2. Machine-Wide Install Settings
```
HKEY_LOCAL_MACHINE\SOFTWARE\Bluebeam Software\Bluebeam Revu\
```
- Stores license information, installation details, and machine-wide configuration.

---

## 📦 Summary of What’s Stored Where

- **Profiles, Tool Sets, Stamps** → `%AppData%` path  
- **Licensing Info / Install Data** → `HKLM` registry path  
- **User Preferences (UI, recent files, settings)** → `HKCU` registry path  
- **Logs & Cache** → `%LocalAppData%` path  

---

## 🔧 Backup / Migration

The recommended way to backup or migrate Bluebeam settings is to use **Revu Administrator → Backup Settings**, which automatically collects all necessary files and registry values.

---

### Tags
#bluebeam #settings #registry #backup #kb  
