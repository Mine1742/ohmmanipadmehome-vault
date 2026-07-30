#accubid 

Accubid Classic Settings not Saving

SCENARIO: You set the path to database, jobdata, or codata folder, but Accubid reverts it back to the default path.

Need to give full Classic registry Permissions
Start > Run (or Windows + R)
 
Type in "regedit".

Navigate to the following registry key: HKEY_CURRENT_USER\Software\Accubid
Right-click on “Accubid” and select “Permissions”.
(OR MAYBE: Need to sign in to your advisor account and do the steps, but instead of this HKEY_CURRENT_USER\Software\Accubid ... go here HKEY_USERS and search the user with Accubid on it)
 
If there are no groups or user names listed, you will need to click on “Add” to add users.
 
Enter object name “Everyone” and click on “Check Names”, then click OK.
 
Make sure “Everyone” is selected and at the bottom, check mark “Full Control” under Allow. Then, Apply.
 
Notice how more users are added to this list. Last step is to click on “Advanced”.
 
Uncheck “Include inheritable permissions from this object’s parent”, then click on “Add”.
 
Click "Add".
 
Check “Replace all child object permissions with inheritable permissions from this object” then click Apply and OK.
 
Click on “Yes” to continue, and “OK” to complete.
 
Check the sub-keys under Accubid for permissions, and they should be identical to the Accubid parent key.

If you switched domains recently or went from Workgroups to a domain and Accubid was installed before either of those moves, this may only be part of the fix. It scenarios like that, we see that not all the sub registry folders will allow you to apply permissions. In those cases, it is likely due the owner of those folders. Perhaps the owner is the login that was used before the switching to a domain. In any case, if the guide above does not work, I would start checking the owner of the sub folders that it will not allow you to provide permissions too.

Some users uninstall Accubid, then create new Windows profiles, then reinstall Accubid in the new profile. This can help with this issue as well, though this can take a good amount of work. Hopefully it does not come that far.
