[[Printer Hub]]
# 🖨️ Printer Stuck in Landscape Mode (Resolved)

## 📅 Date Logged
2025-05-21

## 💻 Device Context
- **Laptop**: New setup
- **Issue**: Printer only prints in *landscape* even when *portrait* is selected.
- **Previous Occurrence**: Same issue appeared after original install.

---

## 🧩 Symptoms
- All print jobs default to **landscape orientation**
- **Portrait** is selected in:
  - Application print dialog (e.g., Word, Adobe, Chrome)
  - Printer driver properties

---

## 🔍 Root Cause
The issue was due to a **default driver mismatch** or **incomplete setup** on a newly imaged or recently acquired laptop. When installing some plotters or multifunction printers, Windows may install a generic driver that doesn't properly manage orientation settings.

---

## 🛠️ Resolution Steps

1. **Check Driver Type**
   - Go to **Control Panel > Devices and Printers**
   - Right-click the printer → **Printer Properties**
   - Under **Advanced tab**, verify driver name.
   - ✅ If it says *Generic* or *Class Driver* → **Replace it**.

2. **Download OEM Driver**
   - Go to official printer website (e.g., Canon, Ricoh, HP).
   - Locate the exact model (e.g., Canon imagePROGRAF TZ-30000).
   - Download and install **Full Feature Driver or PPD**.

3. **Set Printer Defaults**
   - In **Devices and Printers**, right-click printer → **Printing Preferences**
   - Set **default orientation** to **Portrait**
   - Save and apply.

4. **Application-Specific Overrides**
   - Restart printing application (Word, Chrome, etc.)
   - Re-check orientation is set to Portrait

5. **Test Print**
   - Print a test page from multiple applications
   - ✅ Confirmed portrait prints correctly

---

## 📌 Notes
- Some new laptops install "Microsoft IPP Class Driver" or "AirPrint" by default, which limits full feature access.
- If persistent, remove printer completely and reinstall using downloaded OEM driver.

---

## ✅ Status
**Resolved** — Portrait printing restored by replacing driver with official manufacturer version.
