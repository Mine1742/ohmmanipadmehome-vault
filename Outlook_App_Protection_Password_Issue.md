# Outlook App Enterprise App Protection Password Issue – Spinning Wheel  

**User:** Davis Holt  
**Issue Date:** [Insert date]  

## Problem  
Davis Holt cannot access his email in the Outlook mobile app.  

- Yesterday, he set up a six-digit password for the **Enterprise App Protection Policy (Intune/Outlook PIN)**.  
- The app worked fine immediately after setup.  
- Today, when he enters the password, the screen shows a spinning wheel as if loading indefinitely.  
- User has already:  
  - Force closed the Outlook app.  
  - Restarted his phone.  
- Issue persists.  

## Environment  
- **App:** Microsoft Outlook (mobile)  
- **Device:** Smartphone (unspecified OS/version)  
- **Policy:** Intune App Protection / MAM (Mobile Application Management)  

## Likely Causes  
1. **Corrupted app cache** – Outlook sometimes hangs on the PIN entry screen due to cached authentication tokens.  
2. **Policy sync issue** – Enterprise App Protection (PIN) policy may not be syncing correctly with Intune.  
3. **Stale authentication tokens** – Microsoft Authenticator or AAD session may be out of sync.  

## Troubleshooting Steps  
1. **Confirm network connectivity** – Ensure device has a stable internet connection (Wi-Fi or cellular).  
2. **Clear app cache/data:**  
   - iOS: Delete and reinstall Outlook app.  
   - Android: Go to *Settings > Apps > Outlook > Storage > Clear Cache/Clear Data*, then relaunch.  
3. **Re-register device in Intune (if enrolled):**  
   - Open **Company Portal** → *Settings* → *Sync*.  
   - If issue persists, remove device from Intune and re-enroll.  
4. **Check Authenticator app:**  
   - Ensure Microsoft Authenticator is installed and working.  
   - Confirm account appears in Authenticator and notifications are allowed.  
5. **Reset app protection PIN:**  
   - Go to *Outlook app → Profile icon → Settings → Reset PIN* (if available).  
   - If still spinning, a full reinstall will force a new PIN setup.  
6. **Escalation:**  
   - If issue persists, IT should contact the user directly to walk through a clean reinstall and Intune re-enrollment.  

## Resolution Path  
Most cases are fixed by:  
- Clearing Outlook app data (Android) or reinstalling the app (iOS).  
- Re-registering with Company Portal to refresh Intune/MAM policies.  

## Notes for IT  
- Be prepared to walk Davis through removing and re-adding his work account in Outlook after reinstall.  
- Verify the device is compliant in Intune.  
- If issue continues, escalate to the Intune admin team to check app protection logs.  

## External References  
- [Microsoft Docs – Manage app protection policies](https://learn.microsoft.com/intune/app-protection-policy)  
- [Microsoft Support – Outlook for iOS and Android](https://support.microsoft.com/office/outlook-for-ios-and-android-help-8c3ccb8d-5320-46af-b6f6-961e7b6fd3d2)  

---

#tags/Outlook #tags/Mobile #tags/Intune #tags/Troubleshooting  
