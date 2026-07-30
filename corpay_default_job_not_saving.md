#corpay [[Corpay]]
# 🧰 Help Desk: Corpay Default Job Not Saving

## 🧾 Issue Description
Users report that they are **unable to save a default job** on the Corpay website:
- A notification appears acknowledging the save.
- The job disappears immediately afterward.
- The setting does **not persist**.

---

## 🧑‍💻 Environment
- Platform: Corpay Web Application
- Role: Help Desk Support
- Reported by: End users
- Behavior is browser-based and inconsistent

---

## 🛠 Troubleshooting Steps

### 1. ✅ Browser Compatibility
- Try saving using a different browser (Chrome, Edge, Firefox).
- Confirm browser is up to date.

### 2. 🧹 Clear Cache and Cookies
- Clear cookies and cache specific to `corpay.com`.
- Restart browser and attempt to save again.

### 3. 🔌 Disable Browser Extensions
- Especially any:
  - Ad blockers
  - Privacy filters (e.g. DuckDuckGo, Ghostery)
  - Script blockers (e.g. NoScript)
- Test with extensions disabled.

### 4. 🕵️‍♂️ Use Incognito/Private Mode
- Launch an incognito session.
- Attempt the save again — if successful, issue is likely local to user browser profile.

### 5. 🧪 Check JavaScript Console
- Open Dev Tools (`F12` or right-click → Inspect → Console tab).
- Watch for red error messages after clicking "Save".
- Log or screenshot errors for support escalation.

### 6. 🧾 Validate Form Completeness
- Ensure all required or dependent fields are filled.
- Re-enter job details instead of re-using prefilled fields.

### 7. 🔄 Backend/API Errors (Possibility)
- The UI may display a false positive success if the backend save fails.
- Request user to try saving again after logging out and logging in.

---

## 📨 What to Collect for Escalation
If the issue persists, collect the following:
- Browser and version
- Screenshot or screen recording of the behavior
- JavaScript console errors
- Date/time of the attempt
- Job ID/name attempted to be saved

---

## 🔗 External Resources
_(No direct support link available — add if/when Corpay publishes public documentation)_

---

## 🏷 Tags
#corpay #webapp #helpdesk #troubleshooting #defaultjob #support #software 
