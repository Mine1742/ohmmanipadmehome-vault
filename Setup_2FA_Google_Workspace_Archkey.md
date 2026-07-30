---
title: "Setup 2FA for Google Workspace (@archkey.com)"
created: 2025-05-06
tags: [google-workspace, 2fa, mfa, admin-guide, security]
aliases: [Google Workspace 2FA Setup, Two-Step Verification]
---
[[Google Hub]]
# 🔐 Enforcing 2-Step Verification (2FA) for @archkey.com Google Workspace Users

This guide outlines the admin and user steps to enable and enforce **2-Step Verification (2FA)** for your Google Workspace users under the `@archkey.com` domain.

---

## 🛠️ PART 1: Admin Setup via Google Admin Console

### ✅ Steps:
1. **Login to Admin Console**  
   [https://admin.google.com](https://admin.google.com)

2. **Navigate to**:  
   `Security` → `Authentication` → `2-step verification`

3. **Enable 2-Step Verification**
   - Turn on: **"Allow users to turn on 2-step verification"**
   - Click **Save**

4. **(Optional) Enforce 2FA**
   - Click `Enforcement`
     - **Off**: Users may enable it voluntarily
     - **On**: Forces all selected users to enable 2FA
     - **Transition Period**: Give time before enforcement

5. **Apply to Specific Org Units**
   - Select the appropriate OU (e.g., IT department) before changing settings.

---

## 👤 PART 2: User Setup Instructions

Distribute these steps to end users:

1. Visit:https://myaccount.google.com/securityle.com/security](https://myaccount.google.com/security)
2. Under **"Signing in to Google"**, select **2-Step Verification**
3. Click **Get Started** and re-enter password
4. Choose your method:
   - SMS or phone call
1. Set up and verify backup options

---

## 🔧 Admin Best Practices

- Prefer **Google Prompt** or **TOTP apps** over SMS
- Encourage use of **backup codes**
- Monitor compliance via the **Admin console > Reports > Security**
- Use **context-aware access** for advanced security

---

## 📊 Optional: 2FA Status Auditing

Use the Admin SDK or third-party tools to:
- Check which users have 2FA enabled
- Send email reminders to users missing 2FA
- Export CSV reports for compliance

> For scripting/API support, consider using Google Apps Script or PowerShell via GAM.

