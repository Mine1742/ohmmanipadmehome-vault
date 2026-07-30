#printer

Obtain make and model of printer/plotter


Check device to printer associations
Check for updates
Check driver compatibility and for new updates

add printer using ip and port 9100

set default printer



Step-by-Step Troubleshooting
1. Check the Print Queue
Open the Devices and Printers (Windows) or Printers & Scanners (Mac) section in your settings.
Click on the 1st-floor copier and check the print queue:
Look for any stuck or pending jobs.
If there are stuck jobs, cancel them and try sending your print job again.

2. Verify Printer Connection
Ensure that your computer is connected to the same network as the printer/copier.
If the copier is on a separate VLAN or subnet, ensure that your device has proper access.
Test the connection by pinging the printer’s IP address:
Windows: Open Command Prompt and type ping <printer_ip>.
Mac: Open Terminal and type ping <printer_ip>.

3. Check Printer Status
Walk to the copier and check its status:
Look for error messages on the copier’s display (e.g., paper jam, low toner, or offline).
Ensure the copier is online and ready to receive jobs.

4. Ensure Correct Printer Selection
Double-check that you are selecting the 1st-floor copier in the print dialog.
If multiple printers with similar names are listed, you might be sending the job to the wrong one.

5. Authentication or Security Settings
Some copiers require user authentication for printing:

Check if you need to log in or swipe an access card at the copier to release the job.
If authentication is required, ensure you are logged into the printer software with the correct credentials.

6. Check Printer Drivers
Outdated or incompatible drivers can cause print jobs to fail:

Go to the printer manufacturer's website and download the latest drivers for your printer model.
Reinstall the drivers:
Windows: Go to Devices and Printers, right-click the printer, and select Remove device. Then add it again with the updated driver.
Mac: Go to System Preferences > Printers & Scanners, remove the printer, and re-add it with updated drivers.

7. Test with a Different File
The issue might be file-specific:

Try printing a simple document (e.g., a plain text file) to see if it prints.
If it does, the original file may have formatting or content issues.

8. Reset the Printer
Power cycle the printer/copier:

Turn it off and unplug it for about 30 seconds.
Plug it back in and turn it on.
Try sending the print job again.

9. Verify Print Spooling
The spooling service may have encountered an error:

Windows:
Open the Services app (services.msc).
Look for Print Spooler, right-click it, and select Restart.
Mac:
Restart your computer to reset the printing subsystem.

10. Check for Print Job Release
Some office setups require jobs to be manually released at the copier:

Walk to the copier and check the Print Job Release or Secure Print section on its touchscreen or interface.

11. Network Issues
If the copier is networked:

Ensure the printer’s IP address hasn’t changed (check the copier settings or ask your IT admin).
Restart your router or network switch if you suspect network connectivity issues.







-Just an information note on printer netsettings
#powershell 

![[Pasted image 20241226081837.png]]