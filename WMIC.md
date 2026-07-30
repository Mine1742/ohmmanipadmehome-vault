#wmi #wmic

Windows Management Instrumentation Command-line

Basic WMIC Syntax: wmic <alias> <command> <parameters>
- **`<alias>`**: Represents a WMI class or category (e.g., `os`, `process`, `useraccount`).
- **`<command>`**: Specifies an action (e.g., `get`, `list`, `call`).
- **`<parameters>`**: Additional filters or options.

Common WMIC Commands
1. Get System Information

Get basic system info:
cmd: wmic computersystem get model,name,manufacturer,systemtype

Check the operating system version:
cmd:  wmic os get caption,version,buildnumber

List all installed software:
cmd: wmic product get name,version

2. Manage Processes

List all running processes:
cmd: wmic process list brief
Kill a process:
cmd: wmic process where name="notepad.exe" call terminate
Start a process:
cmd: wmic process call create "notepad.exe"

3. Query Hardware Details

Get CPU details:
cmd: wmic cpu get name,maxclockspeed,status
Check hard drive details:
cmd: wmic diskdrive get model,size,serialnumber
Get memory details:
cmd: wmic memorychip get capacity,manufacturer,speed

4. User Management
List all user accounts:
cmd: wmic useraccount list brief
Check if a user account is enabled:
cmd: wmic useraccount where name='username' get name,enabled

5. Network Information
List network adapters:
cmd: wmic nic get name,macaddress
Get IP configuration:
cmd: wmic nicconfig get description,ipaddress,defaultipgateway

6. Remote Management
Query a remote computer:
cmd: wmic /node:"remote-computer-name" computersystem get name
Use credentials for remote access:
cmd: wmic /node:"remote-computer-name" /user:"domain\username" /password:"password" process list brief


