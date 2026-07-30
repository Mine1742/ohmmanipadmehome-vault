[[Windows Hub]]
# 🛠 Bootable USB Installer Guide for Windows and Linux

Use this guide to create a bootable USB installer for a computer with no operating system.

---

## 🟦 Windows 10/11 Bootable USB Installer

### ✅ Requirements
- USB flash drive (8 GB or more)
- Another computer with internet access

### 🔹 Steps

1. Go to the official Microsoft download page:
   - [Windows 11](https://www.microsoft.com/software-download/windows11)
   - [Windows 10](https://www.microsoft.com/software-download/windows10)

2. Click **"Download now"** under “Create Windows Installation Media.”

3. Run the **Media Creation Tool** and:
   - Choose **"Create installation media (USB flash drive)"**
   - Select your preferred language and Windows edition
   - Choose your USB drive from the list
   - Wait for the tool to download Windows and create the installer

4. Insert the USB into the PC with no OS.

5. Power on the PC and press the **boot menu key** (often `F12`, `ESC`, or `F2`)

6. Select the USB drive and proceed with Windows setup

---

## 🐧 Linux (Ubuntu) Bootable USB Installer

### ✅ Requirements
- USB flash drive (4 GB or more)
- Tool like [Rufus](https://rufus.ie)
- Another computer with internet

### 🔹 Steps

1. Download a Linux ISO (e.g., Ubuntu):
   - [https://ubuntu.com/download/desktop](https://ubuntu.com/download/desktop)

2. Download and open **Rufus**:
   - [https://rufus.ie](https://rufus.ie)

3. In Rufus:
   - Select your USB drive
   - Click "SELECT" and choose the downloaded ISO
   - Leave other settings as default (GPT, UEFI)
   - Click **Start** and wait for completion

4. Insert the USB into the PC with no OS

5. Power on and press the **boot menu key** (`F12`, `ESC`, `F2`, etc.)

6. Select the USB drive and proceed with Linux setup

---

## 🧠 Tips

- Always **safely eject** the USB after creation
- For best compatibility, enable **UEFI mode** in BIOS
- Windows setup will allow you to format partitions during installation

---
