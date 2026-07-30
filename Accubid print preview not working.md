#accubid 

Moved Roaming data for Change Order Pro into new local profile:
{Username]\AppData\Roaming\Accubid\ChangeOrder Pro 14\Settings

Restarted Change Order Pro





### 1. **Error: Missing Screen Style**

- **Cause**: The report is configured to use a "Screen Style" (layout) that is not available or not set.
- **Solution**:
    1. Go to **Settings > Screen Styles**.
    2. Check if the **Itemized Breakdown: Client Default** style exists.
    3. If it doesn’t exist, select an available screen style or create a new one with a compatible layout.
    4. Save your changes and try printing or previewing the report again.

---

### 2. **Error: No Data or Reports Selected**

- **Cause**: The system is unable to find data to print or the selected report isn’t configured correctly.
- **Solution**:
    1. Verify that the report contains valid data:
        - Go to the **Takeoff** or relevant tab and confirm that items are properly entered with quantities, costs, etc.
    2. Confirm that the selected report is active:
        - Go to **Job > Print Reports** or **Job > Print Preview**.
        - Choose a report template and ensure it matches the data you want to print.
    3. Verify print settings:
        - In the print dialog, confirm that the number of copies is set to at least 1.
        - Check the print range to ensure the selected data is included.

---

### 3. **Printing to PDF or Preview**

- **To Print to PDF**:
    1. Select **Job > Print Reports**.
    2. In the print dialog, choose **Microsoft Print to PDF** (or any installed PDF printer).
    3. Save the output as a PDF.
- **To Use Print Preview**:
    1. Select **Job > Print Preview**.
    2. If errors persist, double-check the selected report template and data.

---

### 4. **General Troubleshooting Tips**

- **Reassign Report Style**:
    - Go to **Settings > Project Defaults** or **Settings > Global Defaults** and reassign a working report style.
- **Verify Database Location**:
    - Check if the database containing the report templates is accessible and properly linked.
- **Update the Software**:
    - Ensure you are using the latest version of ChangeOrder Pro 14 to avoid compatibility issues.

---

Let me know if you encounter further challenges, and I can provide more detailed steps!