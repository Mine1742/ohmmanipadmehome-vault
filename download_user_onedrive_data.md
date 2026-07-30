---

## title: Download a User’s OneDrive Data date: 2025-08-01 tags: [#OneDrive, #O365Admin, #KB]

# Overview

This guide explains how to download the contents of a user’s OneDrive for Business as an Office 365 administrator using three different methods.

## Method 1: SharePoint Admin Center

1. Sign in to the **Microsoft 365 admin center** at [https://admin.microsoft.com](https://admin.microsoft.com).
2. In the left navigation, select **SharePoint** under **Admin centers**.
3. In the SharePoint admin center, click **OneDrive** in the left pane.
4. Find the target user and click the vertical ellipsis (…) next to their name, then select **Create link to files**.
5. Copy the generated link and paste it into a browser to access the user’s OneDrive site.
6. Go to **Documents**, select the files/folders to download, then click **Download**.

## Method 2: eDiscovery Content Search

1. Open the **Microsoft Purview compliance portal** at [https://compliance.microsoft.com](https://compliance.microsoft.com).
2. Navigate to **Solutions → Content search**.
3. Click **New search**, name it (e.g., *Export OneDrive for *[*jdoe@contoso.com*](mailto\:jdoe@contoso.com)), and click **Next**.
4. Under **Locations**, select **Specific locations**, choose **OneDrive accounts**, and add the user.
5. Apply filters if needed, then click **Submit** to run the search.
6. Once complete, select the search result and click **Export results**.
7. Use the **eDiscovery Export Tool** to download the package, which includes the user’s files and folder structure.

## Method 3: PowerShell (SharePoint Online Management Shell)

1. Install and launch the **SharePoint Online Management Shell**.
2. Connect to your tenant:
   ```powershell
   Connect-SPOService -Url https://<yourTenant>-admin.sharepoint.com
   ```
3. Retrieve the user’s OneDrive site URL:
   ```powershell
   $userSite = Get-SPOSite -IncludePersonalSite $true \
     | Where-Object { $_.Owner -eq "jdoe@contoso.com" }
   ```
4. Grant yourself site collection admin rights:
   ```powershell
   Set-SPOUser -Site $userSite.Url \
     -LoginName "admin@contoso.com" -IsSiteCollectionAdmin $true
   ```
5. Open the OneDrive URL in your browser, navigate to **Documents**, and download the data.

## References

- [Manage user profiles in SharePoint Online](https://learn.microsoft.com/sharepoint/manage-user-profiles)
- [Content search in Microsoft Purview](https://learn.microsoft.com/microsoft-365/compliance/content-search)
- [SharePoint Online Management Shell Cmdlets](https://learn.microsoft.com/powershell/sharepoint/sharepoint-online/connect-sposervice)

## Internal Links

- [[OneDrive Site Permissions]]
- [[eDiscovery Exports]]

