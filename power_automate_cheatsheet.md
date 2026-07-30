# 🤖 Power Automate Cheat Sheet

Essential guide for building, managing, and troubleshooting Power Automate (Cloud & Desktop) flows.

---

## ☁️ POWER AUTOMATE CLOUD BASICS

### **Core Concepts**
- **Flow** – a sequence of automated actions triggered by an event.  
- **Trigger** – starts a flow (e.g., email received, file created).  
- **Action** – a task performed by the flow (e.g., send email, update row).  
- **Connector** – service integration (e.g., Outlook, SharePoint, Teams, SQL).  

---

## 🚀 COMMON FLOW TYPES

| Flow Type | Description | Example |
|------------|--------------|----------|
| Automated | Runs when a trigger event occurs | Send Teams alert on new email |
| Instant | Triggered manually | Click button to start workflow |
| Scheduled | Runs on a timer | Daily report at 7 AM |
| Business process | Step-by-step guided flow | Approval process |

---

## 🔔 TRIGGERS

### Common Examples
- **Outlook:** *When a new email arrives*  
- **SharePoint:** *When a file is created*  
- **Forms:** *When a response is submitted*  
- **Planner:** *When a task is assigned to me*  
- **Manual:** *When a flow button is pressed*  
- **Scheduled:** *Recurrence – every 1 hour*

### Scheduled Flow Example
```plaintext
Recurrence -> Get items from SharePoint -> Create CSV -> Send via Outlook
```

---

## ⚙️ ACTIONS

### Common Actions
- **Outlook:** Send an email  
- **Teams:** Post a message in a channel  
- **OneDrive:** Create file / Move file  
- **SharePoint:** Get items / Update list item  
- **Excel:** Add row / Read table / Update cell  
- **HTTP:** Send API request  
- **Condition:** If-Else logic  
- **Apply to each:** Loop through data  

---

## 🧩 EXPRESSIONS & FUNCTIONS

```plaintext
concat('Hello ', triggerOutputs()?['body/From'])
formatDateTime(utcNow(), 'yyyy-MM-dd')
addDays(utcNow(), 7)
length(body('Get_items')?['value'])
equals(items('Apply_to_each')?['Status'], 'Completed')
```

💡 Tip: Always click the **fx** button to open the dynamic content expression editor.

---

## 🧮 VARIABLES & ARRAYS

```plaintext
Initialize variable: name=counter, type=Integer, value=0
Increment variable: counter + 1
Append to array: append(variables('ArrayVar'), 'new item')
Join array: join(variables('ArrayVar'), ', ')
```

---

## 🧱 CONDITIONS & LOOPS

**Condition Example**
```plaintext
If file size > 10MB  
   → Move to “Large Files” folder  
Else  
   → Process normally
```

**Apply to each Example**
```plaintext
Apply to each (items from Get Items)
   → Send email to item Owner
```

---

## 🧰 ERROR HANDLING

### Configure Run After
Allows continuation when previous step fails.

**Options:**
- has failed  
- has timed out  
- is skipped  

### Try-Catch Equivalent
```plaintext
Scope: Try → Catch → Finally
```

Use three Scopes with **Configure Run After** linking failures and successes.

---

## 💾 FILE & DATA OPERATIONS

### OneDrive / SharePoint
```plaintext
Create file → Folder: /Reports/, File Name: report.csv
Update file → Overwrite existing
Get file content → For attachment
```

### Excel Online (Business)
- Get rows from table  
- Add a new row  
- Update a cell value  
- Filter array with condition  

---

## 🧠 DESKTOP AUTOMATION (PAD)

### Launch & Record
1. Open **Power Automate Desktop**.  
2. Click *New Flow* → *Record Actions*.  
3. Add steps manually or record mouse/keyboard actions.  
4. Use *Variables Pane* to see runtime data.  

### Common PAD Actions
- Launch Excel / Read cell / Write cell  
- Web automation → extract text, click buttons  
- Run Command Prompt commands  
- Conditional logic and error handling  

---

## 🔐 CONNECTORS

| Connector | Example Usage |
|------------|----------------|
| SharePoint | Create or update list items |
| Outlook | Monitor or send emails |
| Teams | Post messages / send adaptive cards |
| Excel | Read or write table rows |
| Planner | Manage tasks |
| Dataverse | Interact with Dynamics data |
| HTTP | Call APIs / integrate with external systems |

---

## 📦 EXPORT, IMPORT & VERSIONING

```plaintext
Export flow as .zip package
Import flow to another environment
Use solutions for group management
Use comments & versions for documentation
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Action |
|------|---------|
| Send email on new SharePoint file | Trigger: SharePoint → Action: Send Email |
| Scheduled daily report | Trigger: Recurrence → Action: Excel/Email |
| Loop through items | “Apply to each” container |
| Error handling | Configure Run After |
| Desktop automation | Use Power Automate Desktop |
| Combine expressions | concat(), addDays(), formatDateTime() |

---

## 💡 TIPS
- Use **Run History** to debug failed flows.  
- Turn on **Concurrency Control** to limit simultaneous runs.  
- Name every step clearly for readability.  
- For complex logic, use **Scopes** with nested conditions.  
- Combine **Cloud** and **Desktop** flows for hybrid automation.

---

**Created for:** Cloud & Desktop Power Automate usage  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #powerautomate #automation #microsoft365 #flow #pad #cloud
