#networkdrive #nas

ensure vpn is connected
try to ping drive for connection
check on server status

check to see is the drive is mapped to ecms? (happened once) \\10.100.83.136

may have to reset user's passwords to gain access to drives



sprig s drive - \\\vmstore.sprigelectric.com\elc\shared
All mapped drives should be set up using FQDN 

ArchKey Mona 
No mapped drives as network shares are in SharePoint 

ArchKey Parsons 
Drive Letter Path AD Security Group Notes 

G:\ \\ecs2018.parsonscorp.int\20 ECS Offline 

I:\ \\design.parsonscorp.int\cad 
O:\ \\parpwr.parsonscorp.int\Office 
R:\ \\parpwr.parsonscorp.int\50 Users 
T:\ \\cloudserver18.parsonscorp.int\T 
X:\ \\archivehq.parsonscorp.int\Archives 
\\estimate.parsonscorp.int\Accubid Data 

ArchKey Sachs 

Drive Letter Path AD Security Group Notes 

J:\ \\fs-1.sachsco.com\common 

Domain Users 
All domain users @ SEC have access 

I:\ \\fs-1.sachsco.com\depts 

Each dept folder has a group access 

"Restricted Drive" 

\\fs-1\depts\restricted 

Each job has group starting with r. ie. R.NGAWest for NGA/EERO 

P:\ \\fs-1.sachsco.com\projects 

Domain Users 

All domain users @ SEC have access 

U:\ \\fs-1.sachsco.com\accubid 

Domain Users 

All domain users @ SEC have access 

N:\ \\fs-1.sachsco.com\sec-eero 

NDA REQUIRED - r.NGAWest additional groups for specific folders 

"Non-Standard" 

\\fs-1.sachsco.com\eerodesign 

NDA REQUIRED - r.NGAWest additional groups for specific folders 

"Non-Standard" 

\\fs-1.sachsco.com\GibsonAve 

 NDA REQUIRED - r.NGAWest additional groups for specific folders 

H:\ \\pc1312.Sachsco.com\eero scans 

 K:\      \\ds-archive.sachsco.com\kingsbay 

V:\ \\fs-1.sachsco.com\EEROProject 

ArchKey Sprig 

Drive Letter Path AD Security Group Notes 

 ArchKey 

A: \\aksmrdc.aadds.archkey.com\Accubid 

P: \\aksamrdc.aadds.archkey.com\projects 
\\fs-1.sachsco.com\accubid 

 brandon.guse@archkey.com 








Multiple ATT ISP network outages reported in St. Louis area. Confirmed to be impacting NGA EERO Site and potential effecting 'N' Network Drive (EERO) connectivity

Remote into device PC1514

When attempting to connect to all fs-1 drives, presented 'Network path not found' error

Attempted to connect to VPN but received network connectivity error

Access work or school sync completed with no issue

Ran gpupdate
-Failed due to network connectivity

Ran dnsflush and registerdns

Restarted device

Issue persisted

Explained to user that service outages may be impacting connectivity to server side services

Documenting the ticket and investigating other tickets with identical issues
Remote into device PC1514
Disconnected 'I Drive' \\fs-1\depts
Attempted to reconnect but received authentication related error message
Reset user's password within AD Manager (richbread28oldRo$e)
-Locked account but user could not sign-in with new credentials
-Old credentials continued to work for sign-in
Verified Device was connected to [sachsco.com](https://sachsco.com/) domain with Access Work or Sschool
Confirmed AAD account was also connected
-Company Portal however listed the device as 'managed by another company'
-Device is within Azure but is not MDM managed or compliant
Ran all Lenovo updates. No Windows updates found
Performed Network Reset
-Made device discoverable
Performed restarted
-Issue persisted (Cannot connect to network drives due to lack of network connectivity)
Inspected network adapters
-DNS settings for both IPv4 and IPv6 were set to automatic

Logged into local AKSAdmin account

-Enroll into AAD was not available within Access Work or School
User described this issue suddenly occurred Wednesday 11/1/23
Contemplated re-installing network adapters but this would disconnect me from the user permanently
Recommended the user visit on-site for asisstance
