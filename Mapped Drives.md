[[Hardware]] [[Networking Hub]] [[Software]]
All mapped drives should be set up using FQDN 

Z drive is the egnite drive and needs support form sprig onsite


ArchKey Mona 

No mapped drives as network shares are in SharePoint 

ArchKey Parsons 

|   |   |   |   |
|---|---|---|---|
|Drive Letter|Path|AD Security Group|Notes|
|G:\|\\ecs2018.parsonscorp.int\20 ECS||Offline|
|I:\|\\design.parsonscorp.int\cad|||
|O:\|\\parpwr.parsonscorp.int\Office|||
|R:\|\\parpwr.parsonscorp.int\50 Users|||
|T:\|\\cloudserver18.parsonscorp.int\T|||
|X:\|\\archivehq.parsonscorp.int\Archives|||

\\estimate.parsonscorp.int\Accubid Data 

ArchKey Sachs 

|                                     |                               |                                                                 |                                                                 |
| ----------------------------------- | ----------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| Drive Letter                        | Path                          | AD Security Group                                               | Notes                                                           |
| J:\|\\fs-1.sachsco.com\common       | Domain Users                  | All domain users @ SEC have access                              |                                                                 |
| I:\|\\fs-1.sachsco.com\depts        |                               | Each dept folder has a group access                             |                                                                 |
| "Restricted Drive"                  | \\fs-1\depts\restricted       |                                                                 | Each job has group starting with r. ie. R.NGAWest for NGA/EERO  |
| P:\|\\fs-1.sachsco.com\projects     | Domain Users                  | All domain users @ SEC have access                              |                                                                 |
| U:\|\\fs-1.sachsco.com\accubid      | Domain Users                  | All domain users @ SEC have access                              |                                                                 |
| N:\|\\fs-1.sachsco.com\sec-eero     |                               | NDA REQUIRED - r.NGAWest additional groups for specific folders |                                                                 |
| "Non-Standard"                      | \\fs-1.sachsco.com\eerodesign |                                                                 | NDA REQUIRED - r.NGAWest additional groups for specific folders |
| "Non-Standard"                      | \\fs-1.sachsco.com\GibsonAve  |                                                                 | NDA REQUIRED - r.NGAWest additional groups for specific folders |
| H:\|\\pc1312.Sachsco.com\eero scans |                               |                                                                 |                                                                 |

K:\                               [\\ds-archive.sachsco.com\kingsbay](file://ds-archive.sachsco.com/kingsbay) 

|                                    |     |
| ---------------------------------- | --- |
| V:\|\\fs-1.sachsco.com\EEROProject |     |
|                                    |     |
![[Pasted image 20250404160627.png]]
ArchKey Sprig 

|   |   |   |   |
|---|---|---|---|
|Drive Letter|Path|AD Security Group|Notes|
|||||

ArchKey 

A: [\\aksmrdc.aadds.archkey.com\Accubid](file://aksmrdc.aadds.archkey.com/Accubid) 

P: \\aksamrdc.aadds.archkey.com\projects