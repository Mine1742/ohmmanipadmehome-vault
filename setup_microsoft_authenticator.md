# 🚀 Microsoft Authenticator – New‑User Setup Guide

*Created 2025-07-25*

---

## 1  Prerequisites

| Requirement | Why it matters |
|-------------|----------------|
| Smartphone (iOS 15 + / Android 8 +) | Authenticator runs only on supported OS versions. |
| Reliable Wi‑Fi or mobile data | Needed to pull the QR code and complete the first sign‑in. |
| Work username + password | You’ll sign in once during setup. |

---

## 2  Download the App

| Platform | Steps |
|----------|-------|
| **Android** | 1️⃣ Open **Google Play Store** → search **“Microsoft Authenticator.”**  2️⃣ Tap **Install**. |
| **iPhone** | 1️⃣ Open **App Store** → search **“Microsoft Authenticator.”**  2️⃣ Tap **Get → Install** (Face ID / Apple ID may prompt). |

Look for a blue padlock inside a white keyhole on a blue background.

---

## 3  Add Your Work (Azure AD / M365) Account

1. **Open** the Authenticator app.  
2. **Allow notifications** when prompted.  
3. Tap **➕ Add account** → **Work or school account** → **Scan QR code**.  
4. On your computer go to **<https://aka.ms/mfasetup>** (or follow the “More information required” prompt).  
5. Click **“Add sign‑in method” → Authenticator app → Next → QR code**.  
6. Point the phone’s camera at the QR code.  
7. Approve the test notification on your phone.  
8. Authenticator now shows a **6‑digit code** for your account.

> **Camera blocked?** Choose **“Can’t scan?”** and enter the **App ID** and **Code** manually.

---

## 4  Verify & Finish

1. The web page should show **“Notification approved.”**  
2. Click **Done**.  
3. *(Recommended)* In the app, tap the account → enable **Cloud backup** (OneDrive / iCloud).

---

## 5  Everyday Usage

* **Push approval** – Tap **Approve**, enter number‑match if required.  
* **Offline code** – Tap the account to reveal the 6‑digit OTP (valid 30 s).  
* **Multiple tenants** – Repeat **Add account → Work or school** for each org.

---

## 🩹 Common First‑Time Hiccups

| Symptom | Fix |
|---------|-----|
| QR won’t scan | Check camera permission in phone settings. |
| “Account already exists” | Delete the old entry in Authenticator, then re‑add. |
| No push notification | Ensure **Do Not Disturb** is off and notifications are allowed. |
| Still asked for text codes | In **My Sign‑ins** set **Microsoft Authenticator – notification** as **default**. |

---

## 🔐 Admin Quick‑Check

1. **Entra ID** → **Users** → select user → **Authentication methods** – confirm **Microsoft Authenticator** is listed.  
2. Verify your MFA policy allows **Push + OTP** for the user.

---

### External Links

* Microsoft MFA Setup Portal → <https://aka.ms/mfasetup>  
* Authenticator iOS FAQ → <https://support.microsoft.com/account-billing/microsoft-authenticator-app-faq>  
* Authenticator Android FAQ → <https://support.microsoft.com/account-billing/what-is-microsoft-authenticator>  

---

### Tags  
#authenticator #mfa #setup #helpdesk #microsoft365
