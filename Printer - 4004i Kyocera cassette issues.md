[[Printer Hub]]
# Printer - 4004i Kyocera Cassette Issues

Below is a guide to ensure your TASKalfa 4004i automatically pulls from Cassette 2 when printing ledger-size jobs, preventing manual error pop-ups.

---

## 1. Verify Cassette 2 Is Correctly Loaded & Configured

1. **Confirm Paper Size in Cassette 2**  
   - On the TASKalfa’s control panel, press **System Menu/Counter** ▶ **System** ▶ **Function Settings** (enter Administrator PIN if prompted).  
   - Go to **Tray Settings** ▶ **Cassette 2**.  
   - Ensure **Paper Size** is set to **Ledger (11" × 17")** or **11 × 17 (Tabloid/Ledger)**.  
   - Set **Paper Type** to a standard type (e.g., **Plain 1**).  
   - Adjust paper guides in Cassette 2 so they fit snug against the ledger paper.  

2. **Paper Level & Tray Status**  
   - Open Cassette 2 and verify sufficient ledger stock is loaded.  
   - Check the tray’s window: paper level should be above minimum.  
   - Fully re-insert the cassette until it clicks; a mis-seated tray will appear empty.

3. **Enable Auto Tray Switching (Machine Side)**  
   - In **Function Settings** ▶ **Tray Settings**, locate **Auto Tray Switching** (or **Auto Tray Select**).  
   - Set **Auto Tray Switching** to **On**.  
   - This instructs the printer to automatically look for the requested size in Cassette 2 instead of halting.

4. **Disable “Stop on Blank Paper” (Optional)**  
   - In **Function Settings** ▶ **Paper Error Alert**, set **Stop on Blank Paper** to **Off**.  
   - With this off, if Cassette 2 runs out, the printer will try the next source without stopping.

5. **Save & Exit**  
   - Press **OK** (or **Enter**) to save changes and exit.  
   - Confirm the machine shows “Ready” before testing.

---

## 2. Configure the Windows Driver for Ledger + Auto Tray Select

1. **Open Devices & Printers**  
   - Press **Windows + R**, type `control printers`, press **Enter**.  
   - Right-click **TASKalfa 4004i** → **Printing preferences**.

2. **Set Default Paper Size to Ledger**  
   - In **Paper/Output** tab, under **Paper Size**, select **Ledger (11 × 17)**.  
   - Leave **Source** set to **Auto Tray Select**; do not hard-set to Cassette 2.

3. **Disable Warnings in the Driver**  
   - Uncheck any options like **“Popup Alert when Paper Empty”** or **“Warn on Media Mismatch”**.  
   - This prevents the driver from interrupting jobs if Cassette 2 is not immediately available.

4. **Apply & Save**  
   - Click **Apply**, then **OK** to save preferences.

---

## 3. Test a Ledger Print Job

1. **Open a Test Document** (e.g., PDF with an 11" × 17" page).  
2. **Print Dialog**  
   - Ensure **Paper Size** = **Ledger (11 × 17)**.  
   - Confirm **Source** = **Auto Tray Select**.  
   - Click **Print**.

3. **Observe the Printer**  
   - The printer should automatically pull from Cassette 2 and start printing.  
   - If an error appears, revisit Section 1 to verify tray settings.

---

## 4. If You Still Get an Error Pop-Up

1. **Update Firmware**  
   - Older firmware may mishandle tray switching. Download latest for TASKalfa 4004i from Kyocera support and update via **Admin > System Menu > System > Update**.

2. **Override Source in the Application**  
   - In the application’s print dialog, manually set **Paper Source** to **Tray 2** and **Paper Size** to **Ledger**.  
   - This ensures the printer is explicitly instructed to use Cassette 2.

3. **Check Bypass Tray & Finisher Settings**  
   - In **Function Settings** ▶ **Tray Settings**, confirm **Bypass Tray** is set to **Any Size** or **Same as Cassette 2**.  
   - If the bypass is restricted, the printer may think Cassette 2 is empty and await bypass media.

4. **Confirm Paper Type/Thickness**  
   - If using heavy ledger stock, in **Tray Settings** ▶ **Cassette 2**, change **Paper Type** to **Thick1** or **Thick2** matching the stock.  
   - Test again after adjusting.

---

## 5. Summary Checklist

1. **Cassette 2 on the Machine**  
   - Loaded with ledger, guides set correctly.  
   - Tray’s **Paper Size** = **Ledger**, **Paper Type** correct.  
   - **Auto Tray Switching** = **On**, **Stop on Blank Paper** = **Off** (optional).

2. **Windows Driver**  
   - **Printing Preferences** → **Paper Size** = **Ledger**, **Source** = **Auto Tray Select**.  
   - Driver pop-up warnings disabled.

3. **Test Print Job**  
   - Select 11" × 17" and Auto tray; printer should pull from Cassette 2 without error.

4. **If Error Persists**  
   - Update firmware.  
   - Override source to Tray 2 in the app.  
   - Verify bypass/finisher settings.  
   - Adjust **Paper Type/Thickness** in tray settings.

---

Following these steps will ensure the TASKalfa 4004i automatically pulls from Cassette 2 for ledger jobs, preventing manual intervention.
