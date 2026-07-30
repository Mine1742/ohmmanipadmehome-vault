#onboarding


First reach out to each one individually and inform them that their machines must be a fresh install and all Windows updates must be completed prior to onboarding. If the computer is not in a fresh state, do not onboard it. Tell them to reach back out once that has been done.

Their account should be a local admin account, so you'll onboard them using their ArchKey accounts. Then you'll log them in with their ArchKey credentials.
 
Last thing you'll do is remove Admin access from their local account.

Est remote connect
computer mgt
local users and groups
check no other profiles are on computer
windows update>check for updates>install all>restart

Manual Enrollment by the User
Guide the User to Enroll:

On a Windows device:
Open Settings > Accounts > Access work or school > Connect.
Enter their Azure AD credentials and follow the prompts.
The device will be enrolled in Intune automatically if MDM is enabled for the user.

sign out user
log them in under other user

test aksadmin pw by switching user to aksadmin account

disable local account admin : net user <name> /active:no
install screenconnect







Mobile Devices (iOS/Android):
Download the Microsoft Intune Company Portal app from the app store.
Sign in with their work or school account.
Follow the app's prompts to enroll the device.


Automatic Enrollment for Windows Devices
For Windows 10/11 devices joined to Azure AD:

Configure automatic enrollment in Microsoft Endpoint Manager:

Go to Devices > Windows > Windows enrollment.
Set MDM user scope to target all users or specific groups.

Have the user join the device to Azure AD:

Open Settings > Accounts > Access work or school > Connect.
Select Join this device to Azure Active Directory.
The device will enroll automatically.



 
 remoted into the computer and had the computer join to the ArchKey domain and also confirmed computer is up to date. I had user sign in with their ArchKey account and installed Azure VPN. Confirmed AKSAdmin works and device is under user in Entra. User did not have anything to backup to the OneDrive.

remoted into the computer with a ConnectWise remote session and confirmed user did not need to backup anything as the machine is new. So, we ran windows updates along with firmware updates. After this was completed, we had the user connect to their Microsoft Entra account under the computer settings. After this we installed ConnectWise software on the computer and switched accounts. After the computer logged into their ArchKey account we switched accounts again with the admin account to confirm it works. 
We also noticed the user had local admin accounts. We reached out to Kevin Scott to confirm if we should remove them. Kevin was not sure if we could or could not remove these accounts. So, we decided to disable the accounts instead. I ran the commands to disable both accounts and confirmed admin account works as well. 


Finished updates
Enrolled device in entra and Intune
Installed ConnectWise
Verified computer has admin password and is in ConnectWise
User had an E1 license, switched that to an E3
Installed JMeter and Jave, and azure vpn for user and configured it

remoted into the computer and checked for updates, installed connect wise and confirmed we can login as admin.

Remoted into computer and ran updates, connected to entra, installed connectwise and had the user login. Confirmed AKSAdmin can login with no issues. 

remoted into the computer and ran updates, connected user to their account and signed them in. Then we downloaded/installed Connectwise. Signed in as an admin and disabled their admin account.

Doing updates right 
Added to ArchKey Entra domain with users ArchKey credentials.
Installed ConnectWise and verified we can remote in.
Disabled all users except AKSAdmin and users account.
Confirmed AKSAdmin creds are working properly.
Installed AzureVPN.
Verified the device is under the user in Entra.

 remoted into the computer, and we were able to harden/enroll in Intune after configuring their account with the appropriate licenses and groups they needed for the enrollment

Completed Windows updates
Added to ArchKey Entra domain with users ArchKey credentials
Verified device was added to Entra (In grace period)
Set Primary user to myself
Verified user could log into Windows with ArchKey credentials
Verified AKSAdmin account was created and functional
Removed all local admin accounts besides AKSAdmin and local administrator
Installed ConnectWise access
Request permission for an e3
Applied E3 license
Remote into ASPLAP3336
Installed Office using file available at portal.office.com
Verified user could login to Office apps with ArchKey credentials


