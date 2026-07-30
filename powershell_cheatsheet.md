# ⚙️ PowerShell Command & Automation Cheat Sheet

A concise reference for everyday scripting, system administration, and automation tasks.

---

## 🧭 GETTING STARTED

### Launch PowerShell
- **Windows:** Press `Win + X`, then select **Windows PowerShell** or **Terminal**  
- **macOS/Linux:** Install via `brew install --cask powershell` or your package manager  
- Run script files with:  
  ```powershell
  .\script.ps1
  ```

### Execution Policy
```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📁 FILE & DIRECTORY MANAGEMENT

```powershell
Get-ChildItem                     # List files (alias: ls, dir)
Get-ChildItem -Recurse            # List all files recursively
Get-Content file.txt              # View file contents
Set-Content file.txt "Text"       # Overwrite file
Add-Content file.txt "New line"   # Append to file
Copy-Item file1.txt backup\      # Copy file
Move-Item file1.txt archive\     # Move or rename
Remove-Item old.log               # Delete file
New-Item new.txt -ItemType File   # Create new file
New-Item Scripts -ItemType Directory
```

---

## 🔍 SEARCHING & FILTERING

```powershell
Get-ChildItem -Recurse | Where-Object {$_.Name -match "error"}     # Files with "error"
Select-String "keyword" *.log                                      # Search inside files
Select-String "Exception" *.ps1 | Select Filename, LineNumber, Line
Get-Process | Where-Object {$_.CPU -gt 100}                        # Filter processes
```

---

## ⚙️ SYSTEM ADMINISTRATION

```powershell
Get-Service                     # List services
Restart-Service spooler          # Restart Print Spooler
Stop-Service wuauserv            # Stop Windows Update service
Get-EventLog -LogName System -Newest 20
Get-Process                     # View processes
Stop-Process -Name notepad -Force
Get-LocalUser                   # List local users
New-LocalUser "TempUser" -Password (Read-Host -AsSecureString)
Add-LocalGroupMember -Group "Administrators" -Member "TempUser"
```

---

## 🌐 NETWORKING

```powershell
Test-Connection google.com                     # Ping
Resolve-DnsName example.com                    # DNS lookup
Get-NetIPAddress                               # Show IP config
Get-NetAdapter                                 # List adapters
Get-NetTCPConnection | Where {$_.State -eq "Listen"}   # Listening ports
Get-NetRoute                                   # Routing table
```

---

## 🧩 TEXT & DATA HANDLING

```powershell
(Get-Content log.txt) -match "Error"                 # Returns True/False
Select-String "Error" log.txt | Measure-Object       # Count matches
Import-Csv users.csv | Where {$_.Department -eq "IT"} | Export-Csv it_users.csv -NoTypeInformation
ConvertTo-Json (Get-Process | Select -First 3)       # JSON output
Get-Process | ConvertTo-Html | Out-File report.html  # HTML report
```

---

## 🧠 VARIABLES & LOOPS

```powershell
$name = "Albert"
for ($i=1; $i -le 5; $i++) { Write-Host "Run $i" }

$users = Get-Content users.txt
foreach ($user in $users) {
    Write-Host "Processing $user"
}
```

---

## 💾 REGISTRY & ENVIRONMENT

```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion"
Set-ItemProperty "HKCU:\Environment" -Name PATH -Value "C:\Tools"
[Environment]::GetEnvironmentVariable("PATH")
```

---

## 🪄 AUTOMATION & TASKS

```powershell
Start-ScheduledTask -TaskName "Backup"
schtasks /query | find "Backup"
Start-Job -ScriptBlock {Get-EventLog -LogName System | Out-File log.txt}
Get-Job; Receive-Job -Id 1
Register-ScheduledJob -Name "DailyReport" -ScriptBlock {Invoke-WebRequest https://example.com/report}
```

---

## ☁️ REMOTE MANAGEMENT

```powershell
Enter-PSSession -ComputerName server01 -Credential admin
Invoke-Command -ComputerName server01 -ScriptBlock {Get-Service}
Enable-PSRemoting -Force
Get-Command -Module PSRemote
```

---

## 🧾 FILE COMPARISON & HASHING

```powershell
Compare-Object (Get-Content file1.txt) (Get-Content file2.txt)
Get-FileHash .\script.ps1 -Algorithm SHA256
```

---

## 📦 MODULES & UPDATES

```powershell
Get-Module -ListAvailable
Install-Module PSWindowsUpdate -Force
Update-Module
Import-Module ActiveDirectory
Get-Command -Module ActiveDirectory
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| List files | `Get-ChildItem` |
| Search text in files | `Select-String "pattern" *.log` |
| Get running processes | `Get-Process` |
| Restart a service | `Restart-Service spooler` |
| Filter by property | `Where-Object {$_.Name -like "*chrome*"}` |
| Export to CSV | `Export-Csv output.csv -NoTypeInformation` |
| Generate JSON | `ConvertTo-Json (Get-Service)` |

---

## 💡 TIPS
- Use `Get-Help <command> -Examples` to learn quickly.
- Use `| Format-Table` or `| ft` to make output readable.
- Use `| Out-GridView` for an interactive table view.
- The pipeline (`|`) passes **objects**, not text—treat them as data.

---

**Created for:** scripting, auditing, and DevOps tasks  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #powershell #scripting #automation #windows #devops
