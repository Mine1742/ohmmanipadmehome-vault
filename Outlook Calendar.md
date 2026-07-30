#outlook 
[[Outlook Hub]]


If you're working with the **OWA (Outlook Web Access)** calendar, here’s a comprehensive guide to help you with common tasks and troubleshooting related to the calendar in the **Outlook Web App**:

---

### **Accessing the OWA Calendar**
1. **Log in to Outlook Web App**:
   - Visit [Outlook Web App](https://outlook.office.com) and log in with your Microsoft 365 or Exchange credentials.

2. **Access the Calendar**:
   - In the left navigation pane or the bottom-left corner, click the **Calendar icon** (looks like a small calendar).

---

### **Common Tasks in OWA Calendar**
#### **1. Sharing a Calendar**
1. Go to the **Calendar view**.
2. Right-click the calendar you want to share in the left-hand list and select **Sharing and Permissions**.
3. Enter the recipient's email address in the **Invite people** field.
4. Assign a permission level:
   - **Can view when I'm busy**: The recipient sees only your availability.
   - **Can view titles and locations**: The recipient sees event details like titles and locations.
   - **Can view all details**: The recipient sees all event details.
   - **Can edit**: The recipient can make changes to your calendar.
   - **Delegate**: The recipient can manage your calendar on your behalf.
5. Click **Share**.

#### **2. Adding a Shared Calendar**
1. In the **Calendar view**, click **Add calendar** (in the toolbar).
2. Select **Add from directory**.
3. Search for the person or shared mailbox whose calendar you want to add.
4. Click **Add** to display their calendar alongside yours.

#### **3. Creating Calendar Events**
1. Click **New event** at the top of the calendar view.
2. Enter event details:
   - **Event name**
   - **Start and end times**
   - Location (optional)
   - Invite attendees (optional)
3. Set **Recurrence**:
   - Choose from options like daily, weekly, monthly, or custom recurrence.
4. Click **Save** to create the event or **Send** if it's a meeting invitation.

#### **4. Setting Up Calendar Permissions**
- Permissions in OWA can be configured under **Sharing and Permissions**.
- For more advanced permissions (e.g., on shared mailboxes), these are typically managed in the **Exchange Admin Center** or via PowerShell.

---

### **Customizing Your OWA Calendar**
1. **Change View Settings**:
   - At the top-right corner of the calendar, click the view options dropdown (e.g., **Day**, **Week**, **Month**).
   - Choose the preferred layout.

2. **Set Working Hours**:
   - Go to **Settings > View all Outlook settings > Calendar > View**.
   - Adjust your working hours and work week.

3. **Change Time Zone**:
   - Go to **Settings > View all Outlook settings > General > Language and time**.
   - Select the correct time zone.

---

### **Troubleshooting OWA Calendar Issues**
#### **1. Shared Calendar Not Appearing**
- **Solution**: Ensure the calendar is properly shared with your account and re-add it:
  1. Go to **Add calendar > Add from directory**.
  2. Search for and add the calendar.

#### **2. Events Not Syncing**
- **Solution**:
  - Verify that your internet connection is stable.
  - Ensure your account is connected to Microsoft 365 or Exchange.
  - Check sync settings if using multiple devices or apps.

#### **3. Missing Calendar Permissions**
- **Solution**:
  - Ask the calendar owner to reassign permissions via **Sharing and Permissions** in OWA or Outlook.
  - Confirm permissions using the **Get-MailboxFolderPermission** PowerShell command if you're an admin.

#### **4. Notifications Not Working**
- **Solution**:
  - Go to **Settings > View all Outlook settings > Calendar > Notifications** and enable desired notifications (e.g., event reminders, email updates).

---

### **Advanced Administration (for IT Admins)**
#### **1. Managing Shared Calendars**
- Use the **Exchange Admin Center (EAC)**:
  1. Log in to the Microsoft 365 Admin Center.
  2. Navigate to **Exchange Admin Center**.
  3. Under **Recipients > Shared**, manage shared mailboxes and their associated calendars.

#### **2. Using PowerShell**
- **Add Permissions to a Shared Calendar**:
  ```powershell
  Add-MailboxFolderPermission -Identity "user@domain.com:\Calendar" -User "anotheruser@domain.com" -AccessRights Editor
  ```

- **View Current Permissions**:
  ```powershell
  Get-MailboxFolderPermission -Identity "user@domain.com:\Calendar"
  ```

- **Remove Permissions**:
  ```powershell
  Remove-MailboxFolderPermission -Identity "user@domain.com:\Calendar" -User "anotheruser@domain.com"
  ```

---

### **Key Features of OWA Calendar**
1. **Mobile-Friendly**:
   - Access the OWA calendar on mobile via a browser or Outlook app.

2. **Integration**:
   - Integrates seamlessly with Teams, OneDrive, and Microsoft To-Do for scheduling and task management.

3. **Cross-Platform Access**:
   - Events created in OWA sync automatically with desktop Outlook and mobile apps.

4. **Room and Equipment Booking**:
   - Use resource mailboxes to schedule meeting rooms or equipment.

---

