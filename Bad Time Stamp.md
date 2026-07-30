#ntp


 For Bad Time Stamp. Is DUO. PC Time wrong and not synced. Need to Uninstall DUO from CW, reboot machine, log in. Fix time / sync it.. Can use CMD, Time command ( HH:MM:SS AM/PM ).  Sync Company Portal as well. Reboot, test log in.

https://archkey.freshservice.com/a/tickets/65256?current_tab=details


cmd> w32tm /resync
Verify that the server’s clock is accurate using an online service like [time.is](https://time.is)

Okay, you have an HP EliteBook 840 G4, and you're getting the "Bad Request Timestamp" error at the Windows login screen. This means we need to focus on the BIOS clock and potentially the CMOS battery.

**1. Accessing the BIOS Settings on an HP EliteBook 840 G4:**

- **Restart Your Laptop:** Restart your HP EliteBook 840 G4.
- **Press Esc Repeatedly:
    
    **As the laptop restarts, repeatedly press the **Esc** key. 1 This should bring up the Startup Menu.  
    
    [
    
    1. HP Consumer Notebook PCs - BIOS Setup Information and Menu Options
    
    ](https://support.hp.com/id-en/document/ish_3900499-3190557-16#:~:text=Turn%20off%20the%20computer%2C%20press,to%20enter%20BIOS%20Setup%20Utility.)
    
    [
    
    ![Source icon](https://encrypted-tbn0.gstatic.com/favicon-tbn?q=tbn:ANd9GcTdjC8SG0gN-Rm2DYcCh3uJxuMwlOQGRi67KXcYxCFK1iMBk5YpG5hizb9Gd-poskFtCJzw8UfJOOGAQvsJfaxhm5VodtCGAJQ)
    
    support.hp.com
    
    ](https://support.hp.com/id-en/document/ish_3900499-3190557-16#:~:text=Turn%20off%20the%20computer%2C%20press,to%20enter%20BIOS%20Setup%20Utility.)
    
- **Select F10 for BIOS Setup:** On the Startup Menu, you should see an option that says "F10 Setup" or similar. Press the **F10** key to enter the BIOS Setup Utility.

**2. Navigating the BIOS to Find the System Clock:**

The exact layout of the BIOS settings can vary slightly, but here's a general guide:

- **Look for "System Configuration" or "Main" Menu:** You'll typically find the date and time settings within a section called "System Configuration," "Main," "System Information," or something similar. Use the arrow keys to navigate the BIOS menus.
- **Find "Date and Time":** Within that section, look for an option labeled "Date and Time," "System Date & Time," or similar.

**3. Setting the Date and Time in the BIOS:**

- **Use Arrow Keys:** Use the arrow keys to highlight the date or time fields.
- **Change Values:** Use the + and - keys (or sometimes the Page Up/Page Down keys) to adjust the values.
- **Set Accurately:** Set the date and time _as accurately as possible_. Compare it to a reliable time source like time.gov on another device.

**4. Saving and Exiting the BIOS:**

- **Look for "Exit" Options:** Look for a section labeled "Exit" or "Save & Exit."
- **Save Changes:** Select the option to save changes (usually "Save Changes and Exit" or "Exit Saving Changes").
- **Confirm:** Confirm that you want to save the changes and exit.

**5. If the BIOS Clock is Still Wrong or Keeps Resetting:**

- **CMOS Battery Replacement:** As mentioned before, a weak or dead CMOS battery is the most likely cause if the BIOS clock is incorrect or keeps losing time.
    - **Locating the Battery:** The CMOS battery on an HP EliteBook 840 G4 is typically a small, round, silver cell battery on the motherboard. You might need to partially disassemble the laptop to access it (refer to HP's support website or YouTube videos for disassembly instructions specific to your model).
    - **Replacing the Battery:** Once you've located the battery, carefully remove it (it might be in a holder) and replace it with a new one of the same type (usually a CR2032 battery). Make sure the polarity (+ and -) is correct.

**6. If You're Not Comfortable with BIOS or Hardware:**

- **Seek Professional Help:** If you're not comfortable working in the BIOS or replacing the CMOS battery, it's best to take your laptop to a qualified computer technician. They can diagnose the issue and make the necessary repairs.

**Important Notes:**

- **HP Support Website:** Check the HP support website for your specific model (EliteBook 840 G4). They might have documentation or videos on accessing the BIOS and replacing the CMOS battery.
- **YouTube:** YouTube can be a great resource for finding videos on how to access the BIOS and replace the CMOS battery on HP laptops. Search for "HP EliteBook 840 G4 BIOS" or "HP EliteBook 840 G4 CMOS battery replacement."
- **Static Electricity:** When working with computer hardware, be sure to ground yourself to avoid electrostatic discharge (ESD) that could damage components.

By following these steps, you should be able to correct the BIOS clock and resolve the "Bad Request Timestamp" error at the login screen. If the problem persists after correcting the BIOS clock, replacing the CMOS battery is the next most likely solution. If you're unsure about any of these steps, please seek professional help.


