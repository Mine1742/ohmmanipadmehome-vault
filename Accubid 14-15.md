[[Accubid Hub]]
#accubid 
Server 

Accubid database is housed on Remote Desktop server.  

AKSMRDC.AADDS.ARCHKEY.COM

### License Server 

Server is housed at  
SPRIG | IP Address: 172.16.1.140 
SACHS| IP Address: 192.7.224.152  
PARSONS | IP Address: 

### Licensing 

For new Accubid users, it must be determined whether they are full-time or seasonal Accubid users PRIOR to Approval and setup for licenses to be assigned.

To view currently assigned users, navigate to Accubid Users.xlsx (sharepoint.com)

### Availability 

Accubid connectivity is only available through the Remote Desktop Server, AKSMRDC.AADDS.ARCHKEY.COM. Users accessing the remote desktop while on company network can access by opening Remote Desktop Connection normally. If remote, they will need to log into Azure VPN prior to attempting remote desktop connection.

### Security Groups 

When setting up users for Accubid, make sure they have been added to the following Azure AD Security Groups

App Accubid Pro


## Accubid Pro

Open Accubid Pro 

Select "Change the program security setting" click OK 

Select "Connect to a customized network security server" 

Input 172.16.1.140 or 192.7.224.152 for Server Address 

Click OK 

---Accubid Pro should automatically open 

Select No to use default Jobdata Folder 

Select Add 

Type \\aksmrdc.aadds.archkey.com\accubid data\jobdata\user folder 

User Folder  = the user's job folder you created earlier (ex. RLeftwich) 

Click OK 

Click OK again 

Select No when asked about using the Default Database 

Remove Highlighted Default Database 

Select Add 

Type \\aksmrdc.aadds.archkey.com\accubid data\databases 

Click OK 

On Menu select Settings > Options 

Remove check from "Prompt to create database..." 

Select Database tab 

Select Multi-user database

Click OK



### Change Order Pro

Open Change Order Pro

Select "Change the program security setting" click OK 

Select "Connect to a customized network security server" 

Input 172.16.1.140 or 192.7.224.152 for Server Address 

 Click OK 

---ChangeOrder Pro should automatically open 

Select Cancel to Select Project 

Select No to use default databases folder 

Add Check to \\aksmrdc.aadds.archkey.com\accubid data\databases 

Click OK 

On Menu select Settings > Options 

Select File Locations 

Remove Global Files Folder entry 

Type \\aksmrdc.aadds.archkey.com\accubid data\codata 

Select Database tab 

Select Multi-user database 

Click OK 

Open Settings > Project Folders 

Remove Highlighted Folder 

Click Add 

Type \\aksmrdc.aadds.archkey.com\accubid data\codata\user folder 

User Folder  = the user's COdata folder you created earlier (ex. RLeftwich) 

Click OK 