[[Outlook Hub]] [[Email Access]]  
# Shared Mailbox – Email Status Not Updating Across Users

## 🧾 Problem

In a shared mailbox (e.g., "payroll@..."), when one user moves or reads an email:
- Other users **don’t see that change**.
- This results in **duplicate work** or missed coordination.

## 🔍 Root Causes

### 1. **Mailbox Access as Separate Account vs. Delegate**
- If added as an **additional mailbox** vs. **full access account**, syncing behavior varies.

### 2. **Cached Exchange Mode**
- Outlook in Cached Mode may **not sync changes immediately**.
- Especially true for shared mailboxes, which can be cached separately.

### 3. **View Settings and Filters**
- Users might have **custom views**, making emails look unread or unmoved.
- "Show as Conversations" or sorting settings can hide updates.

### 4. **Delay in Server Sync**
- Outlook may not push/receive changes in real-time, especially for shared mailboxes.

---

## ✅ Solutions

### ✅ 1. Add Mailbox as a Full Profile (Best Practice)
- Instead of adding the shared mailbox under your main account:
  - Go to `Control Panel > Mail > Profiles`
  - Create a new Outlook profile.
  - Add the **shared mailbox directly** as the primary account.
- This ensures all actions reflect immediately for everyone.

### ✅ 2. Turn Off Cached Mode for Shared Mailboxes
1. In Outlook:  
   `File > Account Settings > Account Settings`
2. Select your account > Click **Change**.
3. Uncheck **"Download shared folders"**.
4. Restart Outlook.

> This forces real-time syncing with the Exchange server.

### ✅ 3. Establish Clear Email Workflow (Tagging/Folders)
- Use folders like:
  - `To Do`
  - `In Progress`
  - `Completed`
- Or use categories/flags (if consistent across all users).

### ✅ 4. Use Microsoft 365 Shared Mailbox Tracking Tools
- Consider **Microsoft 365 Compliance Center** or audit logs to track message activity.
- Integrate **Power Automate** for alerts or task tracking.

---

## 📝 Best Practices for Shared Mailboxes

| Tip | Description |
|-----|-------------|
| 🧑‍🤝‍🧑 Full Access | Assign full access and send-as permissions |
| 🚫 No Cached Mode | Avoid caching for shared folders |
| 🗂 Folder Organization | Use agreed folders to show progress |
| 🏷 Consistent Categories | Agree on category colors/tags |
| 🔁 Frequent Sync | Remind users to refresh folders if needed |
| 📋 Document Rules | Document handling procedures to reduce overlap |

---

## 🧰 Optional: Power Automate Tracker

Set up a Power Automate flow to:
- Move flagged emails to a “Handled” folder.
- Alert a Teams channel when a folder is modified.
