# Scan to Email Setup Guide

Setting up **Scan to Email** on a multifunction printer (MFP) allows scanned documents to be sent as email attachments. This requires configuring the printer to connect to your organization’s SMTP email server.

---

## ✅ Prerequisites
Before setup, gather the following information:
- **SMTP Server Address** (e.g., `smtp.office365.com`, `smtp.gmail.com`)
- **SMTP Port** (`587` for STARTTLS, `465` for SSL/TLS, or `25` if internal relay is used)
- **Authentication Email Address & Password** (use a dedicated service account if possible)
- **Encryption Method** (STARTTLS or SSL/TLS)
- **From Address** (must match the authenticated account for most providers)

---

## 🔧 Setup Steps

### 1. Access Printer’s Web Interface
1. Print a network status/configuration page from the printer to get its **IP address**.  
2. Open a browser and enter the IP (e.g., `http://192.168.1.100`).  
3. Log in with admin credentials.

---

### 2. Configure SMTP (Email) Settings
1. Navigate to **Scan → Email Setup** or **System → E-mail Settings**.  
2. Enter the SMTP details:
   - **SMTP Server**: `smtp.office365.com` (for Office 365)  
   - **Port**: `587` (with STARTTLS)  
   - **Authentication**: Enabled  
   - **Username**: full email (e.g., `scans@yourcompany.com`)  
   - **Password**: account password or app password  
   - **Default From Address**: same as above  

---

### 3. Add Address Book Entries
- Add frequently used recipient emails.  
- If available, enable LDAP/Active Directory integration for company-wide lookup.  

---

### 4. Test Scan to Email
1. Place a document in the scanner.  
2. Select *Scan to Email*.  
3. Enter a test recipient address.  
4. Confirm delivery in inbox.  

---

## 📌 Common SMTP Configurations

### Office 365 / Microsoft 365
- **Server**: `smtp.office365.com`  
- **Port**: 587  
- **Encryption**: STARTTLS  
- **Authentication**: Required  

### Gmail
- **Server**: `smtp.gmail.com`  
- **Port**: 465 (SSL) or 587 (TLS)  
- **Authentication**: Required  
- **Note**: Requires [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled  

### Local Exchange / SMTP Relay
- Use internal relay server if available.  
- May not require authentication if on trusted network.  

---

## ⚠️ Troubleshooting
- **Error: Cannot connect to SMTP** → Check firewall and port settings.  
- **Authentication failed** → Verify credentials or use app password.  
- **Email not delivered** → Ensure sender is allowed in your mail server’s relay policies.  

---

## 🔗 References
- [Microsoft 365 SMTP settings](https://learn.microsoft.com/en-us/exchange/clients-and-mobile-in-exchange-online/connect-to-smtp)  
- [Google Gmail SMTP settings](https://support.google.com/a/answer/176600?hl=en)  

---

## 🏷️ Tags
#printer #email #troubleshooting #office365 #gmail #smtp
