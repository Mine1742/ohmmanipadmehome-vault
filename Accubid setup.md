#accubid 
install windows app first as it is replacing rdp

to map A drive:
New-PSDrive -Name "A" -PSProvider FileSystem -Root "\\aksmrdc.aadds.archkey.com\Accubid" -Persist

 \\akzfile.aadds.archkey.com\Accubid

how many screens do you want the AVD to occupy?
Do you use Change Orger?
Livecount?
Are you Elec or Tech?


#new RDP process
cp
remote desktop app
install

ask eu about display
open app
pin to task bar
open
subscribe
r click >settings
turn off default settngs
turn off displays not using
open RD

open downloads folder
paste in vcredist_x86>run>delete

map a drive

do sso

reset up accubid




License Server  

There is no on-prem license server. Licenses are cloud based  

If user is requesting a license reach out to the Accubid Lead for each site.  

- Bill Gavin – ArchKey Sachs  
    
- John Ghirardi – ArchKey Parsons  
    
- Albert Robles – ArchKey Sprig  
    
- Kelly Clontz – ArchKey Mona  
    

Once approved for software, please reach out to Robert Leftwich or Paul Chiappetta to apply license to account


for pec might need to add to SEC- Estimating [parsonscorp.int/Users]


new users add them a folder
example: \\estimate.parsonscorp.int\Accubid Data\codata\jtyler

A centralized server for Accubid 16 files is available for all Estimators and PMs. 

AKSMRDC1.aadds.archkey.com | ping * 
AKSMRDC.aadds.archkey.com | 172.16.87.14*
AKSMRDP1.aadds.archkey.com |  * - mona

License Server 
There is no on-prem license server. Licenses are cloud based 
If a user is needing a license, please reach out to Robert Leftwich or Paul Chiappetta 

Security Groups 
Users must be assigned to the following Azure AD Groups 
APP Accubid - Provides access to the Network File Share 
App Trimble Accubid SSO - Allows login via SSO 
And also to either the accubid estimator or accubid project managers


|                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- |
| [ArchKey IT - Version 16 - All Documents (sharepoint.com)](https://archkeysolutions.sharepoint.com/sites/ArchKeyIT/Shared%20Documents/Forms/AllItems.aspx?newTargetListUrl=%2Fsites%2FArchKeyIT%2FShared%20Documents&viewpath=%2Fsites%2FArchKeyIT%2FShared%20Documents%2FForms%2FAllItems%2Easpx&id=%2Fsites%2FArchKeyIT%2FShared%20Documents%2FGeneral%2FAccubid%2FInstallSource%2FVersion%2016&viewid=7c99f415%2Dfcae%2D48d1%2D81a9%2D34f546559ee1) | Open in your "ArchKey" Web Browser |

Please install only the following features  

 Accubid Pro 16 
 Change Order Pro 16 
 Supplier Link 


Setting Generic User 
On user's machine, open Powershell as Admin 
Install-module CredentialManager 
You may be prompted to update and install. Make sure you're selecting Y for Yes or A for Yes to All 

Import-Module CredentialManager 
Close PS and reopen as Standard User 
Run the following script 

New-StoredCredential -Target 'aksmrdc.aadds.archkey.com' -Type Generic -UserName 'aadds.archkey.com\<Users UPN>' -Password '<Current MS password>' -Persist 'LocalMachine' 


Mapping Network Drive (Accubid A:\) 
Open File Explorer 
Right-click This PC 
Select Map Network Drive 
Drive Letter: A 
Folder Path:  \\aksmrdc.aadds.archkey.com\Accubid 
Windows Authentication 
Username: aksmrdc.aadds.archkey.com\<User's UPN> 
Password: <User's current MS Password> np
Reconnect at sign-in: Check 
Connect using different credentials: Check 
Click Finish 


Sprig maps
Here's all

S:\Estimating\Accubid Data\JOBDATA
Need to choose one and add in folders location
or add whats needed

S:\Estimating\Accubid Data\JOBDATA\Estimators 2025
S:\Estimating\Accubid Data\JOBDATA\Facilities Services\2025 Facilities Services
S:\Estimating\Accubid Data\JOBDATA
S:\Estimating\Accubid Data\JOBDATA\Estimators 2025 - 16

DB: S:\Estimating\Accubid Data\Databases





Application Configuration (Settings) 

Accubid Pro 16 

Job Folders 
Navigate to Settings 
Select Job Folders 
Click Add 
Enter the name and path of the folder 
A:\Accubid\Jobdata\Region 

Central 
East 
National 
North Central 
Technologies 
West 

Click OK 
Click OK 

Database Folders 
Navigate to Settings 
Select Database Folders 
Click Add 

Enter the name and path of the folder 
Electric 
A:\Accubid\Database - Elec\Legacy 
Technologies 
A:\Accubid\Database - Tech\Legacy 
Click OK 

Click OK 
Options 
Navigate to Settings 
Select Options 
Change Order Pro 16 
Project Folders 
Navigate to Settings 
Select Project Folders 
Click Add 

Enter the name and path of the folder 
A:\Accubid\COData\Region 

Central 
East 
National 
North Central 
Tech 
West 
Click OK 

Click OK 
Database Folders 
Navigate to Settings 
Select Database Folders 

Click Add 
Enter the name and path of the folder 
Electric 
A:\Accubid\Database - Elec\Legacy 
Technologies 
A:\Accubid\Database - Tech\Legacy 
Click OK 

Click OK 
Options 
Navigate to Settings 
Select Options

This additional step is for Technologies Only
Under File Locations tab - place a check the three boxes and enter the following in all four cells
A:\COData\Tech

This additional step is for ArchKey N. Central Only

Common style files
C) Acquire schedule screen style at startup
Folder A:\COData Global File\North Central
Acquåe job screen style at startup
Folder A:\Screen-Report Styles\North Central\Settings
Common Extenson Views
C Acquire extension views at startup
Folder A:\COData Global File\North Central
Global Files Folder
Folder: A:\COData Global File\North Central




JobData Paths (Accubid Job file locations) Accubid 14 Pro

Twin Cities Electrical - \\estimate.parsonscorp.int\Accubid Data\JobData

Twin Cities (including ASI GV and Roch) Technologies - \\estimate.parsonscorp.int \Accubid Data\Jobdata-Technologies

MEI Electrical - \\estimate.parsonscorp.int\Accubid Data\Jobdata-MEI

MEI Technologies - \\estimate.parsonscorp.int \Accubid Data\Jobdata-MEI

Duluth electrical - \\duluthgc\Accubid Data\Jobdata

Duluth Technologies - \\duluthgc\Accubid Data\Jobdata-Technologies

Phoenix - \\phxpwr\accubid data\jobdata

Database Paths

       Twin Cities Electrical - \\estimate.parsonscorp.int \Accubid Data\Databases 

       Twin Cities (including ASI GV and Roch) Technologies - \\estimate\Accubid Data\Databases-Technologies 

       MEI Electrical - \\estimate.parsonscorp.int \Accubid Data\Databases 

       MEI Technologies - \\estimate.parsonscorp.int \Accubid Data\Databases-Technologies 

       Duluth Electrical - \\duluthgc\Accubid Data\Databases 

       Duluth Technologies - \\duluthgc\Accubid Data\Databases-Technologies 

       Phoenix - \\phxpwr\Accubid Data\Databases1

COData Paths - (Change Order locations)

Twin Cities Electrical - \\estimate.parsonscorp.int \Accubid Data\codata

Twin Cities (including ASI GV and Roch) Technologies - \\estimate\Accubid Data\codata-Technologies

MEI Electrical - \\estimate.parsonscorp.int \Accubid Data\codata-MEI

MEI Technologies - \\estimate.parsonscorp.int \Accubid Data\codata-MEI

Duluth electrical - \\duluthgc\Accubid Data\codata

Duluth Technologies - \\duluthgc\Accubid Data\codata-Technologies

Phoenix - \\phxpwr\accubid data\codata

You can ask him if any of these make sense to him. when you are in the directory, youll want to look for jtyler  I would ask his location on where he is. Like if he is duluth, technologies that is if he is a PEC user or parsons