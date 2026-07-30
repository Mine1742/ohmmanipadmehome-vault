[[PFW Hub]]

Archkey - Database Access read Write

Make sure that the excel is 64 bit and not 32
Check trust center settings <TS steps for this below>  ensure to add user's onedrive archkey accounts

check in data>query options>dataload> security>sure fast data load is checked, and that sufficient ram is allowed in the cashe (4m should be good but if speed is noted as a concern up to 8m if available)

security> uncheck require user aproval
privacy> ignore privacy settings

download new document form sharepoint site if user is experiencing any 'weird problems'


Sachs has some unique vpn issues
ArchKey - Database access read write group is needed for access to SQL server

If getting blank login screens when trying to relogin then :

 have them delete the "Options" key from Registry
HkEY_CURRENT_USER\Software\Microsoft\Office\16.\excel\options

make sure to select org level security for both global and local
Sign user in under MS account for global and windows>current user for local


Follow TS directions in call center reference guide 

The VPN error is a generic error that is displayed when the PFW cannot talk with the SQL server. Some of the most common issues are: 

VPN Issue 

PFW Configuration & Data Source 

Document/Location not trusted 

 VPN Issue 

Issue: 

When attempting to run PFW update, prompted with VPN Connection error 
 

Resolution #1 

Establish Azure VPN tunnel 

Open Command Prompt and PING archkeysql.database.windows.net. 

If output resolves correct, the request should timeout. Proceed to Resolution 2. 

If output resolves to a Public IP, this indicates the device has an outdated VPN Profile 

Disconnect from Azure VPN Client 

Navigate to Network and Internet > VPN and remove the ArchKey VPN Profile 

Open Company Portal >Settings > Sync 

Reconnect the Azure VPN Client 

Verify DNS Servers are "172.17.1.4" & "172.17.1.5" 

In Command Prompt, run PING for archkeysql.database.windows.net 

Ping should resolve to a Private IP [172.17.x.x] 

Have user run PFW Update 

 

 

Resolution #2 

With the PFW open, if prompted with PROTECTED VIEW click Enable Editing 

Navigate to File > Options > Trust Center > Trust Center Settings > Trusted Locations 

Click Add new location 

Click Browse and navigate to the root folder where your PFW located 

Place Check Mark in Subfolders of this location are also trusted 

Click OK

Navigate to Data > Get Data > Query Options 

Under the Global section, select the following: 

Data Load - Place Check mark in Fast Data Load 

Security – Remove Check mark from Require user approval for new native database queries 

Privacy – Select Always ignore Privacy Level settings 

Click OK 

Navigate to Data > Get Data > Data Source Settings 

Click on Global Permissions 

Right Click on archkeysql.database.windows.net and select Edit Permissions 

Under Credentials select Edit 

Select Microsoft account and click Sign in 

Login and authenticate your ArchKey account 

Click Save/OK 

Close Data Source Settings window 

Restart PFW  

Have user run PFW Update 

 Is user working remotely or on the network? 


Check VPN Logs for further information 

Applications and Services Logs > Microsoft > Windows > RASClient > Operational 

 

Persistant issue: 

Escalate to PFW team for SQL TS

C:\Users\Bryant.Petway\PFW\AKS PFW 302366.600 - 1.30.25.xlsm