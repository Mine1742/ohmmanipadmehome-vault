[[Accubid Hub]]
# Unable to Access Client Copy of Report in Accubid Classic (CO 16)

## Common Causes and Solutions

| Possible Cause                        | Resolution                                                                                                                                             |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Missing Report Template               | Go to **Reports → Report Setup → Client Copy**, and check if the report template is assigned. Reconfigure report templates if needed.                  |
| File Permission Issues                | Check NTFS permissions for the folder where Accubid stores its reports (commonly on a shared network drive or `C:\Accubid`). Ensure read/write access. |
| Report Path Misconfiguration          | Under **System Options → File Paths**, verify that the path for **Client Reports** is correct and accessible.                                          |
| Accubid Database Corruption           | Run **Accubid Database Utilities** and check for corruption or missing records relating to report settings.                                            |
| Accubid Running in Compatibility Mode | Right-click Accubid shortcut → Properties → Compatibility → Uncheck compatibility settings.                                                            |
| Network Drive Mapping Issues          | Ensure any mapped network drives for report storage are properly connected and accessible.                                                             |
| Accubid User Profile Issue            | Try logging in with a different Accubid user profile to see if the issue is user-specific.                                                             |

---

## Quick Troubleshooting Checklist

- ✅ Can you run **other reports**?
- ✅ Is this happening to **all users** or just one?
- ✅ Is the report **local or network-stored**?
- ✅ Any recent changes to **file paths, permissions, or Accubid version**?
- ✅ Try running Accubid as **Administrator**.

---

## Advanced Step: Rebuild Report Paths

1. Open **Accubid → File → System Options → File Paths**
2. Verify the **Reports Directory** path
3. If incorrect, browse to the correct folder (example: `\\ServerName\Accubid\Reports`)

---

## If All Else Fails

- Reinstall the report files from a backup or installation media.
- Contact **Trimble Accubid support** for further assistance.

---
