
**Purpose:** Build a locked-down, single-purpose Windows 10 device for legacy fire alarm programming software (Notifier VeriFire Tools 5.7, Silent Knight SKSS, etc.) that will not run on Windows 11, while keeping it managed and safe inside an otherwise all-Win 11 Entra tenant.

**Why this OS:** Windows 10 IoT Enterprise LTSC 2021 is supported with security updates until **January 13, 2032** — no ESU fees, no feature updates, no forced upgrades. It is functionally Windows 10 Enterprise 21H2 minus the consumer clutter (no Store, no Edge preinstalled on some images, no inbox UWP apps), which is exactly what an appliance-class device wants.

> ⚠️ Do **not** confuse this with standard Windows 10 Enterprise LTSC 2021, which ends support January 12, 2027. The SKU you want is specifically **IoT Enterprise LTSC 2021**.

---

## Phase 0 — Planning & Procurement

### 0.1 Licensing

IoT Enterprise licenses are sold through the **OEM/embedded channel**, not the standard volume licensing portal. Options:

1. **Embedded/IoT distributor** — Avnet, Arrow, ADI/BlueStar, or similar. You purchase an entitlement (typically tied to a CPU class) and receive an ISO + product key. For 1–2 devices this is a small PO.
2. **Device already licensed** — Some rugged/industrial laptop vendors (Panasonic Toughbook, Getac, Dell rugged line) will sell hardware with IoT Enterprise LTSC preinstalled. If you're buying hardware anyway, this is the least friction.
3. **CDW / SHI / Insight** — Larger resellers can also source IoT Enterprise entitlements; ask specifically for "Windows 10 IoT Enterprise LTSC 2021 value/high-end SKU" (SKU tier is CPU-based: Celeron/entry = value, Core i5/i7 = high end).

Keep the entitlement paperwork — activation is via a standard product key (OA3/ePKEA or key card), not KMS in most embedded-channel purchases.

### 0.2 Hardware checklist for the repurposed machine

- [ ] CPU/RAM adequate: VeriFire and SKSS are lightweight; any 8th-gen Intel or newer with 8 GB RAM is plenty
- [ ] **TPM 2.0 present and enabled** (needed for BitLocker + clean Entra join attestation)
- [ ] **Native RS-232 serial port or plan for USB-serial adapters** — this matters more than anything else on this build. Panel programming is serial-heavy. FTDI-chipset adapters (not Prolific clones) are the reliable choice
- [ ] SSD (swap in a fresh one if the machine is a hand-me-down — cheap insurance)
- [ ] BIOS updated to latest version **before** install
- [ ] BIOS: SATA mode set to **AHCI** (you've hit the RAID→AHCI driver problem before; settle it now, not mid-install)
- [ ] BIOS: Secure Boot **enabled**, TPM enabled, virtualization enabled (for VBS/HVCI)
- [ ] Wi-Fi card identified — note the exact model so you can stage the driver (LTSC images are lean and frequently lack current Wi-Fi drivers, especially Intel AX-series)

### 0.3 Downloads to stage on a USB drive before you start

- IoT Enterprise LTSC 2021 ISO (from your distributor / entitlement portal)
- Rufus (or use the Media Creation-style `diskpart` + copy method)
- OEM driver pack for the laptop model (chipset, Wi-Fi, Ethernet, storage) — export from the vendor's site or from a working identical machine (`pnputil /export-driver * C:\Drivers`)
- FTDI VCP drivers for your USB-serial adapters
- Notifier VeriFire Tools 5.7 installer + any panel firmware databases
- Silent Knight SKSS installer (+ SKSS downloading software / HFSS if used)
- Any other panel tools (Fire-Lite FS-Tools, Gamewell, etc.)
- Latest cumulative update (`.msu`) for Windows 10 LTSC 2021 from the Microsoft Update Catalog (search "Windows 10 21H2 cumulative x64") — lets you patch offline before the device ever touches a network

---

## Phase 1 — OS Installation

### 1.1 Create install media

1. Rufus → select the LTSC ISO → GPT partition scheme, UEFI (non-CSM) target → default NTFS.
2. Copy the driver pack and staged installers to a second folder on the same USB (or a second stick).

### 1.2 Clean install

1. Boot the USB (F12/F9 one-time boot menu depending on vendor).
2. At the install screen, delete **all** existing partitions on the target disk → install to unallocated space.
3. If the disk isn't visible: you're in RAID/RST mode — either load the Intel RST driver from the driver pack (`Load driver`) or reboot into BIOS and flip to AHCI (preferred).
4. Enter the IoT Enterprise product key when prompted (or choose "I don't have a key" and activate later with `slmgr`).

### 1.3 OOBE — keep it local for now

1. At OOBE, **do not** connect to a network yet. LTSC OOBE will happily create a local account offline — do that.
2. Create a local admin account with a non-obvious name (e.g., `pgmadmin`), strong password → this becomes your break-glass local admin. The field tech will get a separate account later.
3. Skip all telemetry/diagnostics prompts at the minimum settings.

### 1.4 Drivers and offline patching

1. Install the chipset, storage, Ethernet, and Wi-Fi drivers from your staged pack. If Wi-Fi is missing from Device Manager, this is the manual driver injection you've done before: `pnputil /add-driver <path>\*.inf /subdirs /install`.
2. Install the staged cumulative update `.msu` **before** connecting to any network.
3. Reboot, verify Device Manager is clean (no bangs).
4. Activate if needed: `slmgr /ipk XXXXX-XXXXX-XXXXX-XXXXX-XXXXX` then `slmgr /ato` (this one needs network — fine to do after Phase 2 join).

---

## Phase 2 — Entra Join & Intune Enrollment

You want this device **visible and managed**, just heavily fenced. Entra joined + Intune enrolled, then scoped hard with filters and Conditional Access.

### 2.1 Pre-stage in Intune (do this from your admin workstation first)

1. **Create an Entra security group** — e.g., `SG-Devices-OT-PanelProgramming` (assigned membership; you'll add the device object after join).
2. **Create a device filter** in Intune (Tenant admin → Filters):
    - Rule: `(device.deviceOwnership -eq "Corporate") and (device.displayName -startsWith "OT-FIRE")` — or simpler, filter on the OS: `(device.operatingSystemVersion -startsWith "10.0.19044")`
    - You'll use this filter to _exclude_ the device from Win 11 baselines and _include_ it in the OT policy set.
3. **Review your existing Compliance policies** — if your tenant compliance policy requires Windows 11 minimum OS version, this device will land non-compliant and CA will lock it out of everything, including enrollment completion. Either:
    - Create a **separate compliance policy** for the OT group (min OS `10.0.19044.x`, BitLocker required, Defender required, Secure Boot required), and exclude the OT group from the Win 11 compliance policy, **or**
    - Assign the Win 11 policy with the OT filter set to _exclude_.
4. **Naming convention:** decide now — e.g., `OT-FIRE-01`. Rename before or immediately after join so your filters and dynamic rules catch it.

### 2.2 Join the device

1. Connect to network (this is the device's first network contact — it's patched, so acceptable).
2. Rename the PC: `Rename-Computer -NewName "OT-FIRE-01" -Restart` (elevated PowerShell).
3. Settings → Accounts → Access work or school → **Connect** → **Join this device to Microsoft Entra ID** (bottom link, _not_ the "add work account" flow).
4. Sign in with the enrollment account. Recommendation: use a **dedicated onboarding/admin identity**, not the field tech's account — whoever joins becomes local admin by default unless you've configured the Entra local admin settings/LAPS.
5. Verify: `dsregcmd /status` → `AzureAdJoined : YES`, `MDMUrl` populated.
6. In Intune, confirm the device appears and finishes enrollment; add the device object to `SG-Devices-OT-PanelProgramming`.

### 2.3 Local accounts strategy

- Enable **Windows LAPS** (Entra-backed) for the local `pgmadmin` account so the break-glass password rotates and escrows to Entra.
- The field tech signs in with **their Entra account as a standard user** (default for Entra join — only the joiner and designated admins get local admin). This gives you sign-in auditing without giving the tech admin rights.
- If the tech needs to install panel firmware updates in the field, prefer an **elevation path** (LAPS retrieval by IT, or Endpoint Privilege Management if licensed) over making them a permanent admin.

---

## Phase 3 — Conditional Access Fencing

Goal: the device authenticates to Entra for management and sign-in, but **cannot** reach Exchange, SharePoint, Teams, or anything else it doesn't need.

### 3.1 Block M365 workloads from this device

Create a CA policy:

- **Name:** `CA-Block-M365-From-OT-PanelDevices`
- **Users:** All users (or the tech's account — but device-based is more durable)
- **Target resources:** Office 365 (the grouped app) — or All cloud apps with exclusions for Intune enrollment endpoints (`Microsoft Intune`, `Microsoft Intune Enrollment`) and Windows sign-in
- **Conditions → Filter for devices:** Include → `device.displayName -startsWith "OT-FIRE"` (or extensionAttribute if you prefer tagging: set `extensionAttribute1 = "OT"` on the device object and filter on that — more resilient to renames)
- **Grant:** Block
- Run it in **report-only** for a day, check the sign-in logs, then enable.

### 3.2 Keep the tech's normal experience intact elsewhere

Because the filter is device-scoped, the tech's account works normally on their Win 11 daily driver. Nothing user-scoped to change.

### 3.3 Exclude from Win 11 stuff

Sweep your tenant for anything that would fight this device:

- [ ] Feature update / Windows Update rings — exclude the OT group, or create a dedicated update ring: **security updates only**, feature updates deferred/blocked (LTSC won't take feature updates anyway, but keep the ring clean)
- [ ] Autopatch, if used — exclude
- [ ] Any remediation scripts assuming Win 11 paths
- [ ] Windows 11 upgrade policies / readiness — exclude explicitly so nothing nags or attempts an upgrade

---

## Phase 4 — Hardening

This is an OT engineering workstation. Treat it like one.

### 4.1 Intune configuration profiles (assign to `SG-Devices-OT-PanelProgramming`)

**BitLocker (Endpoint security → Disk encryption):**

- OS drive: XTS-AES 256, TPM required, recovery key escrow to Entra ID, hide recovery options from end user
- Silent enablement on

**Defender (Endpoint security → Antivirus):**

- Real-time protection, cloud-delivered protection (High), PUA blocking on
- Scheduled full scan weekly
- Onboard to **Defender for Endpoint** if licensed — MDE fully supports Win 10 21H2 and gives you EDR visibility on exactly the device that needs it most

**Attack Surface Reduction rules (Endpoint security → ASR):** enable in Block mode at minimum:

- Block executable content from email/webmail
- Block Office apps creating child processes (harmless here — no Office installed)
- Block credential stealing from LSASS
- Block execution of potentially obfuscated scripts
- Block untrusted/unsigned processes from USB ← **test this one in Audit first**; your panel installers and FTDI drivers come in via USB. Promote to Block after confirming your toolchain is whitelisted or installed.

**Firewall (Endpoint security → Firewall):**

- Default inbound: **Block all** (no exceptions — nothing should ever connect _to_ this laptop)
- Outbound: allow, but see network notes in 4.3

**Device restrictions / Settings catalog:**

- Disable Microsoft consumer experiences, Cortana, widgets-equivalents (mostly absent on LTSC anyway)
- Disable OneDrive (Settings catalog: "Prevent the usage of OneDrive for file storage")
- Block Microsoft account sign-in for apps
- Screen lock: 10 min, require password on wake
- Disable Wi-Fi Sense / auto-connect to open hotspots

### 4.2 Application control — the big one

The strongest single control for an appliance device is an allow-list. Two tiers depending on appetite:

**Tier 1 — AppLocker (simpler, good enough):**

1. Build the machine completely (all panel software installed, Phase 5) **first**.
2. On the device, run `Get-AppLockerFileInformation -Directory "C:\Program Files (x86)" -Recurse` etc. to inventory, or just use the AppLocker wizard's "generate rules from folder."
3. Rules: allow `C:\Windows\*`, `C:\Program Files\*`, `C:\Program Files (x86)\*` for Everyone; **no user-writable paths allowed**; explicit publisher or hash rules for the panel tools if any live outside Program Files (some legacy fire tools install to `C:\` root or `C:\Notifier` — hash/path rules for those).
4. Deploy via Intune (Settings catalog → AppLocker CSP, or a custom OMA-URI with the exported XML), Audit mode for a week → Enforce.

**Tier 2 — WDAC/App Control for Business:** stronger (kernel-enforced) but more brittle with unsigned legacy installers. Given VeriFire 5.7-era code signing practices, expect unsigned binaries; AppLocker with hash rules is usually the pragmatic call here.

### 4.3 Network posture

- **In the field:** the laptop talks to a fire panel over serial/USB and maybe a hotspot for email-free reference downloads. Fine.
- **In the office:** put it on a **segmented VLAN** (your OT/IoT segment if one exists, or a guest-adjacent VLAN with internet-only + explicit allows to Windows Update, Intune endpoints, and Defender cloud). It has no business on the same L2 as domain controllers or servers.
- Consider blocking outbound SMB (445/139) and RDP (3389) at the host firewall outright.
- No VPN client, no access to internal file shares. If the tech needs panel config files, transfer via a scoped mechanism (e.g., a single dedicated SharePoint library accessed from their _daily_ device, then USB across — or a Teams-free flow you control).

### 4.4 Browser

LTSC 2021 ships with IE remnants but not modern Edge. Options:

- Install current **Edge** (still supported on Win 10 LTSC) and lock it down via Intune Edge policies: SmartScreen enforced, extensions blocked, downloads restricted, homepage set to a blank page. Rationale: you _will_ occasionally need to download a panel firmware file from Honeywell/Silent Knight portals.
- Or install no browser at all and treat all file staging as USB-from-daily-device. Cleaner, slightly more friction.

---

## Phase 5 — Panel Software Installation

Order matters less than documentation — capture everything so the _next_ rebuild is an afternoon, not a week.

1. **FTDI VCP drivers first**, then plug in each USB-serial adapter and note its assigned COM port. Pin the COM assignments: Device Manager → adapter → Port Settings → Advanced → set explicit COM numbers (e.g., COM3 always = the gray Notifier cable). Legacy tools often hardcode or poorly enumerate COM ports.
2. **Notifier VeriFire Tools 5.7:**
    - Run installer as admin (from `pgmadmin` or elevated session)
    - Install any panel-family database/firmware packs the techs use
    - Launch once as the _tech's standard account_ and confirm it runs without admin (many legacy tools write to their own Program Files folder — if it fails as standard user, grant Modify on the app's data folder to the tech's account rather than making them admin: `icacls "C:\Program Files (x86)\<app>\Data" /grant "Users:(OI)(CI)M"`)
3. **Silent Knight SKSS:** same pattern. SKSS is old enough that it may want to write to its install directory — same `icacls` targeted-permissions fix.
4. **Other tools** (Fire-Lite FS-Tools, etc.): repeat.
5. **Compatibility shims if needed:** right-click → Properties → Compatibility → run in Windows 7/XP SP3 compatibility mode is sometimes needed for the oldest tools; document any shims applied.
6. **Test end-to-end against a real panel** (or a bench panel at the shop) before declaring victory — serial timing issues only show up against hardware.
7. **Snapshot the result:** after everything works, capture a full image (e.g., `wbadmin` system image to an external drive, or Macrium/Clonezilla). This is your golden image for rebuilds — legacy installers have a way of disappearing from vendor portals.

---

## Phase 6 — Ongoing Operations

|Task|Cadence|Notes|
|---|---|---|
|Cumulative updates|Monthly (Patch Tuesday)|Via the dedicated Intune update ring; LTSC gets security-only, no feature updates|
|Defender signature/platform|Automatic|Verify in MDE portal monthly|
|Sign-in / device audit|Monthly|Confirm CA block policy shows blocked attempts = 0 anomalies|
|BitLocker key escrow check|Quarterly|Entra ID → device → recovery keys present|
|LAPS password rotation|Automatic|Spot-check retrievability quarterly|
|AppLocker audit log review|Quarterly|Look for blocked-execution noise = drift or tampering|
|Golden image refresh|After any software change|Re-image after adding/updating panel tools|
|Vendor Win 11 support check|Every 6 months|The moment VeriFire/SKSS successors run on Win 11, plan the retirement of this device|
|Hardware health|Annually|It's a field laptop; battery, hinge, port wear|

### End-of-life plan

Write the exit criteria now: this device retires when (a) all required panel tools run supported on Win 11, or (b) January 2032, whichever comes first. Put a recurring reminder in your ticketing system so it doesn't become the forgotten XP machine in the closet.

---

## Quick-Reference Summary

- **OS:** Windows 10 IoT Enterprise LTSC 2021 (supported to Jan 2032, embedded channel licensing)
- **Identity:** Entra joined, Intune enrolled, dedicated device group + filter, LAPS on local admin, tech signs in as standard user
- **Fencing:** CA policy blocks all M365 workloads by device filter; excluded from all Win 11 baselines/update rings; separate compliance policy
- **Hardening:** BitLocker, Defender/MDE, ASR block mode, inbound-block firewall, AppLocker allow-list, no OneDrive/no personal MSA, segmented VLAN in-office
- **Software:** FTDI drivers with pinned COM ports → VeriFire 5.7 → SKSS → others; `icacls` folder grants instead of admin rights; golden image after build
- **Lifecycle:** monthly patching, quarterly audits, semi-annual vendor check, hard retirement criteria documented