[[Outlook Hub]]
# Sending SMS via Distribution List and Creating Outlook Mailbox Rules

## 📱 Sending SMS via a Distribution List in Microsoft 365

### ✅ Requirements
- Microsoft 365 admin rights to modify Distribution Lists (DLs)
- Email-to-SMS gateway domains for recipients' carriers
- SMS email addresses (e.g., `2025551234@vtext.com`)

### 📤 Steps

1. **Create or Edit the Distribution List**
   - Go to [admin.microsoft.com](https://admin.microsoft.com/)
   - Navigate to **Groups > Active groups**
   - Choose an existing DL or create a new one
     - Group type: **Distribution**
     - Add members manually

2. **Add SMS Addresses to the DL**
   For each user, format their phone number with their carrier's email-to-SMS domain:
   - Verizon: `@vtext.com`
   - AT&T: `@txt.att.net`
   - T-Mobile: `@tmomail.net`
   - Sprint: `@messaging.sprintpcs.com`
   - **MetTel**: `@sms.mettel.net`
   
   Example: `2025551234@sms.mettel.net`

3. **Send Email to DL**
   - Open Outlook
   - Send an email to the DL address (e.g., `alerts@yourdomain.com`)
   - Use plain text format; limit message to 160 characters for best SMS compatibility

4. **Restrict Who Can Send to DL** *(Optional)*
   - Configure sender restrictions in DL settings for internal use only

### ⚠️ Notes
- Long messages may be split or truncated
- No attachments supported
- Delivery speed depends on the mobile carrier

---

## 📬 How to Create Outlook Mailbox Rules

### ✅ In Outlook Desktop App
1. Open Outlook
2. Click **Home > Rules > Manage Rules & Alerts**
3. Click **New Rule**
4. Choose a rule template (e.g., "Move messages from someone to a folder")
5. Define conditions and actions
6. Name the rule and click **Finish**

### ✅ In Outlook Web App
1. Go to [Outlook Web](https://outlook.office.com/)
2. Click the **gear icon (⚙)** > Search **Inbox Rules**
3. Click **+ Add new rule**
4. Enter:
   - **Name**
   - **Condition** (e.g., from `billing@company.com`)
   - **Action** (e.g., move to folder “Invoices”)
5. Click **Save**

### 🔁 Common Rule Scenarios
- Move newsletters to a "Promotions" folder
- Flag high-priority messages
- Forward select emails to SMS
- Auto-delete messages with known spam keywords

