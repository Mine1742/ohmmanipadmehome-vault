
# #Phish_Alert_Button - Valid Authentication Token Error

**Error Message:**
```
Error
Your mail server needs a valid authentication token for the Phish Alert Button. If you need assistance with your mail server settings, please contact your admin.
```

---

## 🔎 Overview
This error typically occurs when the Outlook add-in (Phish Alert Button) cannot obtain a valid Exchange Web Services (EWS) / Single Sign-On (SSO) callback token from the user's mailbox. This can be due to identity conflicts, add-in deployment scope, missing WebView2, or Exchange/EWS restrictions.

---

## ✅ Quick Triage Steps

1. **Test in Outlook on the Web (OWA)**  
   - If **works in OWA** but not desktop → client issue (identity/cache/WebView2).  
   - If **fails in both** → server/tenant configuration.

2. **Check Office account sign-in**  
   - In Outlook: `File → Office Account` → ensure only the correct work account is signed in.  
   - Remove personal or other work accounts → restart Outlook.

3. **Clear Office web add-in cache**  
   - Close Outlook.  
   - Delete all contents from:  
     ```
     %LOCALAPPDATA%\Microsoft\Office\16.0\Wef\
     ```
   - Reopen Outlook and test.

4. **Repair or install WebView2 Runtime**  
   - `Settings → Apps & Features → Microsoft Edge WebView2 Runtime` → Repair.  
   - If missing, [download and install](https://developer.microsoft.com/microsoft-edge/webview2/#download-section).

5. **Verify add-in deployment scope**  
   - Microsoft 365 Admin Center → `Settings → Integrated apps` → locate Phish Alert Button.  
   - Ensure the user (or their group) is in the deployment scope → re-save.

---

## 🖥️ If Failing in OWA Too (Server/Tenant Checks)

6. **Verify EWS is enabled for the mailbox**  
   ```powershell
   Get-CASMailbox user@domain.com | fl EwsEnabled
   Set-CASMailbox user@domain.com -EwsEnabled:$true   # if disabled
   ```

7. **Check org-wide EWS restrictions**  
   ```powershell
   Get-OrganizationConfig | fl EwsApplicationAccessPolicy,EwsAllowList,EwsBlockList
   ```
   - If an `EwsAllowList` is in place, ensure required Outlook web add-in identifiers are included.

8. **Hybrid/on-prem Exchange?**  
   - Confirm OAuth between Exchange and Microsoft 365 is healthy.  
   - Verify EWS virtual directory URL & certificate validity.  
   - Ensure the latest CU is installed.

9. **Conditional Access Policies**  
   - Review CA targeting Exchange/SharePoint that might block legacy auth/EWS or require compliant devices.  
   - Temporarily exclude the user to test.

---

## 💡 Additional Fixes That Often Work
- Re-deploy the add-in to the affected user (remove → re-add in Integrated Apps).  
- If using **new Outlook for Windows**, confirm the **web add-in** flavor of PAB is deployed (COM add-ins don’t run in new Outlook).  
- If testing from a **shared mailbox**, try from the **primary mailbox** instead (token acquisition can fail in shared mailboxes).

---

## 📎 Reference Links
- Microsoft Learn — [Manage integrated apps in the Microsoft 365 admin center](https://learn.microsoft.com/microsoft-365/admin/manage/manage-integrated-apps)  
- Microsoft Learn — [Exchange Online PowerShell V3 module](https://learn.microsoft.com/powershell/exchange/exchange-online-powershell-v2)  
- Microsoft Edge — [WebView2 Runtime download](https://developer.microsoft.com/microsoft-edge/webview2/#download-section)  
- KnowBe4 Support — [Phish Alert Button (PAB) Installation and Troubleshooting](https://support.knowbe4.com/hc/en-us/articles/115001298207-Phish-Alert-Button-PAB-Installation)

---

## 🏷️ Internal Tags
#Outlook #Troubleshooting #PhishAlert #AddIn #EWS #PowerShell #HelpDesk

