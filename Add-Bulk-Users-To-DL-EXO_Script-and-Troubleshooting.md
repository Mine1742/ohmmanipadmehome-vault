
# Bulk Add Users to a Distribution List (Exchange Online) — Script + Troubleshooting
**Last updated:** 2025-08-28

This note contains a **robust** PowerShell script to bulk‑add members from a CSV into a group. It works for classic **Distribution Groups** and **Microsoft 365 Groups** and avoids common path issues seen in Windows PowerShell (e.g., `$report` being null, `Split-Path` parameter‑set errors).

---

## CSV format (examples)
Use a header with email/UPN (any one of these is fine):

```csv
Email
user1@archkey.com
user2@archkey.com
```
or
```csv
UserPrincipalName
user1@archkey.com
user2@archkey.com
```

Supported column names (first match wins): `Email, PrimarySmtpAddress, UserPrincipalName, UPN, Mail, User, Address`.

---

## Usage
```powershell
# Preview (WhatIf) then commit
.\Add-BulkGroupMembers.ps1 -GroupIdentity 'CLB@archkey.com' -CsvPath '.\CLB.csv' -WhatIf
.\Add-BulkGroupMembers.ps1 -GroupIdentity 'CLB@archkey.com' -CsvPath '.\CLB.csv'
```

---

## Script: Add-BulkGroupMembers.ps1 (hardened)
```powershell
param(
  [Parameter(Mandatory=$true)]
  [string]$GroupIdentity,              # e.g., CLB@archkey.com, alias, or DN

  [Parameter(Mandatory=$true)]
  [string]$CsvPath,                    # e.g., .\CLB.csv or C:\Path\CLB.csv

  [switch]$WhatIf                      # Preview actions without making changes
)

Import-Module ExchangeOnlineManagement -ErrorAction SilentlyContinue | Out-Null
try { Disconnect-ExchangeOnline -Confirm:$false -ErrorAction SilentlyContinue } catch {}
Connect-ExchangeOnline -ShowBanner:$false

if (-not (Test-Path -LiteralPath $CsvPath)) { throw "CSV not found: $CsvPath" }

# Load CSV and pick a supported column
$headerOrder = 'Email','PrimarySmtpAddress','UserPrincipalName','UPN','Mail','User','Address'
$rows = Import-Csv -LiteralPath $CsvPath
if (-not $rows -or $rows.Count -eq 0) { throw "CSV is empty: $CsvPath" }

$col = $null
foreach ($h in $headerOrder) { if ($rows[0].PSObject.Properties.Name -contains $h) { $col = $h; break } }
if (-not $col) { throw "CSV must contain one of these headers: $($headerOrder -join ', ')" }

# Resolve group and determine type
$grp = Get-Recipient -Identity $GroupIdentity -ErrorAction Stop
$groupType = $grp.RecipientTypeDetails

# Fetch existing members (skip-if-present)
switch ($groupType) {
  'GroupMailbox' { $existing = (Get-UnifiedGroupLinks -Identity $grp.Identity -LinkType Members -ResultSize Unlimited -ErrorAction SilentlyContinue).PrimarySmtpAddress }
  default       { $existing = (Get-DistributionGroupMember -Identity $grp.Identity -ResultSize Unlimited -ErrorAction SilentlyContinue).PrimarySmtpAddress }
}

# Build a safe report path (handles relative CSVs and 'Split-Path' quirks)
$csvFull = (Resolve-Path -LiteralPath $CsvPath).Path
$dir     = [System.IO.Path]::GetDirectoryName($csvFull)
if ([string]::IsNullOrWhiteSpace($dir)) { $dir = (Get-Location).Path }

$stamp   = Get-Date -Format 'yyyyMMdd-HHmmss'
$base    = if ($grp.PrimarySmtpAddress) { $grp.PrimarySmtpAddress } else { $GroupIdentity }
$safe    = ($base -replace '@','_at_') -replace '[^a-zA-Z0-9._-]','_'
$report  = Join-Path -Path $dir -ChildPath ("Add-BulkGroupMembers_{0}_{1}.csv" -f $safe, $stamp)

Write-Host ("Processing {0} entries from {1} into group '{2}' [{3}]" -f $rows.Count, $csvFull, $grp.PrimarySmtpAddress, $groupType)

$out = @()
foreach ($row in $rows) {
  $raw = ($row.$col).ToString().Trim()
  if ([string]::IsNullOrWhiteSpace($raw)) { continue }

  # Resolve recipient
  $recip = $null
  try { $recip = Get-Recipient -Identity $raw -ErrorAction Stop } catch {}
  if (-not $recip) {
    $out += [pscustomobject]@{ Input=$raw; Resolved=$null; Action='Skip'; Status='Fail'; Message='Recipient not found' }
    continue
  }

  # Already a member?
  $already = $false
  if ($existing) { $already = $existing -contains $recip.PrimarySmtpAddress }
  if ($already) {
    $out += [pscustomobject]@{ Input=$raw; Resolved=$recip.PrimarySmtpAddress; Action='Skip'; Status='OK'; Message='Already a member' }
    continue
  }

  try {
    if ($groupType -eq 'GroupMailbox') {
      if ($WhatIf) { Write-Host "[WhatIf] Add-UnifiedGroupLinks -Identity '$($grp.Identity)' -LinkType Members -Links '$($recip.Identity)'" }
      else         { Add-UnifiedGroupLinks -Identity $grp.Identity -LinkType Members -Links $recip.Identity -ErrorAction Stop }
    } else {
      if ($WhatIf) { Write-Host "[WhatIf] Add-DistributionGroupMember -Identity '$($grp.Identity)' -Member '$($recip.Identity)' -BypassSecurityGroupManagerCheck" }
      else         { Add-DistributionGroupMember -Identity $grp.Identity -Member $recip.Identity -BypassSecurityGroupManagerCheck -ErrorAction Stop }
    }
    $out += [pscustomobject]@{ Input=$raw; Resolved=$recip.PrimarySmtpAddress; Action='Add'; Status='OK'; Message='' }
  } catch {
    $out += [pscustomobject]@{ Input=$raw; Resolved=$recip.PrimarySmtpAddress; Action='Add'; Status='Fail'; Message=$_.Exception.Message }
  }
}

# Always emit a report (even in -WhatIf)
$out | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath $report
Write-Host "Done. Report: $report"
```

---

## Troubleshooting
- **`Export-Csv ... -LiteralPath $report` is null/empty**  
  Caused by building `$report` from a relative CSV path. The script above resolves the CSV to a **full path** and uses `[System.IO.Path]::GetDirectoryName()` to avoid `Split-Path` parameter‑set conflicts.
- **`Split-Path ... -LiteralPath ... -Parent : Parameter set cannot be resolved`**  
  Some environments throw this when combining `-LiteralPath` and `-Parent`. The script avoids it by using `[System.IO.Path]::GetDirectoryName()`.
- **Members already present** are skipped and noted in the report.  
- **Permission errors**: ensure your account can modify group membership (e.g., Recipient Management).

---

## Tags
#KB/ExchangeOnline #KB/Groups #KB/DistributionList #PowerShell #Automation #Troubleshooting
