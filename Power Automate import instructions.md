# Notify-Me-Mentions-Replies-IT-Software-Licensing Flow

This document explains how to import, configure, and test the Power Automate flow that notifies you whenever:
- Someone types **Albert Smith** in a Teams channel message,
- Someone @mentions **Albert Smith**, or
- Someone replies to one of your own posts.

The flow is scoped to the **IT Software Licensing** Team and all of its subchannels (General, Google Workspace, Trimble Accubid 16, etc.).

---

## 📥 Import the Flow Package
1. Download the file:  
   `Notify-Me-Mentions-Replies-IT-Software-Licensing.zip`

2. Go to [Power Automate](https://make.powerautomate.com).

3. In the left navigation, select **My flows**.

4. At the top, click **Import**.

5. Upload the `.zip` file.

---

## 🔧 Configure After Import
1. On the import screen, you’ll see the flow name:  
   **Notify-Me-Mentions-Replies-IT-Software-Licensing**

2. Under **Connections**, click the ⚠️ warning icon and select **Microsoft Teams**.  
   - Choose **+ Create new** if prompted.  
   - Sign in with your ArchKey Teams account.

3. Click **Import**.

4. After import completes, click into the flow and verify:  
   - **Team** = *IT Software Licensing*  
   - **Channel** = *All Channels*  
   - Your display name **Albert Smith** is already embedded in the conditions.

---

## ▶️ Turn On the Flow
1. In **My flows**, locate the new flow.  
2. Toggle the switch **On**.  

---

## 🧪 Test the Flow
1. In Teams, go to the **IT Software Licensing** team.  
2. Post a new message in **General** with:  
   - `Albert Smith` (plain text)  
   - `@Albert Smith` (mention)  
3. Reply to one of your own posts.  

You should receive a **Flow bot message in Teams chat** with:
- Sender’s name,  
- The message text,  
- A clickable **View in Teams** link.  

---

## ✅ Notes
- Flow only monitors the **IT Software Licensing** team and all its subchannels.  
- If your Teams display name changes, you must edit the flow and update `"Albert Smith"`.  
- If you want to expand this to other Teams later, duplicate the flow and change the Team scope.  

---

