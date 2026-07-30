# Microsoft Teams Calls Not Ringing – Troubleshooting Guide

## Overview
If incoming calls in Microsoft Teams do not always ring and you only receive a missed call notification, this may be caused by notification settings, Focus Assist/Do Not Disturb, background app behavior, or device configuration.

---

## 1. Check Teams Notification Settings
1. In Teams, click your **profile picture** → **Settings**.
2. Navigate to **Notifications**.
3. Under **Meetings & Calls**:
   - Set **Calls** to **Banner and ring** (not just Banner).
   - Ensure **Ringtone** is enabled and volume is up.
4. Under **Appearance and sound**, check **Play sound for incoming calls and notifications**.

**Reference:** [Manage notifications in Teams](https://support.microsoft.com/en-us/office/manage-notifications-in-teams-2f3e1fd2-5d8f-4b44-b4ef-9f97b1bda992)

---

## 2. Verify Call Answering Rules
1. Go to **Settings → Calls** in Teams.
2. Ensure **Call answering rules** is set to **Ring me**.
3. Check the **If unanswered** setting — ensure it’s not immediately forwarding to voicemail.

**Reference:** [Set your call answering rules in Teams](https://support.microsoft.com/en-us/office/set-call-answering-rules-in-teams-ecfdc74f-142e-4b8f-a69d-26b87a761397)

---

## 3. Check Focus Assist / Do Not Disturb
### In Windows:
1. Press `Windows key + A` to open Quick Settings.
2. Ensure **Focus Assist** is **Off**.
3. If using Focus Assist rules, add Teams to the **Priority list** under `Settings → System → Focus Assist`.

### In Teams:
- Ensure your status is not **Do Not Disturb** — this suppresses ringing.

**Reference:** [Use Focus assist in Windows](https://support.microsoft.com/en-us/windows/use-focus-assist-to-avoid-distractions-7b735c92-9bfa-99a1-2ee9-df3d7d2c38f3)

---

## 4. Keep Teams Running in the Background
- In Teams, go to **Settings → General** and enable **On close, keep the application running**.
- Restart Teams periodically to avoid stale background processes.

---

## 5. Verify Audio Device and Permissions
- In **Settings → Devices**, select the correct speakers/headset for call alerts.
- In Windows `Settings → Privacy & security → Microphone`, ensure Teams has microphone permission.

---

## 6. Mobile App Considerations
If using Teams on mobile:
- Enable Teams notifications in your phone’s system settings.
- Disable **Battery Optimization** for Teams to allow it to stay active in the background.

**Reference:** [Teams mobile notifications](https://support.microsoft.com/en-us/office/manage-notifications-in-teams-2f3e1fd2-5d8f-4b44-b4ef-9f97b1bda992)

---

## 7. Advanced – Check Calling Policy
If an organizational policy is restricting private calls, you can check with PowerShell:

```powershell
# Connect to Teams PowerShell
Connect-MicrosoftTeams

# Check Global calling policy
Get-CsTeamsCallingPolicy -Identity Global
```

Verify **AllowPrivateCalling** is set to `True`.

---

## Internal Tags
#teams #notifications #calls #kb #troubleshooting #focusassist #microsoft365
