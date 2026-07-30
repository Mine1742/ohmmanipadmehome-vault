[[Outlook Hub]]
# Reset Outlook to Default Settings

This guide covers how to reset Microsoft Outlook settings back to default across various platforms.

---

## 🔍 Outlook for Windows

### ⚙️ Method 1: Reset View Settings

1. Open Outlook.
2. Go to the **View** tab.
3. Click **Reset View** and confirm.

*Repeat for each folder as needed.*

---

### ⚙️ Method 2: Delete Outlook Profile (**Complete Reset**)

> Warning: This will remove accounts, settings, and local cache. Email will re-sync from the server if applicable.

1. Close Outlook.
2. Go to **Control Panel > Mail (Microsoft Outlook)**.
3. Select **Show Profiles**.
4. Select your profile (usually **"Outlook"**) and click **Remove**.
5. Reopen Outlook and create a new profile when prompted.

---

### ⚙️ Method 3: Registry Reset (**Advanced Users Only**)

1. Press **Win + R**, type `regedit`, and press Enter.
2. Navigate to:
   ```
   HKEY_CURRENT_USER\Software\Microsoft\Office\<version>\Outlook
   ```
3. Right-click the **Outlook** key and select **Delete**.
4. Restart Outlook.

---

## 🔍 Outlook on the Web (Outlook.com / Office 365)

No full reset, but you can manually reset some settings:

- **Theme & Layout:**
  - **Settings > General > Appearance > Reset to default theme/layout.**
- **Focused Inbox:**
  - **Settings > Mail > Layout > Focused Inbox.**
- **Inbox Rules, Signatures, Automatic Replies:**
  - **Settings > Mail > Rules / Compose & Reply.**

---

## 🔍 Outlook for Mac

1. Quit Outlook.
2. Navigate to **\~/Library/Preferences/**.
3. Delete the following files if present:
   - `com.microsoft.Outlook.plist`
   - `com.microsoft.office.plist`
4. Restart Outlook.

For a complete reset, remove and re-add your Outlook profile under **Preferences > Accounts**.

---

## 🔗 External References

- [Reset View in Outlook](https://support.microsoft.com/en-us/office/reset-view-in-outlook-2c3e5b4c-1a19-4d56-9f3c-c4ef7d48cf9f)
- [Recreate Outlook Profile](https://support.microsoft.com/en-us/office/create-an-outlook-profile-f544c1ba-3352-4b3b-be0b-8d42a540459d)

---

## #outlook #reset #email #troubleshooting #how-to #o365

