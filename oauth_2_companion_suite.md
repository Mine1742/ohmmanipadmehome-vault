# OAuth2 Companion Suite

This companion document bundles practical, developer-focused references requested: OpenID Connect (OIDC) summary, JWT deep dive, example OAuth 2.0 configurations for Azure AD / Google / GitHub, a sequence diagram (textual) of the flows, and a short implementation cheatsheet.

---

## A — OpenID Connect (OIDC) — Quick Reference

**Purpose:** OIDC is an authentication layer built on top of OAuth 2.0. It provides identity information (an ID Token) in addition to OAuth access tokens.

**Key elements:**
- **ID Token (JWT):** Contains claims about the authenticated user (sub, iss, aud, exp, iat, name, email)
- **UserInfo Endpoint:** OAuth-protected endpoint that returns normalized user profile data
- **Scopes:** `openid` is required. Others: `profile`, `email`, `phone`, `offline_access` (for refresh tokens)
- **Recommended flow for web apps:** Authorization Code Flow with PKCE for public clients

**Common use cases:**
- Single sign-on (SSO)
- Authentication for native & web apps
- Getting a verified user identity along with API access

**Minimal steps for OIDC (Authorization Code + PKCE):**
1. Client requests `response_type=code&scope=openid profile email` + PKCE challenge.
2. User authenticates at the authorization server.
3. Client exchanges code + PKCE verifier at the token endpoint.
4. Server returns `id_token` (JWT) + `access_token` (+ `refresh_token`).
5. Client validates `id_token` signature & claims.

---

## B — JWT (JSON Web Token) Deep Dive

**Structure:** 3 base64url parts separated by `.`
1. **Header** (JSON): `alg`, `typ`, sometimes `kid`
2. **Payload** (claims): standard + custom claims
3. **Signature**: HMAC or RSA/ECDSA over header+payload

**Common Claims:**
- `iss` (issuer) — who issued the token
- `sub` (subject) — user id
- `aud` (audience) — intended audience (client id, resource)
- `exp` (expiration time)
- `iat` (issued at)
- `nbf` (not before)

**Validation Checklist:**
1. Verify token is well-formed (three parts).
2. Verify signature using `kid` -> JWK endpoint (e.g., `/.well-known/jwks.json`).
3. Verify `iss` matches configured issuer.
4. Verify `aud` includes your app/client id or resource.
5. Verify `exp` is in the future and `nbf` <= now.
6. Optionally check `azp` (authorized party) for multi-audience tokens.

**Best practices:**
- Use short lifetime for access tokens (minutes).
- Use refresh tokens for long-lived sessions (rotate them).
- Use asymmetric signing (RS256) for public trustable tokens.
- Never store sensitive PII in JWT unless encrypted.

---

## C — Example OAuth 2.0 Configs

### 1) Azure AD (Microsoft Entra)
**Register App (Azure Portal)**
- Required values produced: `Application (client) ID`, `Directory (tenant) ID`, and `Client Secret` (optional for public clients).
- Set **Redirect URI** (web: `https://yourapp.com/callback`, mobile: custom scheme or `msal://`)
- Add **API permissions** (Microsoft Graph: `User.Read`, `Files.Read`)

**Endpoints (v2)**
- Authorization: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize`
- Token: `https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token`
- JWKS: `https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys`
- OIDC metadata: `https://login.microsoftonline.com/{tenant}/v2.0/.well-known/openid-configuration`

**Authorization Code (example)**
- Scope example: `openid profile offline_access User.Read` (offline_access yields refresh token)
- Token request requires `client_id`, `client_secret` (confidential client), `code`, `redirect_uri`, `grant_type=authorization_code`.

### 2) Google OAuth
**Console Setup**
- Create OAuth Client, get `client_id` and `client_secret` and configure Redirect URI.

**Endpoints**
- Authorization: `https://accounts.google.com/o/oauth2/v2/auth`
- Token: `https://oauth2.googleapis.com/token`
- JWKS: `https://www.googleapis.com/oauth2/v3/certs`
- OIDC metadata: `https://accounts.google.com/.well-known/openid-configuration`

**Scopes:** `openid email profile https://www.googleapis.com/auth/drive.readonly` etc.

### 3) GitHub OAuth
**App Registration** (GitHub Developer Settings)
- `client_id`, `client_secret`, set `Authorization callback URL`

**Endpoints**
- Authorization: `https://github.com/login/oauth/authorize`
- Token: `https://github.com/login/oauth/access_token` (returns urlencoded or JSON if requested)

**Notes:** GitHub uses `scope` like `repo`, `user:email`. For enterprise GitHub, use your enterprise domain for endpoints.

---

## D — OAuth 2.0 Sequence Diagram (Textual)

### Authorization Code Flow (w/ PKCE) — condensed
1. **Client → Auth Server (authorize)**
   - `GET /authorize?response_type=code&client_id=...&redirect_uri=...&scope=openid profile&code_challenge=...&code_challenge_method=S256&state=xyz`
2. **Auth Server ↔ User** login & consent
3. **Auth Server → Client (browser redirect)**
   - `GET /callback?code=AUTH_CODE&state=xyz`
4. **Client → Auth Server (token exchange)**
   - `POST /token` with `grant_type=authorization_code&code=AUTH_CODE&redirect_uri=&client_id=&code_verifier=...`
5. **Auth Server → Client** returns `access_token`, `id_token`, `refresh_token`
6. **Client → Resource Server** with `Authorization: Bearer ACCESS_TOKEN` to access APIs

### Client Credentials (server-to-server)
1. **Client → Auth Server** (`client_id`+`client_secret`)
2. **Auth Server → Client** `access_token`
3. **Client → Resource Server** `Bearer` token for API calls

---

## E — Implementation Cheatsheet (Developer Quick Start)

**Config values to gather**
- Client ID
- Client Secret (for confidential clients)
- Redirect URIs
- Allowed CORS origins (for SPAs)
- Authorization & Token endpoints
- Scopes required
- JWKS (for signature validation)

**Libraries & SDKs (recommended)**
- Web (Node/Express): `passport.js` (passport-azure-ad), `openid-client`
- Python: `Authlib`, `msal` (Microsoft), `google-auth`
- Java: `spring-security-oauth2-client`
- Mobile: MSAL (Microsoft), Google Sign-In SDK, AppAuth (iOS & Android)

**Security checklist**
- Use HTTPS everywhere
- Validate `state`
- Use PKCE for public clients
- Use short-lived access tokens
- Store refresh tokens securely (server-only or encrypted storage)
- Validate JWT signature & claims

**Debug tips**
- Use browser devtools network tab to capture the redirect and `code` value.
- Use Postman for token endpoint testing.
- Check provider OIDC metadata endpoint for correct URLs and supported claims.
- For JWT debugging: jwt.io (inspect payload only; verify signature using JWKs locally)

---

## F — Sample Snippets

### Verify JWT signature (Python, PyJWT + requests for JWKs)
```python
import requests, jwt
jwks = requests.get('https://accounts.google.com/.well-known/jwks.json').json()
# find key by kid and construct public key, then:
payload = jwt.decode(token, key=public_key, algorithms=['RS256'], audience=CLIENT_ID)
```

### Token request (cURL) — Authorization Code exchange
```bash
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=AUTH_CODE&redirect_uri=https://app/cb&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET" \
  https://provider.com/oauth2/v2.0/token
```

---

## G — Next Steps / References
- RFC 6749 (OAuth 2.0)
- OpenID Connect Core 1.0
- OAuth 2.0 Security Best Current Practice (RFC 8252, PKCE)
- Microsoft identity platform docs (Azure AD)
- Google Identity docs

---

If you’d like, I can:
- Export this as a downloadable PDF or markdown file.
- Generate a sequence diagram PNG (SVG) using the textual flow above.
- Produce a ready-to-run sample app (Node + Express) that implements Authorization Code + PKCE against Google or Azure.

Which output do you want next?

