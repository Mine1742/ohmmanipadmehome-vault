# Mapping and Troubleshooting Network Drives

## Mapping a Network Drive

### Windows GUI Method
1. Open **File Explorer**.
2. Right-click **This PC** and select **Map network drive**.
3. Choose a drive letter (e.g., `Z:`).
4. Enter the folder path (e.g., `\\server\share`).
5. Check **Reconnect at sign-in** if you want it persistent.
6. Check **Connect using different credentials** if needed, then enter the correct username and password.
7. Click **Finish**.

### Command Line (CMD)
```cmd
net use Z: \\server\share /persistent:yes
```
- Replace `Z:` with your desired drive letter.
- `/persistent:yes` makes the mapping survive reboots.

### PowerShell
```powershell
New-PSDrive -Name "Z" -PSProvider FileSystem -Root "\\server\share" -Persist
```
- `-Persist` ensures the mapping remains after reboot.

---

## Troubleshooting Network Drive Issues

### 1. Verify Network Connectivity
- Run `ping servername` to confirm the server is reachable.
- Check if you can access the share via `\\server\share` in File Explorer.

### 2. Check Permissions
- Ensure the user has **NTFS** and **Share permissions** to access the folder.
- Try connecting with different credentials if access is denied.

### 3. Clear Cached Credentials
- Open **Credential Manager** → **Windows Credentials**.
- Remove old saved credentials for the file server.
- Reconnect and provide updated credentials.

### 4. Check Group Policy Mappings
- Some drives are mapped via Group Policy.
- Run `gpresult /R` or `gpresult /H report.html` to see applied policies.

### 5. Remove and Remap the Drive
```cmd
net use Z: /delete
net use Z: \\server\share /persistent:yes
```
- This clears old mappings and remaps fresh.

### 6. Check for Offline Files / Sync Issues
- If using **Offline Files**, conflicts may prevent access.
- Disable Offline Files if not needed.

### 7. DNS and Name Resolution
- Try accessing via IP: `\\192.168.1.10\share`.
- If IP works but name does not, troubleshoot DNS.

### 8. Firewall or Security Software
- Firewalls may block SMB (ports 445/139).
- Temporarily disable security software to test.

---

## Resolution Workflow
1. Confirm network connectivity (ping, IP test).  
2. Verify share path syntax and user permissions.  
3. Clear cached credentials and re-enter.  
4. Delete and remap the drive.  
5. Check Group Policy drive mappings.  
6. Test with IP to rule out DNS issues.  
7. Escalate if persistent (server or AD issue).  

---

## References
- [Microsoft Docs – Map a Network Drive](https://support.microsoft.com/help/4026635)  
- [Microsoft Docs – New-PSDrive](https://learn.microsoft.com/powershell/module/microsoft.powershell.management/new-psdrive)  

---

#tags/Networking #tags/Troubleshooting #tags/Windows #tags/PowerShell
