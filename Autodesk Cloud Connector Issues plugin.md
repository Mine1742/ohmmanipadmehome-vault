---

## title: Revit Issues Plugin Pulling from Wrong ACC Hub date: 2026-05-11 tags: [revit, autodesk, acc, bim360, issues, troubleshooting] category: IT Support

# Revit Issues Plugin Pulling from Wrong ACC Hub

## Symptom

The Revit Issues panel (Autodesk Construction Cloud / BIM 360 built-in issue tracking) is displaying issues from the wrong account — in this case, the **AKS hub** instead of the **Contractor's hub**.

---

## Root Cause

The Issues plugin does not have an independent hub selector. It reads issues from whichever ACC hub the **active cloud model is tied to**. If the model was opened from or synced to the AKS hub, the Issues panel will reflect AKS regardless of user intent.

---

## Diagnostic Steps

### 1. Confirm Where the Model Is Hosted

Determine which hub the central model actually lives in:

- AKS ACC hub
- Contractor ACC hub

If it was opened via **Collaborate → Open from Cloud**, note which hub was selected at that time.

### 2. Check for Cross-Linked / Shared Models

If the contractor shared the model with an AKS user via ACC, Revit may be opening it through the AKS hub copy rather than the contractor's original. The Issues panel will follow wherever Revit considers "home" for that model.

### 3. Understand the Plugin Limitation

The built-in Revit Issues panel has **no hub selector**. It cannot be independently pointed at a different hub. The only way to change which hub Issues pulls from is to open the model from the correct hub directly.

---

## Resolution

### Primary Fix — Open the Model from the Contractor's Hub

1. In Revit, go to **Collaborate → Open from Cloud**
2. Switch to the **Contractor's ACC hub** (the user must be a project member on the contractor's side)
3. Open the model from there
4. The Issues panel will now pull from the contractor's project

### If the User Only Has Access to the AKS Hub Copy

The contractor needs to add the user as a **project member** on their ACC project directly. Without that access, the user cannot open the model from the contractor's hub and the Issues panel cannot be redirected.

---

## Additional Account Conflict Checks

If the correct hub still doesn't appear or auth issues persist, work through these:

|Check|Action|
|---|---|
|Revit sign-in|Top-right avatar → verify email, sign out/in if wrong|
|Autodesk Desktop Connector|System tray → Sign Out → Sign back in with correct account|
|Cached credentials|Windows Credential Manager → remove `autodesk` / `adsk` / `acc` entries|
|Browser SSO|Sign out of `accounts.autodesk.com` before re-authenticating to avoid silent wrong-account login|

---

## Notes

- This issue commonly occurs when a model is **shared cross-hub** and the recipient opens it through their own hub copy
- The Issues plugin behavior is by design — it is scoped to the cloud model's host project, not the signed-in user's preferred hub
- If both AKS and the contractor need to track issues collaboratively, the cleanest solution is to consolidate the project in one hub and grant cross-org member access