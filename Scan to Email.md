
Need credentials from onsite




Steps to Set Up and Use Scan to Email
1. Configure the Printer or Scanner
You need to set up the device to use an email server for sending emails.

Basic Setup Steps:
Access the device’s web interface or control panel.
Go to the Email Settings or SMTP Settings.
Enter the following SMTP server details:
SMTP Server Address: (e.g., smtp.gmail.com, smtp.office365.com).
SMTP Port: Typically 587 for TLS or 465 for SSL.
Authentication: Enable authentication and provide the email address and password.
Set the Sender Email Address:
This will appear as the "From" address for scanned emails.
Test the settings to ensure they work.
2. Scan to Email Using the Device
Once the email configuration is complete:

Place the document in the scanner (feeder or flatbed).
Select Scan to Email from the menu.
Enter the recipient's email address manually or select it from the device’s address book.
Choose the scan settings (e.g., file format like PDF or JPEG, resolution).
Start the scan, and the device will email the scanned file as an attachment.
Example SMTP Settings for Popular Email Services
Service	SMTP Server	Port	Security	Authentication Required
Gmail	smtp.gmail.com	587	TLS	Yes
Outlook/Office365	smtp.office365.com	587	TLS	Yes
Yahoo Mail	smtp.mail.yahoo.com	465	SSL	Yes
Custom Domain	Check your provider's documentation for SMTP settings.			
Troubleshooting Tips
Authentication Errors:

Ensure the username and password for the email account are correct.
For Gmail or other secure services, you may need to enable App Passwords or allow less secure apps.
Email Not Sent:

Check the SMTP server and port settings.
Verify the device has internet access.
Ensure the recipient’s email address is correct.
Large File Size:

Many email servers have file size limits (usually 10–25 MB).
Reduce the scan resolution or split the document into smaller parts.
Firewall or Network Restrictions:

Ensure the SMTP server is accessible from your network.