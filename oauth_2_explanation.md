# OAuth 2.0 – How It Works, Why It Exists, and What You Need to Use It

This document explains OAuth 2.0 in clear, practical terms for technical reference and implementation notes. It covers concepts, flows, terminology, tokens, and what information is required to use OAuth 2.0 in an application.

---

## 1. What Is OAuth 2.0?
OAuth 2.0 is an **authorization framework** that allows an application ("client") to access protected resources on behalf of a user, *without* requiring the user’s password.

OAuth 2.0 provides:
- A secure way for users to grant limited access to their data.
- A token-based mechanism instead of password sharing.
- A standardized method used by Google, Microsoft, Facebook, GitHub, and most modern APIs.

**Important:** OAuth = authorization, *not authentication*. (Authentication is typically added using OpenID Connect.)

---

## 2. Essential Roles in OAuth 2.0

### **1. Resource Owner (User)**
The person who owns the data and grants permission.

### **2. Client (Your App)**
The application requesting access to the user’s data.

### **3. Authorization Server**
The system that verifies identity and issues tokens.
Example: login.microsoftonline.com, accounts.google.com.

### **4. Resource Server (API)**
Where the user’s protected data lives.
Example: Microsoft Graph, Google Drive API.

---

## 3. The OAuth 2.0 Tokens
OAuth relies on tokens instead of passwords.

### **1. Access Token**
- Short-lived (minutes to hours)
- Sent with API requests
- Grants access to specific scopes

### **2. Refresh Token**
- Long-lived (days to months)
- Used to obtain new access tokens without re-authenticating
- Should be stored securely

### **3. ID Token** *(only in OIDC)*
- A JWT containing user identity info
- Used for authentication

---

## 4. The Most Common OAuth 2.0 Flows
Different application types use different OAuth flows.

### **1. Authorization Code Flow (most common, safest)**
Used for:
- Web apps
- Native mobile apps

**Steps:**
1. Client sends user to Authorization Server.
2. User logs in and approves access.
3. Server sends back a one-time **authorization code**.
4. Client exchanges the code for:
   - Access token
   - Refresh token
5. Client uses access token to call APIs.

**Why it’s secure:** The token is never exposed in the browser; the exchange happens server-to-server.

### **2. Client Credentials Flow**
Used for:
- Server-to-server communication
- No user involved

The client uses its **client_id** and **client_secret** to obtain a token.

### **3. Device Code Flow**
Used for:
- TVs, IoT, CLI tools (no browser access)

Shows user a code to enter on a separate device.

### **4. Implicit Flow (obsolete)**
Used historically for SPAs; no longer recommended due to security weaknesses.

---

## 5. What You Need to Use OAuth 2.0
To integrate OAuth with any provider (Google, Microsoft, GitHub), you need the following.

### **1. Client ID**
Public identifier for your application.

### **2. Client Secret**
Private key used for secure token exchanges.
(Should NEVER be included in front-end JavaScript or mobile apps.)

### **3. Redirect URI(s)**
The callback destination where the authorization server sends the authorization code after login.

### **4. Scopes**
Permissions your app is requesting.
Examples:
- `openid`
- `email`
- `profile`
- `User.Read`
- `Files.ReadWrite`

### **5. Authorization Server Endpoints**
Every OAuth provider exposes URLs for:

- Authorization endpoint  
  Example: `/oauth2/v2.0/authorize`

- Token endpoint  
  Example: `/oauth2/v2.0/token`

- (Optional) UserInfo endpoint  
  Example: `/userinfo`

### **6. Token Format (commonly JWT)**
You may need to parse or validate JWTs.

---

## 6. Example Authorization Code Flow (Step-by-Step)

### **Step 1 — Redirect User to Auth Server**
```
GET https://provider.com/authorize?
  client_id=YOUR_CLIENT_ID
  &response_type=code
  &redirect_uri=https://yourapp.com/callback
  &scope=openid+profile+email
  &state=xyz123
```

### **Step 2 — User Logs In**
User authenticates and grants permission.

### **Step 3 — Provider Sends Authorization Code**
```
https://yourapp.com/callback?code=ABCD1234&state=xyz123
```

### **Step 4 — App Exchanges Code for Tokens**
```
POST https://provider.com/token
  grant_type=authorization_code
  code=ABCD1234
  redirect_uri=https://yourapp.com/callback
  client_id=YOUR_CLIENT_ID
  client_secret=YOUR_CLIENT_SECRET
```

### **Step 5 — Provider Returns Tokens**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "id_token": "...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### **Step 6 — App Calls API with Access Token**
```
GET /me
Authorization: Bearer ACCESS_TOKEN_HERE
```

---

## 7. Security Best Practices
- Always use HTTPS.
- Never expose client secrets in front-end code.
- Use PKCE for mobile and SPA apps.
- Validate `state` values to prevent CSRF.
- Store refresh tokens securely (encrypted storage).
- Rotate and expire tokens regularly.
- Validate JWT signatures from authorization server.

---

## 8. Common OAuth Misunderstandings
- **OAuth is NOT authentication.**  
  It only handles authorization.
- **ID Tokens require OpenID Connect.**  
  OAuth alone does not return user identity.
- **Access tokens do not guarantee identity.**  
  They simply prove authorization.

---

## 9. Summary
OAuth 2.0 is a secure, flexible authorization framework using tokens to access APIs without sharing user passwords. To use it, you need:
- Client ID & secret
- Redirect URLs
- Scopes
- Authorization + token endpoints
- Token validation logic

It is the foundation of nearly all modern authentication and API access systems.

If you want a second document explaining **OpenID Connect (OIDC)**—the layer that adds authentication and user identity—I can generate that as well.

