
## The cast of characters (fixed in your head first)

- **You**: sitting at a Windows 11 machine
    
- **Windows Hello**: your local authenticator (PIN / fingerprint / face)
    
- **TPM**: hardware chip protecting keys
    
- **Azure AD (Entra ID)**: identity provider
    
- **OIDC**: the protocol Azure AD uses to talk to apps
    
- **Your app**: a web app, internal tool, or cloud service
    

Nothing else. No magic.

---

## Phase 0: One-time setup (this already happened)

Before the login you’re about to perform, these things are true:

### On your device

- Windows generated a **public/private key pair**
    
- Private key is:
    
    - stored in TPM
        
    - non-exportable
        
- Public key is registered with Azure AD
    
- Windows Hello is bound to _you + this device_
    

### In Azure AD

- Azure AD has:
    
    - your user object
        
    - your device object
        
    - your public key
        
- Conditional Access policies exist (maybe):
    
    - MFA required?
        
    - compliant device?
        
    - location risk?
        

This setup step is why Windows Hello is fast later.

---

## Phase 1: You try to access an app

Example:  
You open a browser and go to:

`https://internal-app.company.com`

The app says:

> “I don’t know who you are.”

So it redirects you to Azure AD:

`https://login.microsoftonline.com/...`

This redirect includes:

- client_id (who the app is)
    
- redirect_uri
    
- scopes
    
- response_type=code
    
- state + nonce
    

This is **OIDC Authorization Code Flow** starting.

---

## Phase 2: Azure AD decides how you must authenticate

Azure AD now evaluates **policy**, not credentials.

It checks:

- Are you already signed in?
    
- Is your device trusted?
    
- Is MFA required?
    
- Is passwordless allowed?
    
- Risk signals?
    

Azure AD decides:

> “Windows Hello is acceptable.”

Important point:  
**OIDC does not care how you authenticate**  
Azure AD does.

---

## Phase 3: Windows Hello is invoked (local, not cloud)

Now something subtle but critical happens.

Your browser hands control to **Windows**.

You see:

- PIN prompt  
    or
    
- fingerprint scan  
    or
    
- face recognition
    

This step:

- does NOT send biometrics anywhere
    
- does NOT talk to Azure AD yet
    

What Windows Hello is doing:

> “Prove to _me_ that you are the authorized human allowed to use this private key.”

---

## Phase 4: Cryptographic proof (the heart of FIDO2)

Azure AD sends a **challenge** (random data).

Windows:

1. Unlocks the private key (after PIN/biometric)
    
2. Signs the challenge using the private key
    
3. Sends the signature back
    

Azure AD:

- Looks up your stored public key
    
- Verifies the signature
    
- Confirms:
    
    - correct user
        
    - correct device
        
    - correct domain
        
    - correct challenge
        

No password ever existed.

This is **FIDO2 authentication**.

---

## Phase 5: Azure AD now trusts the authentication

At this moment, Azure AD says:

> “This user successfully authenticated using a phishing-resistant method.”

Now it moves _up the stack_.

Authentication is done.  
Now comes **identity issuance**.

---

## Phase 6: Azure AD issues OIDC tokens

Azure AD creates:

### 1. ID Token (OIDC)

This answers:

> “Who is this?”

It contains claims like:

- `sub` (user ID)
    
- `name`
    
- `email`
    
- `tid` (tenant)
    
- `amr` (authentication method reference)
    
    - shows `pwd`, `fido`, `mfa`, etc
        
- `auth_time`
    

Signed by Azure AD.

### 2. Authorization Code

This is short-lived and sent back to the app.

The browser is redirected to:

`https://internal-app.company.com/callback?code=XYZ`

---

## Phase 7: App exchanges code for tokens

Your app backend:

- sends the code to Azure AD
    
- authenticates itself (client secret / cert)
    
- requests tokens
    

Azure AD responds with:

- **Access Token** (OAuth)
    
- **ID Token** (OIDC)
    
- optional **Refresh Token**
    

At no point did the app see:

- your password
    
- your biometrics
    
- your private key
    

---

## Phase 8: App trusts the tokens, not the login

The app:

- validates token signature
    
- checks issuer
    
- checks audience
    
- checks expiration
    

Then it says:

> “Azure AD vouches for this identity.”

Now authorization happens:

- roles
    
- group membership
    
- scopes
    

The app decides:

- what you can see
    
- what actions you can take
    

---

## Phase 9: Accessing APIs (OAuth side)

When the app calls an API:

- it presents the **access token**
    
- API validates it
    
- API enforces scopes/roles
    

OIDC stops here. OAuth continues.

---

## End-to-end summary in one clean chain

`You → Windows Hello (local auth)      → TPM signs challenge      → Azure AD verifies key      → Azure AD issues ID Token (OIDC)      → App trusts token      → API trusts access token`

---

## Why this is so powerful

- No shared secrets
    
- No password database
    
- No phishing
    
- No replay attacks
    
- Device-bound trust
    
- Policy-driven authentication
    

This is why Microsoft pushes:

- Windows Hello
    
- FIDO2 keys
    
- Passwordless tenants
    

---

## The single most important insight

> **Windows Hello does not authenticate you to the app.  
> It authenticates you to Azure AD.  
> OIDC is how Azure AD tells the app who you are.**

Once that clicks, the whole stack makes sense.

---

## Where this maps to your future work

This exact pattern shows up in:

- Azure Managed Identity (machines instead of humans)
    
- Service principals
    
- Secure agent authorization
    
- Zero Trust API design
    

Same idea. Different actor.