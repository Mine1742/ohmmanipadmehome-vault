# 🧾 Brother HL-L6400DW — Scan-to-Email Setup Guide

A step-by-step guide to configure scan-to-email functionality on the Brother HL-L6400DW printer.

---

## 📋 Prerequisites

Before beginning:
- Printer must be **connected to the network** (wired or Wi-Fi) and have a valid **IP address**.
- Access to the printer’s **web interface (Web Based Management)**.
- An available **email account** (Office 365, Gmail, or SMTP relay) with:
  - SMTP server name  
  - Port number  
  - SSL/TLS requirement  
  - Username & password (if authentication is required)

---

## ⚙️ Step 1: Access the Web Interface

1. On the printer, press **Menu → Print Reports → Network Config → Start** to print a network configuration page.
2. Note the **IP address** listed.
3. On your computer, open a browser and enter that IP address (e.g., `http://192.168.1.45`).
4. Log in as **Administrator** (default password is on the printer label or `initpass`).

---

## 📧 Step 2: Configure SMTP Settings

1. In the web interface, navigate to:
   - **Administrator → Network → Protocol → SMTP**  
     *(or)*  
   - **Scan → Scan to Email → Setup** depending on firmware.
2. Enable **SMTP** or **Email Sending** if disabled.
3. Enter mail server details:

| Setting | Example (Microsoft 365) |
|----------|-------------------------|
| SMTP Server | smtp.office365.com |
| Port | 587 |
| Secure Connection | STARTTLS |
| Authentication | On |
| Username | yourname@domain.com |
| Password | (App Password or normal password depending on policy) |

### Gmail Example
| Setting | Value |
|----------|-------|
| SMTP Server | smtp.gmail.com |
| Port | 465 (SSL) or 587 (STARTTLS) |
| Authentication | On |
| Username | yourname@gmail.com |
| Password | Gmail App Password |

---

## 🧠 Step 3: Set Sender and Reply-To Addresses

- **Sender Email Address:** The authenticated account.
- **Display Name:** e.g., *Brother HL-L6400DW*.
- **Reply-To Address:** Optional.

Click **Submit** or **OK** to save.

---

## 🧾 Step 4: Add Email Destinations

1. Navigate to **Scan → Address Book → Add Email Address**.
2. Enter the recipient’s **name** and **email address**.
3. Optionally, assign a shortcut number for quick selection.

---

## 🧪 Step 5: Test Scan-to-Email

1. On the printer, press **Scan → to Email Server**.
2. Choose a stored contact or enter an email manually.
3. Press **Start**.
4. Verify that the recipient receives the email.

---

## 🛠️ Troubleshooting Reference

| Error | Meaning | Resolution |
|-------|----------|------------|
| DHCP/Network Error | No network connection | Verify cable/Wi-Fi connection |
| SMTP Auth Error | Invalid credentials | Re-enter username/password or app password |
| TLS Error | Incorrect port or encryption | Match server’s SSL/TLS settings |
| Cannot Send Email | DNS or relay blocked | Set DNS to 8.8.8.8 or mail relay |

---

## 💡 Tips

- For Microsoft 365, use an **authenticated connector** or **relay** account with “Send As” permissions.
- Secure configuration with **Function Lock** under **Administrator → Security**.
- Backup configuration via **Administrator → Maintenance → Export Settings** after setup.
- Ensure outbound SMTP ports (465 or 587) are not blocked by firewall.

---

**Created for:** MFP scan-to-email setup and field troubleshooting  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #brother #printer #scan #email #smtp #mfp #network
