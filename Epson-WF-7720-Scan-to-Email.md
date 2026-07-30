# Epson WF-7720 — Scan to Email (SMTP + Epson Connect)
**Last updated:** 2025-08-27

## Summary
Set up **Scan to Email** on the Epson WF‑7720 either by configuring a **direct SMTP server** (e.g., Microsoft 365 or Gmail) or by using **Epson Connect – Scan to Cloud**.

---

## Option A — Direct SMTP (recommended in managed environments)
Use this when you want emails to come **from** a mailbox you control (e.g., `scanner@yourdomain.com`).

### 1) Collect SMTP details
- **Microsoft 365 (Exchange Online)**  
  - Server: `smtp.office365.com`  
  - Port: **587**  
  - Encryption: **STARTTLS**  
  - Auth: **SMTP-AUTH (username + password)**  
- **Gmail**  
  - Server: `smtp.gmail.com`  
  - Port: **587 (TLS)** or **465 (SSL)**  
  - Auth: Username = full Gmail address; Password = **App Password** (requires 2‑Step Verification)

### 2) Configure SMTP on the printer (control panel)
`Home → Settings → General Settings → Network Settings → Advanced → Email Server → Server Settings`  
- Choose **SMTP-AUTH** (not POP before SMTP).  
- Enter SMTP server, **port**, and **encryption**.  
- **Authenticated Account** = mailbox UPN (e.g., `scanner@contoso.com`).  
- **Authenticated Password** = mailbox password (or **Gmail App Password**).  
- **Sender's Email Address** = the same mailbox address.  
- **Connection Check** to verify.

### 3) Add Contacts (optional)
From **Scan → Email**, use **Contacts** to store frequent addresses.

### 4) Scan to email (panel steps)
`Home → Scan → Email` → pick **Contacts**/**Keyboard**/**History** → **Scan Settings** → **File Format** → **Send`.

---

## Option B — Epson Connect (Scan to Cloud)
If SMTP is blocked or complex, enable Epson Connect and use **Scan to Cloud** with a **Destination List** (email addresses or cloud apps).  
- Activate Epson Connect (register device), then build **Scan to Cloud → Destination List** in your Epson Connect account.  
- On the WF‑7720, choose **Scan → Cloud**.

---

## Best practices
- Create a **dedicated mailbox** (e.g., `scanner@yourdomain.com`) and allow SMTP AUTH just for that account.  
- Keep **time/date** correct.  
- Limit email size in **Scan Settings**.  
- For Microsoft 365, consider **Direct Send** via an EXO connector if you must avoid authentication (uses your org’s public IP and port 25).

## Troubleshooting
- **Auth errors**: For M365 ensure **SMTP AUTH** is enabled; for Gmail use an **App Password**.  
- **TLS/STARTTLS**: Match your provider’s port/encryption.  
- **Firewall**: Allow outbound to SMTP host/port.  
- **Large PDFs**: Reduce **Resolution**/**Compression Ratio**.

---

## Internal tags
#KB/Printers #KB/Epson #KB/ScanToEmail #KB/Outlook #KB/ExchangeOnline #HowTo