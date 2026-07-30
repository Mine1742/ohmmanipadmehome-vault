# Resetting Linux VM Passwords and Fixing GNOME Keyring Issues in VirtualBox

This guide provides step-by-step instructions to regain access to Ubuntu or Linux Mint virtual machines (VMs) in Oracle VirtualBox when you’ve forgotten your login password or encounter GNOME Keyring password mismatch pop-ups.

---

## 1. Resetting a Forgotten Login Password

If you cannot log into your VM because you forgot your password:

1. **Boot into GRUB Menu**  
   - Start the VM and immediately hold **Shift** (or **Esc** for UEFI) to access the GRUB menu.

2. **Select Recovery Mode**  
   - From the list, choose:  
     `Advanced Options → <kernel version> (recovery mode)`

3. **Drop to Root Shell**  
   - In the recovery menu, select **root – Drop to root shell prompt**.

4. **Remount Filesystem as Read/Write**  
   ```bash
   mount -o rw,remount /
   ```

5. **Change Your User Password**  
   Replace `<username>` with your actual account name:
   ```bash
   passwd <username>
   ```
   Enter the new password twice.

6. **Reboot**  
   ```bash
   reboot
   ```

You can now log in using the new password.

---

## 2. Fixing GNOME Keyring Password Mismatch

If you log in successfully but get the pop-up:

> *Authentication required: The password you use to log in to your computer no longer matches that of your login keyring.*

This means your **keyring password** is still set to your *old* login password.

### Option A: If you remember your old password
- Enter your old password into the dialog.  
- Use **Seahorse (Passwords and Keys)** to change the keyring password so it matches your current login password:
  ```bash
  sudo apt install seahorse
  ```
  Open *Passwords and Keys → Right-click Login → Change Password*.

### Option B: If you don’t remember your old password
1. Boot into **Recovery Mode** and select **root shell**.

2. Navigate to your user’s keyring folder:
   ```bash
   ls /home
   cd /home/<username>/.local/share/keyrings/
   ```

3. Remove the old keyring files:
   ```bash
   rm *.keyring
   rm *.kdbx
   ```

4. Reboot:
   ```bash
   reboot
   ```

5. Log back in. A new keyring will be created tied to your current login password. The pop-up will no longer appear.

⚠️ Note: Saved Wi-Fi passwords and stored secrets will be lost, but they can be re-entered when prompted.

---

## 3. Summary
- **Forgot login password?** Reset it via GRUB recovery root shell with `passwd <username>`.  
- **Keyring mismatch?** Delete `~/.local/share/keyrings/*` or update it via Seahorse.  

Both fixes ensure you regain smooth access to your Ubuntu or Mint VM in VirtualBox.

---

### External Resources
- [Ubuntu Community Help on Keyring](https://help.ubuntu.com/community/GnomeKeyring)
- [VirtualBox User Manual](https://www.virtualbox.org/manual/UserManual.html)

---

#tags/linux #ubuntu #mint #virtualbox #password #keyring #troubleshooting

