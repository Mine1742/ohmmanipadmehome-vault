---

title: "Troubleshooting Old Emails Being Resent" date: 2025-08-06 tags:

- troubleshooting
- outlook
- exchange
- email

---

# Troubleshooting: Old Emails Being Resent

**Issue:** A user reports that Outlook is resending emails from 3–4 months ago. The resent messages don’t appear in the Sent folder and the user cannot see which items are being sent.

## 1. Determine the Affected Client(s)

- Ask the user which mail client(s) exhibit the behavior: Outlook desktop, Outlook on the web (OWA), mobile app, etc.
- **Why this matters:** If only one client is affected, the issue is likely local to that client (e.g., a stuck Outbox or add-in) rather than server-side.

## 2. Use Message Trace to Validate Resends

1. **Exchange Online:** Navigate to the Security & Compliance Center → Mail flow → Message trace.
2. **On‑Prem Exchange:** Run in Exchange Management Shell:
   ```powershell
   Get-MessageTrace -SenderAddress user@domain.com -StartDate 2025-08-06 -EndDate 2025-08-07
   ```
3. Look for messages with an `OriginalClientSubmissionTime` from 3–4 months ago to confirm delayed delivery or queueing.

## 3. Inspect Local Queues and Hidden Folders

- In Outlook desktop, enable **Folder List** (View → Folder Pane → Folder List).
- Check **Outbox**, **Sync Issues**, and **Local Failures**.
- If nothing appears, use [MFCMAPI](https://github.com/stephenegriffin/mfcmapi) to open the mailbox and inspect hidden items in the Outbox.

## 4. Review Rules and Delayed-Delivery Settings

1. In Outlook, go to **File → Manage Rules & Alerts**.
2. Look for any rule that delays delivery or forwards messages based on age.
3. In Exchange Admin Center, check for any transport rules affecting message delivery timing.

## 5. Check for Unauthorized or Rogue Clients

- Reset the user’s password to break any stuck sessions.
- In Azure AD (Entra), review **Sign‑in logs** for unusual client apps or IP addresses.

## 6. Rebuild the Local Outlook Data File

1. **Close Outlook.**
2. Rename or delete the `.ost` file (typically located in `%localappdata%\Microsoft\Outlook`).
3. Reopen Outlook to force a full resync, clearing any stuck local queue.

## 7. Validate the Fix

- Send test emails and monitor the Outbox.
- Run a follow-up Message Trace to ensure no old items are sent.

---

## External Links

- [Use Message Trace in Exchange Online](https://docs.microsoft.com/exchange/security-and-compliance/message-trace)
- [MFCMAPI GitHub Repository](https://github.com/stephenegriffin/mfcmapi)
- [Configure Transport Delivery Delays](https://docs.microsoft.com/exchange/mail-flow/transport-delivery-delays)

## Internal Tags

`#troubleshooting` `#outlook` `#exchange` `#email`

