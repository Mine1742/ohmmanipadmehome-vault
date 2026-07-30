---
title: "Convert DWG and Revit Files to PDF"
created: 2025-05-06
tags: [pdf, dwg, revit, plotting, autocad, printing]
aliases: [DWG to PDF, Revit to PDF, Print Drawings]
---
[[AutoDesk Hub]][[Autodesk]]
# 🖨️ How to Convert .DWG and Revit Files to PDF for Plotting

## 🔷 AutoCAD – Convert .DWG to .PDF

### 📌 Steps:
1. **Open the .dwg file** in AutoCAD.
2. **Switch to a Layout tab** (e.g., Layout1).
3. **Open the Plot dialog**:
   - Type `PLOT` or go to `Output` tab → `Plot`
4. **Set Printer/Plotter** to `DWG to PDF.pc3`.
5. **Select Paper Size** (e.g., ANSI D, ARCH E1).
6. **Choose Plot Area**:
   - Select `Layout` or `Window` and define the area.
7. **Set Plot Scale** (usually 1:1).
8. **Choose Plot Style Table**:
   - `monochrome.ctb` for black-and-white output.
9. **Preview** and click `OK` to generate the PDF.
10. **Save the file** to your preferred location.

### 🔁 Batch PDF Export:
- Use `PUBLISH` command in AutoCAD to batch plot multiple DWGs.

---

## 🟣 Revit – Export Sheets/Views to PDF

### 📌 Print Method:
1. **Open Revit project (.rvt)**.
2. Go to `File` → `Print` → `Print` (or `Ctrl + P`).
3. Choose a PDF printer:
   - `Microsoft Print to PDF`, `Adobe PDF`, etc.
4. **Select Sheets/Views** to export.
5. Adjust settings:
   - Page size, orientation, print range
   - Zoom: `100%` or `Fit to Page`
6. **Click Print** and save the resulting PDF.

### 🗃 Export via Built-in Revit PDF Exporter (2022+):
1. Go to `File` → `Export` → `PDF`.
2. Select multiple sheets/views.
3. Customize file naming (e.g., `<Sheet Number>_<Sheet Name>`).
4. Click `Export`.

---

## ⚠️ Notes
- Revit uses **View Templates** and **Visibility/Graphics (VG)** for line control, not `.ctb` files.
- AutoCAD supports plot styles and drawing scale more directly.

---

## 🧰 Tools for Automation
- **Revit Plugins**: [Diroots SheetLink](https://diroots.com) or **RTV Tools** for advanced batch plotting.
