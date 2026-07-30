
# PowerDB Setup Guide
tags: #powerdb #software-setup #electrical-testing #asset-management

## Editions
- **PowerDB Lite**  
  - Free, supports only [Megger](https://megger.com/) instruments.  
  - Works on Windows Vista–11.  
  - [Lite Edition Overview](https://www2.powerdb.us/index.php?Itemid=112&id=9&option=com_content&view=article)

- **PowerDB Advanced**  
  - Licensed version with full form library and file-based data storage.  
  - [Advanced Edition Details](https://www2.powerdb.us/index.php?Itemid=104&id=9&layout=blog&option=com_content&view=category)

- **PowerDB Pro**  
  - Full enterprise version with SQL backend, centralized database, and advanced features.  
  - [Pro Edition Overview](https://www2.powerdb.us/index.php?Itemid=126&id=23&option=com_content&view=article)

---

## Download & Install
1. Visit [PowerDB Downloads → Installs](https://www2.powerdb.us/index.php?Itemid=106&catid=2&option=com_jdownloads&view=category).
2. Download the latest version (e.g., **11.3.8**, June 5, 2025).
3. Unzip the downloaded package fully.
4. Run `setup.exe` as **Administrator** (right-click → Run as Administrator).

---

## Licensing
- **Hardware dongle**: Insert USB dongle before launching the app.
- **Soft key**:  
  - Go to **Tools → PowerDB Licensing**.  
  - Enter your license serial number and contact info.  
  - Click **"License Online"** for activation.  
- Without licensing, PowerDB operates in **Reader Mode**.
- [Licensing Guide PDF](https://www.powerdb.com/download/powerdb/help/powerdb_users_manual.pdf)

---

## Initial Configuration
1. Log in as `administrator`.
2. Select **Application Style**:  
   - `Asset Owner` or `Testing Company`.  
   - This is a one-time setup.
3. Configure your **Master Database** and user accounts.
4. For teams:  
   - Create **Field Databases** for remote/portable use.
   - Set user permissions and synchronize jobs.
5. For upgrades:  
   - Ensure all users are logged out.  
   - Install updates on all machines (Master + Field databases).

---

## Forms & Instruments
- PowerDB includes **300+ built-in forms** for common electrical testing.
- Modify or create forms using the **Form Editor**.
- Integrates with various electrical test instruments:  
   - Lite Edition supports only [Megger](https://megger.com/) tools.

---

## Training & Support
- **Training options**:  
   - 2-day basic and 4-day form design courses.  
   - Delivered onsite, remotely, or at the Texas HQ.  
   - NETA CTDs available.
- **Support Resources**:  
   - [Downloads & Documentation](https://www2.powerdb.us/index.php?Itemid=150&catid=4&option=com_jdownloads&view=category)  
   - [Doble Support Portal](https://www.doble.com/support/downloads/)  
   - Includes manuals, drivers, and upgrade packages.
- Extended Support includes phone/email support and software updates.  
   - [Extended Support Details](https://www2.powerdb.us/index.php?Itemid=105&id=10&layout=blog&option=com_content&view=category)

---

## ✅ Tips
- Always back up your databases before upgrades.
- Coordinate updates in multi-user setups to prevent database lockouts.
- For assistance, refer to the [PowerDB User Manual (PDF)](https://www.powerdb.com/download/powerdb/help/powerdb_users_manual.pdf).

---

## Related KB Entries
- [[Megger Device Setup]]
- [[SQL Server Setup for PowerDB]]
- [[Electrical Test Form Customization]]
