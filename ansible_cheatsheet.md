# 🧩 Ansible Cheat Sheet

Command and playbook reference for configuration management, automation, and infrastructure orchestration.

---

## ⚙️ SETUP & BASICS

```bash
ansible --version
ansible all -m ping                    # Test all hosts
ansible-inventory --list               # Show inventory details
ansible-config view                    # Show current configuration
```

### **Inventory Example**
`inventory.ini`
```
[web]
web1 ansible_host=192.168.1.10
web2 ansible_host=192.168.1.11

[db]
db1 ansible_host=192.168.1.12
```

---

## 🚀 AD-HOC COMMANDS

```bash
ansible all -m ping
ansible all -m shell -a "uptime"
ansible web -m yum -a "name=httpd state=present"
ansible db -m service -a "name=mysql state=started"
ansible all -a "df -h"
```

---

## 🧱 PLAYBOOK STRUCTURE

`site.yml`
```yaml
---
- name: Deploy Web Server
  hosts: web
  become: yes
  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present

    - name: Start Apache
      service:
        name: httpd
        state: started
```

### **Run Playbook**
```bash
ansible-playbook site.yml
```

---

## 🧮 VARIABLES & FACTS

### **Defining Variables**
`group_vars/web.yml`
```yaml
http_port: 80
server_name: webserver
```

Use in tasks:
```yaml
- name: Print variable
  debug:
    msg: "Server {{ server_name }} listening on port {{ http_port }}"
```

### **Gather Facts**
```bash
ansible all -m setup
```

---

## 🔁 LOOPS & CONDITIONS

```yaml
- name: Install multiple packages
  yum:
    name: "{{ item }}"
    state: present
  loop:
    - git
    - vim
    - curl

- name: Restart service only if updated
  service:
    name: nginx
    state: restarted
  when: ansible_os_family == "RedHat"
```

---

## 🧩 ROLES

```bash
ansible-galaxy init webserver
ansible-galaxy install geerlingguy.mysql
```

### **Role Directory Structure**
```
roles/
  webserver/
    tasks/
    handlers/
    templates/
    files/
    vars/
```

### **Including Role**
```yaml
- hosts: web
  roles:
    - webserver
```

---

## 🧾 HANDLERS

Used to perform actions only when notified.

```yaml
tasks:
  - name: Update config
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/httpd.conf
    notify: Restart Apache

handlers:
  - name: Restart Apache
    service:
      name: httpd
      state: restarted
```

---

## 🧠 TEMPLATES (Jinja2)

`index.html.j2`
```html
<html>
  <h1>Welcome to {{ inventory_hostname }}</h1>
</html>
```

`tasks/main.yml`
```yaml
- name: Deploy index.html
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

---

## 🔐 ANSIBLE VAULT

```bash
ansible-vault create secrets.yml
ansible-vault view secrets.yml
ansible-vault edit secrets.yml
ansible-vault encrypt site.yml
ansible-vault decrypt site.yml
```

Use with playbook:
```bash
ansible-playbook site.yml --ask-vault-pass
```

---

## 🧩 TAGS & LIMITS

```bash
ansible-playbook site.yml --tags "setup,deploy"
ansible-playbook site.yml --skip-tags "debug"
ansible-playbook site.yml --limit web1
```

---

## 📦 COLLECTIONS & GALAXY

```bash
ansible-galaxy collection list
ansible-galaxy collection install community.general
ansible-galaxy role install geerlingguy.apache
```

---

## 🪄 QUICK REFERENCE SUMMARY

| Task | Command |
|------|----------|
| Test all hosts | `ansible all -m ping` |
| Run playbook | `ansible-playbook site.yml` |
| Install package | `ansible all -m yum -a "name=git state=present"` |
| Encrypt file | `ansible-vault encrypt secrets.yml` |
| Use tags | `ansible-playbook site.yml --tags "deploy"` |
| List inventory | `ansible-inventory --list` |

---

## 💡 TIPS

- Use `--check` flag for dry-run testing.  
- Use `--diff` to see configuration differences.  
- Keep secrets in **Vault**, not Git.  
- Combine with **Terraform** or **Docker** for full automation.  
- Add `become: yes` for privilege escalation.  
- Group related roles in **collections** for modular reuse.

---

**Created for:** system configuration and DevOps orchestration  
**By:** Albert Smith’s Knowledge Base  
**Tags:** #ansible #automation #devops #infrastructure #iac #configuration
