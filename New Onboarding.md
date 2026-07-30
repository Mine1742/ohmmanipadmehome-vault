#newhire

![[Pasted image 20260507125805.png]]



chris von or jen braden they are valid requesters and do not need hr
other req need hr approvals

if through talent acquisition then e5 license auto, office user and gets a laptop

Mona Create new account in entra
else create user acct in AD mgr 
	enter information provided in ticket
	
For Mona:  
3 groups needed for onboarding a cloud account.
MFA
Exclaimer
App protection policy

PC user - M365 E5

Mobile-only user - O365 E1, Enterprise Mobility & Security E5, Defender for Office P2 (Security Group App Office_365_E1_DP_2_EMS_E5) this will auto assign the licenses to the user. You'll want to add licenses manually and then add the group. If we do not have all the licenses, when one gets freed up, the group will auto assign.

add new user to the MFA group

if an iPad or phone only user,  put in the App Office_365_E1_DP_2_EMS_E5 group to issue licenses

send temp pw to user via 1pass

add to <location> all employees group

add user to AD
**add eu to proper exclaimer group**


When onboarding new users make sure to put them in synching OUs


Nick Rykal parsons field supervisor


the Parsons domain OUs for them I'd just put them in Archkey > Archkey Office. If its a PEC technologies user maybe one of those other two OUs in the Archkey Parent OU. Not sure if the sub OUs actually make a difference but I know they all sync.

The correct OUs are different depending on which domain you're looking at though.

For Sachs its Office Users

~~For Mona its Mona Electric Group > MEG Users > corresponding sub OU depending on location/role.~~

For sprig its Archkey Accounts OU 

to adjust the email signature: Logged into AD Manager
Located User
Under "Account" tab, added requested modifications under ExtensionAttribute1



Nonazuresyinching OU
Unfortunately its different for each domain. One thing that is consistent is that the standard "Users" OU is a nonsyncing OU same goes for the default disabled OU. So if you get an offboarding request and they ask you to disable someone and give mailbox perms to another user, you need to put the disabled Onprem principle in one of the AzureSyncingOUs designated for term'd users. If you put them in the regular disabled OU, they will lose sync in Entra which completely removes the account in the cloud, including their mailbox so it can really screw things up if it goes unnoticed. I think there might be a KB on sharepoint or the OneNote that lists all of the syncing OUs for each domain, I'll check.

IF A CONSULTANT
[https://archkey.freshservice.com/a/catalog/request-items/107](https://archkey.freshservice.com/a/catalog/request-items/107 "https://archkey.freshservice.com/a/catalog/request-items/107") or manually navigate to Request a Service > User Account Management > Contractor Access Request



Part 1: Azure AD Joinin’ 101  
Important  

"Only new machines are Azure AD Joined. Old machines need Hybrid Join Fixed. Effective Dec 18th Legacy On Premise AD Join will be restricted." 

 "Once all user’s windows devices are Intune compliant please add the user to the Azure AD Group 'MFA Intune Required'. " 

Hot Tip - If an end user uses Chrome they will need to install the chrome extension 'Windows Accounts' 

Part 1: Confirming User Prerequisites 

Is the user in Entra? 

Is the User is licensed with 'Enterprise Mobility and Security E3'? 

Request end user to open Entra ID and show what licenses they have assigned. 

If the user is not licensed they won’t be able to enroll into Intune completely. They will however still be able to Azure Join the device. 

Is the User is licensed with 'Office 365 E3'?  

What would be the difference between having an Office 365 E1 and E3? 

If the user is not licensed they will not be able to activate Office Desktop Apps 

Group Membership: 

‘MFA’ – This group ensures the end user will be required to have Multi Factor Authentication. Very important! Sprig Users must be in the Sprig All Employees Group. 

PEC 

All Employees,  

SEC-Barracuda, 

Mfa.sec-Office365 

 

MEG  

All ArchKey tenant users 

Archkey Password Reset 

MFA 

APP Exclaimer ArchKey Mona Email Signature 

APP Freshservice MEG 

 

Part 1: Azure Join AD Join  

 Prerequisites:  

Recreate TRAINME VM on DENPRO Azure. 8VCPU 32GB RAM, Enable RDP 

Create Teams Meeting for Training Session 

The Trainee must be licensed with an Office 365 E3 and Enterprise Security + Mobility E3 License to provide the ability to fully manage the device via Intune and Activate the Desktop License.  

Steps: 

Trainee: Share there full computer screen via Teams Meeting 

Trainee: Remote Desktop: mstsc /v 20.55.124.69 Username AKSAdmin Password TCOAvenger23! 

Rename the computer 

Trainee: Rename the local computer with the ArchKey computer naming convention <3 Letter Org Code>-<Last 6 of Serial/Service Tag>-<Computer   type 2 Letter><Last 2 of Year> 

Do you know how to obtain the serial number of the device via System Information? 

Examples: 

MEG-123456-SL23 

 
Trainee: Join the Device to Azure AD (AADj) 

Settings > Accounts > Access Work or School > Join this Device to Azure   

When prompted have the Trainee use their own Archkey.com credentials to logon 

Note: Whomever Joins the machine is a local admin. We ALWAYS want to have the technician join initially and later in the process we will assign the device in Intune a Primary User. Secondary users will be Non-Administrators. 

Note: Office 365 E3 Licensing gives you a quota of up to 5 computers to activate the Office 365 Desktop Software.  

Trust but Verify! 

Open Computer Management > Event Viewer > Applications and Services > Windows > User Device Registration. These logs will show you details on the Join Process. Good place to go if you need to troubleshoot Join Errors.    

Instruct: Let’s open the Endpoint Manager in Windows to see if the Device is showing up yet 

Exploration 

OS: What is the current build of the Windows OS. 

LAPS: s the device in Laps yet? What local username and password can I use to logon to this device as a local administrator? 

Action Item for Engineering: Why does I have to hand type the AKSAdmin password 

If the device is not showing in Intune yet you may want to skip to the next step and cycle back to Step 6. 

Instruct: Task Manager can be used to get some insight into if the installation is progressing or stalled. Open Task Manager. Process you might see pop up: 

Microsoft Windows Intune Agent – Intune is configuring the device. 

Antimalware Service Executable – Microsoft Defender for Endpoint is installing or scanning the device 

Windows Installer – Intune is installing applications  

CPU might be pegged in task manager. On low performance devices you may see consistently high utilization at 100% 

Microsoft Office Click to Run – Intune Is installing Microsoft Office 

Antimalware Service Executible – Microsoft Defender for Endpoint is processing onboarding requests on machine. 

 

Instruct: Open the Command Line under the user context and run: DSREGCMD /STATUS 

AADJ >YES, NO, NO 

 		Tenant Details should be populated  

Diag Data: Managed by: MDM 

 

Instruct: Verify Windows Settings > Accounts > Access Work or School > Azure Connect Click the Info Button to view Sync information 

Verify Registration versus Azure AD Join in Entra 

https://entra.microsoft.com 

Verify Primary User in inutne 

https://endpoint.microsoft.com > Devices > Windows > search for Device 

Verify Ninite  

C:\program files (x86)\ninite Agent 

Verify The the Defender is connected in security.microsoft.com 

Verify ConnectWise 

C:\program files (x86)\ITSPLatform 

C:\Program Files (x86)\ScreenConnect Client (8a35...) (About 30 Mins to appear) 

Local Admin would get Duo Authenticate 

 

Applications: 

Exclaimer – Manages signatures on behalf of users in Outlook. If C:\Program Files (x86)\Exclaimer Ltd exists 

Office 365 – Should see Word, Excel, Outlook applications in Start Menu 

OneDrive – You may see the icon for one drive but be aware during this process you are logged on as the Local Admin AKSAdmin. One Drive will not sign on until you sign onto the machine with an ArchKey.com User Account. 

Ninite – this is our third party patching software for things non Microsoft like Firefox, Chrome and so on. You can verify it is installed by finding the process ninite.exe in task manager or if c:\program files (x86)\ninite agent exists. 

Company Portal – eventually this app will show up in your start menu. Be aware just as Step C you will need to be logged on as a Archkey.com user to see all the magic. 

Company Portal provides deeper insight into apps it has installed automatically and also provide a place for you to see other apps you can install under a non administrator context.  

Company portal will also show you the progress of application installation.  

When opening company portal you will be prompted to choose correct Category (assuming you are logged on with your archkey.com account). Choose what seems appropriate. This is for tagging purposes only. There is no configuration at the time of this writing that leverages tagging. 

ConnectWise – This is our Remote Management Tool 

C:\program files (x86)\ITSPLatform (Will show up First) 

C:\Program Files (x86)\ScreenConnect Client (8a35...) (Slow machines this coud take longer) 

You should soon be able to search ConnectWise for the machine name. At this point you should connect via ConnectWise and logon with your Archkey.com account. If you do not see the option for Other User then restart the computer. 

Defender for Endpoint – Go to the Microsoft 365 Defender Admin portal in your browser to see if the machine exists under devices. It can take a while for this to populate. 

Intune Device 

Verify Recovery Keys (This may take a while to populate) if you don’t see this you can cycle back when you get to the end of training. Go to Entra Admin Console in your webbrowser  to check. 

Verify LAPS 

Duo Security - C:\Program Files\Duo Security 

 

Once ConnectWise Screen Connect is installed remote in via ConnectWise, Restart the Computer and via ConnectWise logon with your Archkey.com account. 

 Once all the users’ Windows devices are enrolled into Intune please add the user to the Azure AD Group "MFA Intune Required".  

  

*After Duo is installed any administrative functions under your personal ArchKey.com account will require you to request a bypass code from the SOC via Fresh Service 

 Once the machine shows up in ConnectWise :30 Minutes 

Restart Machine and connect as your archkey.com to logon. 

Logon to  Microsoft Hello (will not work for duo enrolled Users) 

Sync Company Portal to fix – GP getting in the way 

User account? No admin access 

Company Portal sync 

Opened Word > Signed in 

Activation prompt > 

 

Post Azure AD Join Questions  

Intune 

Please open up Intune in your web browser 

Can you show me what the computer PC1400 Intune Compliance status is? 

PC1400 had a status of Not Evaluated 

OS: What is the current build of the Windows OS.  

Can you tell from the build number if it’s Windows 11 or Windows 12? 

Kevin Scott is kinda of an ass. Could make an educated guess 

What feature pack or windows version supports LAPS? 

22H2 or 10.0.19045 and above is LAPS Supported 

LAPS: What local username and password can I use to logon to this device as a local administrator? 

User must be Intune Admin, You can see password via Entra/Device 

Who is the primary user?  

How does being assigned a primary user affect your Office 365 Desktop  

Can we tell if Duo Security is installed on PC1400? 

Can you let me know if Duo was installed manually or if this is a managed application? 

Entra question: Can you show me all the devices registerered or joined for this primary user? 

Entra question: Can you show me what groups this user is a member of? 

Entra Question: Can you let me know if there are any groups that are missing from the user account? 

Entra Question: Can you show me the different Authentication methods setup for this user? 

Entra Question: How do you create a temporary password for the user? 

 

Defender 

Please navigate to the Microsoft 365 Defender Admin console. 

Is Defender onboarded and enabled on the computer. Is Defender Antivirus Mode “Active”. 

What is the “Exposure Level” for PC1400 in Microsoft Defender? 

  Show me software that needs to be updated (Security Recommendations filter) 

  Show me software that needs to be uninstalled (Security Recommendations filter) 

  Show me Missing KBs for the machine 

Can you show me the join type for device PC1400 

  What is the difference between Registered, Hybrid Joined, Azure Joined 

Registered - Office or website that required modern authentication was opened from personal or work device. Common user signed in with Azure AD Credentials OWA, Outlook Installed, Teams 

What Group could we assign the user to prevent access from non intune joined devices 

Hybrid Joined - Devices joined to On Premise AD and then subsequently enrolled into intune via the Hybrid Join Process. Group Policy and local AD On Prem user credentials are allowed AND Intune configurations are applied. 

Azure AD Joined - Only allows Azure AD accounts to logon AND Intune configurations are applied. The device does not require any communication directly with Domain Controllers. Ala no VPN 

 

Mapped Drives 

Action: Investigate Map Drive Cloud Managed Agent 

Need a full list of Mapped Drives 

MEG - None 

PEC  

SPE   

SEC 

  General 

  net use J: \\fs-1.sachsco.com\common /persistent:yes 

  net use P: \\fs-1.sachsco.com\projects /persistent:yes 

  net use I: \\fs-1.sachsco.com\depts /persistent:yes 

   

  Departments (HR, Design, IT) 

  net use I: \\fs-1.sachsco.com\depts\Design /persistent:yes 

  Accubid_Users 

  net use U: \\fs-1.sachsco.com\accubid /persistent:yes 

  

  ILRG 

  net use M: \\fs-1.sachsco.com\ilrgcommon /persistent:yes 

  

  R.Vandelay 

  net use V: \\sec-vandelay.sachsco.com\restricted /persistent:yes 

  

  R.NGAWest 

  net use E: \\fs-1.sachsco.com\eerodesign /persistent:yes 

  net use N: \\sec-eero.sachsco.com\common /persistent:yes 

  

  R.NGABAS_Controls 

  net use W: \\sec-eero.sachsco.com\BAS_Controls /persistent:yes 

  net use Z: \\ds-archive.sachsco.com\kingsbay /persistent:yes 

  net use X: \\ds-dekalb.sachsco.com\common /persistent:yes 

  net use O: \\sec-omaha.sachsco.com\common /persistent:yes 

  net use S: \\ds-socialcircle.sachsco.com\common /persistent:yes 

  net use K: \\sec-costpnt.sachsco.com\cpapps /persistent:yes 

  net use Y: \\cbfs.sachsco.com\common /persistent:yes 

  

  

Printing 

DirectPrint.io -  

  

Part 2 

Hybrid Joined Troubleshooting 

//Answer these important questions prior to proceeding 

Identify if they are personel or corp devices prior to prceeding? 

Is the device joined to the on premise domain. If not Azure AD Join device? 

  

Part 3 

[Wipe Machine] 

Remove ConnectWise Device 

Remove Device Registrations Entra 

Mark Inactive Microsoft Defender 

 

 [Verify] 

Verify ConnectWise 

Remove legacy EDR Sophos, Crowd Strike. If unable to remove wipe or replace device 

Patch Windows 22H2. If Laps password exists you have 22H2 

Remove local admins (Excluding AKSAdmin) 

If the user was previously a local admin. See Kevin 

  

From Techs Computers 

Open Intune 

Find a device 

Check the Compliance Settings 

What is the difference bewteen Discovered apps and Managed Apps 

  

Open Microsoft Defender / Security.microsoft.com 

Find a device, determine the risk level 

Understand the relationship between Compliance by Machine Risk Level 





Revit 2027 -x

Revit 2024 -x

Revit 2025 -x

Revit 2026 -x

Desktop Connector - x

*BIM Collaborate Pro License -- x

Navis Coordination Issues Add-In - x

Navis Revit Exporter Plug-in 24 x

Navis Revit Exporter Plug-in 25 x

Navis Revit Exporter Plug-in 26 n\a


NEED EVOLVE LICENSE

eVolve 2023 - no revit 23

eVolve 2024 - x

eVolve 2025 - x

eVolve 2026 - x

Apollo - x

Coins - x

Guardian - x

Navis Manage 2027 - X

AutoCAD 2027 - X

Bluebeam -x

DUO Separate ticket

DiRoots - x

DiRoots sheets - x

IMAGiNIT ? Stand alone - x