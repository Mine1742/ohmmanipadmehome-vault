# Drive “Disappears” After Windows Update — Triage & Fix Guide

_Last updated: 2025-09-29_

**TL;DR:** Windows Updates can reshuffle storage and networking at boot. That can unassign a **drive letter**, disable **automount**, require **BitLocker** re‑auth, swap **USB/storage drivers**, or remap **network drives** before the network/VPN is up. Use the decision tree below to identify your case and apply the matching fix.

---

## Decision Tree (Pick Your Path)

1. **Is it an internal disk/partition (SATA/NVMe)?**  
   Go to [Case A](#case-a-internal-diskpartition-satanvme).

2. **Is it an external USB drive?**  
   Go to [Case B](#case-b-external-usb-hddssd).

3. **Is it a mapped network drive (\\\\server\\share)?**  
   Go to [Case C](#case-c-mapped-network-drive).

4. **Is it a cloud-sync folder (OneDrive/Dropbox/Google Drive)?**  
   Go to [Case D](#case-d-cloud-sync-roots-and-virtual-drives).

5. **None fit / intermittent only after updates?**  
   Scan [Case E](#case-e-oddballs-and-edge-cases).

---

## Case A: Internal disk/partition (SATA/NVMe)

**Symptoms**
- Disk shows in Disk Management but has **no drive letter**.
- Volume shows as **BitLocker locked** after reboot.
- Disk intermittently missing until a **rescan**.
- Recent **chipset/storage driver** change.

**Fixes**

### A1) Reassign the drive letter
1. `Win+X → Disk Management (diskmgmt.msc)`  
2. Right‑click the volume → **Change Drive Letter and Paths…** → **Add/Change** → choose a **high, stable letter** (e.g., `R:`).

### A2) Re‑enable automount and rescan (Admin)
```text
diskpart
automount
automount enable
rescan
exit
```

### A3) BitLocker auto‑unlock
Check status and re‑enable autounlock (replace `E:` with your volume):
```cmd
manage-bde -status
manage-bde -autounlock -enable E:
```

### A4) Refresh storage drivers
- **Device Manager** → **Storage controllers / IDE/ATA/ATAPI / NVMe/RAID** → **Update driver**.  
- Reinstall OEM **chipset**, **Intel RST** / **AMD NVMe** packages if offered.

> **Prevention:** Keep a **fixed high letter** for secondary volumes and ensure **automount** stays enabled. Consider disabling **Fast Startup** if disks initialize late (see Case E).

---

## Case B: External USB HDD/SSD

**Symptoms**
- Works until reboot/update; then “missing”.
- Shows up again after unplug/plug.
- Letter changes or collides with a mapped drive.

**Fixes**

### B1) Disable aggressive USB power saving
- Device Manager → **Universal Serial Bus controllers** → each **USB Root Hub (USB 3.0)** → **Power Management** tab → uncheck **Allow the computer to turn off this device to save power**.
- Power Options → Advanced → **USB selective suspend** → **Disabled**.

### B2) Assign a stable **high** letter
- Use Disk Management and pick `T:` or `X:` to avoid collisions with network letters.

### B3) Update drivers
- Install OEM **chipset/USB controller** drivers.

> **Prevention:** Keep external drives on a **fixed high letter**; avoid letters commonly used by network shares (e.g., `H:, S:, Z:`).

---

## Case C: Mapped Network Drive

**Symptoms**
- Explorer shows drive as **Disconnected**, yet path works after opening `\\\\server\\share` directly.
- Appears after a delay, or only after VPN connects.
- Prompts for credentials post‑update.

**Quick Tests (PowerShell)**
```powershell
net use
Test-Path \\server\share
```

**Fixes**

### C1) Clean remap (with persistence)
```cmd
net use * /delete /y
cmdkey /list
:: (Optionally remove stale entries shown above)
net use Z: \\server\share /persistent:yes
```

If using alternate creds:
```cmd
cmdkey /add:server /user:DOMAIN\user /pass:YourPassword
net use Z: \\server\share /user:DOMAIN\user /persistent:yes
```

### C2) Delay mapping until network/VPN is ready
Create a **Task Scheduler** task (Triggers: _At log on_, Delay: **30–60s**) to run this PowerShell:
```powershell
$share='\\server\share'
$drive='Z'
for($i=0;$i -lt 24;$i++){
  if(Test-Path $share){
    if(Get-PSDrive -Name $drive -ErrorAction SilentlyContinue){ Remove-PSDrive $drive -Force -ErrorAction SilentlyContinue }
    New-PSDrive -Name $drive -PSProvider FileSystem -Root $share -Persist | Out-Null
    break
  }
  Start-Sleep 5
}
```

**Domain/GPO approach**
- User Config → Preferences → **Windows Settings → Drive Maps**.  
- Enable: **Run in logged-on user’s security context**.  
- Computer Config → Policies → Admin Templates → System → Logon → **Always wait for the network at computer startup and logon** = **Enabled**.

> **Prevention:** Reserve high letters for **local** disks and assign **predictable letters** for network shares in GPO. Be mindful of SMB protocol changes on old NAS boxes.

---

## Case D: Cloud Sync Roots and Virtual Drives

**Symptoms**
- OneDrive/Dropbox/Google Drive “missing” or shows placeholders only.
- Sync client signed out during update or **Files On-Demand** changed.
- A custom letter you mapped to the sync root no longer exists.

**Fixes**
- Re‑sign in to the sync client; verify sync **root path** and **Files On‑Demand** setting.
- If you used a custom letter via `subst`/junction, recreate it (adjust path to your tenant):
```cmd
subst O: "C:\Users\<you>\OneDrive - Company"
```

---

## Case E: Oddballs and Edge Cases

- **Fast Startup**: can race device init.  
  Control Panel → Power Options → Choose what the power buttons do → uncheck **Turn on fast startup**.
- **MountPoints2 cache**: reassigning the letter regenerates it automatically.
- **SMB protocol policy**: Updates may disable legacy SMB1; update the NAS or ensure SMB2/3.
- **SAN policy / Automount disabled**: `diskpart → automount enable` (see A2).

---

## One‑Shot “Fix It Now” Sequence (Admin)

1. **Disk letters & automount**
   ```text
   diskpart
   automount enable
   rescan
   exit
   ```
2. **Network drives (clean remap)**
   ```cmd
   net use * /delete /y
   cmdkey /list
   :: remove stale entries if needed
   net use Z: \\server\share /persistent:yes
   ```
3. **USB power (set once)**
   - Disable **USB selective suspend** and hub power‑saving (see B1).

---

## Operational Tips

- Prefer **high, reserved letters** for local/external disks to avoid collisions.  
- Keep a **post‑update checklist**: driver health, BitLocker auto‑unlock, network drive policy.  
- For laptops that undock frequently, use the **Task Scheduler** delayed‑map approach to make network drives deterministic.

---

## Saved Snippets

### Rebuild a mapped drive after VPN connects (per‑user Task)
```powershell
$drives = @(
  @{Name='S'; Root='\\fileserver\Shares'},
  @{Name='P'; Root='\\fileserver\Projects'}
)
foreach($d in $drives){
  1..24 | ForEach-Object {
    if(Test-Path $d.Root){
      if(Get-PSDrive -Name $d.Name -ErrorAction SilentlyContinue){ Remove-PSDrive $d.Name -Force -ErrorAction SilentlyContinue }
      New-PSDrive -Name $d.Name -PSProvider FileSystem -Root $d.Root -Persist | Out-Null
      break
    }
    Start-Sleep 5
  }
}
```

### Check BitLocker status all volumes
```powershell
Get-BitLockerVolume | Select-Object MountPoint,VolumeStatus,AutoUnlockEnabled,KeyProtector
```

---

## Tags
#Windows #Storage #Troubleshooting #DiskPart #BitLocker #USB #NetworkDrives #GPO #PowerShell #OneDrive

