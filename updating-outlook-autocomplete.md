# Updating Outlook Auto-Complete Suggestions

When composing a new email in Outlook, the **auto-populate (Auto-Complete) list** suggests addresses based on cached entries, not directly from your Contacts. Sometimes frequently emailed contacts may not show up or may only resolve in certain formats.

---

## 📌 Why Contacts Don’t Auto-Populate
- Outlook uses the **Auto-Complete list (nickname cache)**, not just your Contacts.
- If you’ve never sent an email to someone from this device/profile, they won’t appear.
- Corrupt or cleared cache entries can remove suggestions.
- Sometimes names only resolve in certain formats (e.g., only by last name).

---

## 🖥️ Outlook Desktop App (Windows/Mac)

### Add a Contact to Auto-Complete
1. Open a **New Email**.
2. In the **To:** field, type the person’s **full email address** manually and press **Enter**.
3. Send the message (to them or even CC them in a test email).
4. Outlook will now include the contact in future suggestions.

### Manage Auto-Complete List
1. Go to **File → Options → Mail**.
2. Scroll to **Send Messages** section.
3. Ensure **“Use Auto-Complete List to suggest names”** is checked.
4. To remove a bad suggestion:
   - Start typing the name/email in a new message.
   - Highlight the unwanted entry.
   - Press **Delete**.
5. To reset everything, click **Empty Auto-Complete List** (⚠️ removes all entries).

---

## 🌐 Outlook on the Web (OWA / Office 365)

### Add to Auto-Complete
1. Start a **New Message**.
2. Type the **full email address** into the **To:** field.
3. Send the message.
4. Outlook will remember it for future use.

### Remove or Reset Suggestions
1. Start typing in the **To:** field.
2. Hover over the incorrect suggestion.
3. Click the **X** to delete it.

---

## 🔧 Troubleshooting: Name Only Matches in Certain Formats

### Symptom
- Contact only appears if you type the **full last name**.  
- Does not resolve when typing **FirstName + LastInitial**.

### Fixes
1. **Delete and Re-Add the Cache Entry**
   - Start typing until the suggestion appears → highlight → press **Delete**.
   - Manually re-enter the full email → send one message.
   - Outlook rebuilds the cache, allowing more flexible matches.

2. **Check Contact Display Name**
   - Open the contact in **People**.
   - Verify **Full Name** and **File As** fields (e.g., `Jane Doe` not `Doe, Jane`).
   - Save and test again.

3. **Check GAL (Exchange/Office 365)**
   - If contact is in the **Global Address List**, the entry may be stored as `LastName, FirstName`.
   - Outlook will only match in that format.

4. **Force Seed by Sending**
   - Send a new email using **FirstName LastName** format.
   - Outlook often “learns” and accepts partial matches after this.

---

## 🔑 Best Practice
- Always add important people to your **Contacts (People app)** for permanent storage.
- Send them at least one message so they appear in Auto-Complete.
- Periodically clean out bad or outdated suggestions.

---

## 🔗 External References
- [Microsoft Support – Manage Auto-Complete List](https://support.microsoft.com/en-us/office/manage-suggested-recipients-in-the-to-cc-and-bcc-boxes-with-auto-complete-780ad817-82cc-4783-8617-5f16fbb73c6d)

---

## 🏷️ Tags
#Outlook #Contacts #Autocomplete #KB
