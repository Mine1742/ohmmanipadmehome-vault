# Setting Up SharePoint for Client Large File Uploads

## Overview
This guide explains how to allow a client to securely upload large files (up to 250 GB each) to your SharePoint or OneDrive for Business environment.

---

## Option 1 – SharePoint “Request Files” (Best for One-Off Uploads)

**Purpose:** Allow clients to upload files without seeing existing content.

### Steps:
1. Go to your SharePoint Document Library.
2. Create or choose a target folder.
3. Right-click the folder and select **Request files**.
4. Add a description (e.g., "Upload project deliverables here").
5. Copy the **generated link** and send it to your client.

**Notes:**
- Clients do **not** need a Microsoft account.
- Clients can only upload, not download or see other files.

---

## Option 2 – OneDrive “Request Files”

**Purpose:** Isolated upload folder not linked directly to a SharePoint site.

### Steps:
1. Go to OneDrive for Business web interface.
2. Create a folder specifically for uploads.
3. Select the folder → **Request files** from the toolbar.
4. Provide the request link to your client.

**Notes:**
- Files go directly to your OneDrive.
- Same upload-only restriction as SharePoint Request Files.

---

## Option 3 – Client-Specific SharePoint Library (Two-Way Collaboration)

**Purpose:** Allow both upload and download for ongoing projects.

### Steps:
1. In your SharePoint site, create a **new document library** for the client.
2. Go to **Library Settings → Permissions for this document library**.
3. Select **Stop inheriting permissions**.
4. Grant the client's Microsoft account **Contribute** or **Edit** permissions.
5. Share the library link.

**Notes:**
- Client must have a Microsoft account.
- Ideal for ongoing file exchanges.

---

## Option 4 – Microsoft Teams Guest Access

**Purpose:** Combine chat and file sharing in one platform.

### Steps:
1. Create a **private channel** in Teams for the client.
2. Invite the client as a **guest** to your tenant.
3. Client uploads files in the channel’s **Files** tab (stored in SharePoint).

**Notes:**
- Requires guest account setup.
- Great for collaboration with messaging.

---

## File Size Limits
- SharePoint & OneDrive: **Up to 250 GB per file**.
- Supports resumable uploads.
- Works best in Edge or Chrome.

---

## External Resources
- [Microsoft Docs: Request Files in SharePoint](https://support.microsoft.com/office/request-files-in-onedrive-or-sharepoint-3c4b9c30-5316-40c5-aaa1-99ca9f9d3512)
- [Microsoft Docs: Share files and folders](https://support.microsoft.com/office/share-sharepoint-files-or-folders-1fe37332-0f9a-4719-970e-d2578da4941c)

---

## Tags
#sharepoint #onedrive #fileupload #clientportal #microsoft365 #filesharing
