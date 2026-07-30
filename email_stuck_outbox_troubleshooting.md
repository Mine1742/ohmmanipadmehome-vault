[[Outlook Hub]]
#📨 Troubleshooting: Email Stuck in Outbox

## Issue
Occasional emails are moving to the Outbox but **not sending**. Recreating the email sometimes allows it to go through. Other emails continue to send and receive without issue.

## ✅ Steps to Resolve

### 1. Confirm Outlook Is Online
- Look at the lower-right corner of Outlook for status:
  - Should say: **Connected**, **Connected to Microsoft Exchange**, or similar.
  - If it says **Working Offline**, go to `Send/Receive > Work Offline` to reconnect.

### 2. Try Resending the Stuck Email
- Open the stuck email in the Outbox.
- Click **Send** again.

### 3. Restart Outlook in Safe Mode
- Run:  
  ```bash
  outlook.exe /safe
  ```
- This disables add-ins that may interfere with sending.
- Try sending the stuck email again.

### 4. Check Send/Receive Errors
- Go to `Send/Receive > Show Progress`.
- Look for any error codes (e.g., 0x800ccc13).

### 5. Rebuild the OST File
- Close Outlook.
- Navigate to:
  ```
  %LOCALAPPDATA%\Microsoft\Outlook\
  ```
- Rename the `.ost` file (e.g., `Outlook.ost.bak`).
- Restart Outlook to rebuild the OST cache.

### 6. Use Outlook Web Access (OWA)
- Visit: [https://outlook.office.com](https://outlook.office.com)
- Check if the email appears in Outbox or Drafts.
- Try sending it directly from the web.

### 7. Disable Antivirus/Firewall Temporarily
- Security software may interfere with email transport.
- Temporarily disable AV/firewall and try resending.

### 8. Create a New Outlook Profile
- Go to:
  ```
  Control Panel > Mail > Show Profiles > Add
  ```
- Configure your email account.
- Use the new profile to see if issue persists.

### 9. Check SMTP Authentication Settings
- Only applicable if **not using Exchange or Microsoft 365**.
- Ensure correct SMTP server, port, and authentication settings.

---

## 🛠 Preventative Tips
- Keep Outlook and Windows fully updated.
- Avoid sending oversized attachments — use OneDrive or SharePoint links.
- Regularly clear out stuck emails.
- Use smaller mailbox size or archive old messages.

---

## 🔗 External Links
- [Outlook Safe Mode Instructions](https://support.microsoft.com/en-us/office/open-outlook-in-safe-mode-3f4cf3f5-4d8b-4b53-94cb-43d0f3e72620)
- [Repair Outlook Data Files (.ost and .pst)](https://support.microsoft.com/en-us/office/repair-outlook-data-files-pst-and-ost-25663bc3-11ec-4412-86c4-60458afc5253)
- [How to Create a New Outlook Profile](https://support.microsoft.com/en-us/office/create-an-outlook-profile-f544c1ba-3352-4b3b-be0b-8d42a540459d)

---

## 🏷 Tags
#troubleshooting #email #outlook #microsoft365 #it-support
