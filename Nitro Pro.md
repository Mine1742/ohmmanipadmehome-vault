#nitro


if the eu is not in the app nitro group they have to be issued an account by paul or robert prior to applying the license so we can track who is licensed

Team, the Nitro Pro 14 Intune Pkg has been updated to ver. 14.37.2 with the updated license file. Reminder that Nitro users need to be added via the Nitro Admin Portal and added to Azure group App Nitro PDF for SSO.


needs a license from:   robert L
remote in install from CP and apply the license 

Application states "TRIAL EXPIRED" 

Issue: 

Nitro Pro users are stating that their software is displaying their trial period had expired and to purchase the software. 

Resolution 

Install volume license key. 

Upload License File 

- Get Licence file from  
    

[ArchKey IT - Nitro PDF - All Documents (sharepoint.com)](https://archkeysolutions.sharepoint.com/sites/ArchKeyIT/Shared%20Documents/Forms/AllItems.aspx?newTargetListUrl=%2Fsites%2FArchKeyIT%2FShared%20Documents&viewpath=%2Fsites%2FArchKeyIT%2FShared%20Documents%2FForms%2FAllItems%2Easpx&id=%2Fsites%2FArchKeyIT%2FShared%20Documents%2FGeneral%2FNitro%20PDF&viewid=7c99f415%2Dfcae%2D48d1%2D81a9%2D34f546559ee1) 

New Nitro License key 

eyJQYXlsb2FkIjp7IkN1c3RvbWVyTmFtZSI6IkFyY2hLZXkgU29sdXRpb25zIiwiRXhwaXJhdGlvbkRhdGUiOiIyMDI3LTA3LTE1IiwiTGljZW5zZVV1aWQiOiJiOWM4MTIzYy1jZTNlLTQ5MGUtYThkZS02MWJlZTk4YzllNDgiLCJQcm9kdWN0TmFtZSI6InBybzE0In0sIlNpZ25hdHVyZSI6IkFPM1VIdEwwdHdIVThxcWtVNTNOZTBKK0EramM0N3JkaVUzblBHdHBjRVVYeHBRbWR1MEpKekMrejRTeTRaZGdXSFRoOVwvRlM3bTZCa09wZ2pqMXc4MW9WQWZVNVJaOTQyK2QrMW91VjB6dFBRYzR5QTlJeG9PUmYzbkkwWGFycjNhWldJS3VmR2ZNeFI2Rm5UaENJVitwS2RTQmVoQTVGQ3c2Vk9GV0lsSGVCZmxQQiJ9

- Access user's machine via ConnectWise 
    
- Open Nitro Pro 
    
- Click on Help then Activate 
    
- Enter user's First name and Last name. 
    
- Click on Load from file 
    
- Navigate to where the .lic file was dowloaded and select it to upload 
    
- Click Ok 
    

Activate using ConnectWise 

- Locate user's machine in ConnectWise 
    
- Select the Commands icon on your ConnecWise console 
    
- Run the following command 
    this is the license
    -s eyJQYXlsb2FkIjp7IkN1c3RvbWVyTmFtZSI6IkFyY2hLZXkgU29sdXRpb25zIiwiRXhwaXJhdGlvbkRhdGUiOiIyMDI2LTA3LTE1IiwiTGljZW5zZVV1aWQiOiJmM2Y1NDdmMy0yNDExLTQwYjAtYTViYy02NGRmMGMxOTNlYWEiLCJQcm9kdWN0TmFtZSI6InBybzE0In0sIlNpZ25hdHVyZSI6IkFUcUFSZllwT3RCVWlDZU9xeWcwV1M5MlJsVFBWc1JWdGVlNUdHSTlMS3FmOUMranIrSjV3Z2lCU0JBNjRjYUd2XC9lNnMwdXNBOGZZMzlKdHFRS3ZrYzEzQU1WTVlZZVpCSEMreVhtRHYrcjc2Q1hXYnJxb2M0ZjdIM0JueStKUEJjczB0N1RJUHlQaE4ydEpvVWZKMjNKNlEwb1dmaVowUjhYY1h6NDJLRnVYamJIdCJ9
        
- If Nitro is open, close the program and reopen. 
    
- Application should be licensed. 
    
- Be sure to have user log into application using SSO

Need to make sure app is assigned also too the individual via groups in Entra  
  
Also the version in company portal is old. So it installs expired trial. Have to get the one from sharepoint