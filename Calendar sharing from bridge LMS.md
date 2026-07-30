
#bridge #outlook 

It sounds like you're trying to integrate **Bridge (Learning Management System - LMS)** with **Outlook Calendar**, but when you download the calendar event, it opens as an email in a **SharePoint web layout** instead of adding it to your Outlook calendar. Here’s how to troubleshoot and fix the issue:

---

### **1. Understanding How Bridge Exports Calendar Events**

Bridge typically provides a **.ICS (iCalendar) file** for importing events into Outlook. If the download is opening as an email instead of a calendar event, the issue could be:

- The **default app settings** for .ICS files.
- A **SharePoint redirect or policy affecting downloads**.
- Outlook’s **default behavior** when handling calendar invites.

---

### **2. Fix: Manually Import the ICS File into Outlook**

If the downloaded file **doesn’t auto-add to the calendar**, try adding it manually:

#### **For Outlook Desktop (Windows/Mac)**

1. **Download the ICS file from Bridge** (right-click and choose **Save As** if needed).
2. Open **Outlook**.
3. Go to **File > Open & Export > Import/Export**.
4. Select **Import an iCalendar (.ICS) or vCalendar file**.
5. Locate the downloaded .ICS file and open it.
6. Click **Save & Close** to add it to your Outlook calendar.

#### **For Outlook Web (OWA)**

1. Open **Outlook Web** ([outlook.office.com](https://outlook.office.com/)).
2. Go to **Calendar**.
3. Click **Add Calendar > Upload from file**.
4. Select the .ICS file and import it.

---

### **3. Fix: Ensure .ICS Files Open in Outlook Instead of SharePoint**

If the event file **opens in a SharePoint email layout**, the system might be forcing ICS files to open in a **browser instead of Outlook**.

#### **Change Default App for ICS Files (Windows)**

1. **Right-click** the ICS file > **Open with > Choose another app**.
2. Select **Outlook** and check **Always use this app**.
3. Try opening the ICS file again.

---

### **4. Fix: Download ICS File Properly from Bridge**

Sometimes SharePoint or browser settings **open downloads in a web-based viewer** instead of downloading them.

#### **Try this:**

- **Right-click** the download link and select **"Save Link As"**.
- Ensure it downloads as **.ICS** (not as a SharePoint email format).
- If prompted, select **"Download" instead of Open"**.

---

### **5. Fix: Use Direct Sync Between Bridge & Outlook (If Available)**

Some versions of Bridge LMS allow **direct calendar integration** with Outlook via **subscriptions**.

#### **Check if this feature is available in Bridge:**

1. In **Bridge**, go to your courses or events.
2. Look for an **"Add to Calendar"** or **"Subscribe to Calendar"** option.
3. If available, it will provide a **calendar subscription link (URL)**.
4. In **Outlook**, go to:
    - **Settings > View all Outlook settings > Calendar > Shared calendars > Add a calendar**.
    - Choose **From the Internet** and paste the URL.

This will keep all Bridge events **automatically updated** in Outlook.

---

### **6. Check If SharePoint Is Redirecting Files**

If SharePoint is **forcing ICS files to open in the browser**, your IT policy may be affecting file handling.

#### **Fix: Try Opening in a Private/Incognito Window**

- Open **Bridge in an Incognito window** and try downloading the ICS file.
- If it downloads correctly, then **SharePoint policies** may be interfering.

---

### **Final Steps**

✅ **Try manually importing the ICS file into Outlook.**  
✅ **Change the default app for ICS files to Outlook.**  
✅ **Download the ICS file directly (not opening in SharePoint).**  
✅ **Check if Bridge allows direct calendar sync.**  
✅ **Try an incognito window to bypass SharePoint’s redirects.**

If the issue persists, let me know **how Bridge is presenting the download** and whether you are using **Outlook desktop or web**. 🚀