# Outlook App Protection – IT Call Checklist  

**User:** Davis Holt  
**Purpose:** Quick reference checklist for IT while assisting user.  

---

## Initial Checks  
- [ ] Confirm device has stable Wi-Fi or cellular internet.  
- [ ] Verify Outlook app is up to date.  
- [ ] Confirm user is entering the correct six-digit Enterprise App Protection PIN.  

## Step 1 – Restart and Cache  
- [ ] Ask user to force close Outlook app.  
- [ ] If Android: clear app cache (*Settings > Apps > Outlook > Storage > Clear Cache*).  
- [ ] If iOS: skip to reinstall step.  

## Step 2 – Reinstall Outlook  
- [ ] Uninstall Outlook app.  
- [ ] Reinstall from App Store (iOS) or Google Play (Android).  
- [ ] Launch Outlook and attempt login again.  

## Step 3 – Verify Authenticator & Company Portal  
- [ ] Confirm Microsoft Authenticator is installed and account is present.  
- [ ] Open Company Portal → *Settings → Sync*.  
- [ ] If needed, remove and re-enroll device in Intune.  

## Step 4 – Reset App PIN  
- [ ] In Outlook, go to *Profile → Settings → Reset PIN*.  
- [ ] If option unavailable, reinstall will prompt for a new PIN.  

## Escalation  
- [ ] If Outlook still hangs on spinning wheel:  
   - Remove work account and re-add in Outlook.  
   - Confirm Intune device compliance.  
   - Escalate to Intune admin for app protection logs if unresolved.  

---

#tags/Outlook #tags/Mobile #tags/Intune #tags/Checklist
