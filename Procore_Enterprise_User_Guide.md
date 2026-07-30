# Procore Enterprise User Guide & Account Setup

## 1. Overview
Procore is a cloud-based construction project management platform that helps organizations manage projects, resources, and financials from planning to completion. In an enterprise setup, accounts are centrally managed by IT/Admins to ensure consistent security, permissions, and project structure.

---

## 2. Account Setup for Enterprise Organization

### Step 1: Admin Console Access
1. Navigate to [Procore Login](https://login.procore.com).
2. Sign in with your admin credentials.
3. Access the **Company Admin Tool** from the top-level navigation.

---

### Step 2: Enterprise Configuration
- **Company Profile**: Enter organization name, logo, and contact details.
- **Regions/Divisions**: Define business units or divisions for organizational hierarchy.
- **Default Project Settings**: Establish naming conventions, default cost codes, and workflows.

---

### Step 3: Identity & Access Management
1. **SSO Integration (Recommended for Enterprise)**  
   - Configure SAML/SCIM for Azure AD, Okta, or another IdP.  
   - Test SSO login with a pilot group.  
2. **Multi-Factor Authentication (MFA)**  
   - Enforce MFA at the enterprise level for all users.  
3. **Role-Based Access Control (RBAC)**  
   - Define standard roles (e.g., Project Manager, Superintendent, Subcontractor, Finance).  
   - Map Procore permissions templates to roles.  

---

### Step 4: User & Group Creation
1. **Bulk Import Users** (via CSV template):  
   - Required fields: First Name, Last Name, Email, Company, Role, Permission Template.  
2. **Create Distribution Groups**:  
   - Examples: “Project Managers East”, “Superintendents West”, “Finance Team”.  
   - Assign groups to projects for quick communication and permissions.  

---

### Step 5: Project Templates
1. Create **Enterprise Project Templates** that include:  
   - Standard folder structures for documents.  
   - Default cost codes and budget templates.  
   - RFI, Submittal, and Change Event workflows.  
2. Apply templates when spinning up new projects to maintain consistency.  

---

## 3. User Login & Setup Guide (End Users)

### Step 1: Accessing Procore
- URL: [https://login.procore.com](https://login.procore.com)  
- Select **Company** (if part of multiple organizations).  
- Log in with:
  - **SSO** (preferred) → Use company email + network password.  
  - **Procore Account** (if provisioned separately) → Use email + password.  

---

### Step 2: Setting Up Your Profile
1. Click on your name (top-right corner) → **My Profile Settings**.  
2. Update:  
   - Contact information (email, phone, title, trade).  
   - Time zone and notification preferences.  
   - Profile photo (recommended for site teams).  

---

### Step 3: Notifications & Preferences
- Enable or disable **email notifications** for:  
  - RFIs, Submittals, Observations, Daily Logs.  
- Set **mobile push notifications** if using iOS/Android app.  

---

### Step 4: Installing the Procore App
- **Desktop Access**: Any modern browser (Chrome, Edge, Safari).  
- **Mobile Access**: Download “Procore” app from iOS App Store or Google Play.  
- Sign in with the same enterprise credentials (SSO or Procore login).  

---

### Step 5: Getting Started with Projects
- Upon login, you’ll see **Projects Dashboard**.  
- Select assigned project(s).  
- Navigate modules:  
  - **Home** → Overview of project activity.  
  - **Drawings** → Access latest plans.  
  - **Documents** → Centralized file repository.  
  - **RFIs/Submittals** → Submit and respond.  
  - **Daily Logs** → Site reporting.  

---

## 4. Best Practices for Enterprise Users
- Always log in via **SSO** to ensure security.  
- Use **Project Templates** to avoid reinventing workflows.  
- Set **default permissions via templates** to maintain compliance.  
- Train users on **mobile app offline mode** for fieldwork.  
- Leverage **dashboards and reporting tools** for executive insights.  

---

## 5. Support & Resources
- **Internal IT/Procore Admins**: [Insert company contact info]  
- **Procore Support**: [https://support.procore.com](https://support.procore.com)  
- **Procore Learning Portal**: [https://learn.procore.com](https://learn.procore.com)  

---

#tags/procore #tags/setup #tags/userguide
