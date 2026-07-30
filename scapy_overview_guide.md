# Scapy Overview and Guide

## 🧠 What is Scapy?

**Scapy** is a powerful Python-based tool for crafting, sending, sniffing, and dissecting network packets. It is widely used in cybersecurity, network testing, and protocol development.

---

## 🧰 What Can You Do with Scapy?

| Category            | Description                                       |
|---------------------|----------------------------------------------------|
| 📦 Packet Crafting   | Create custom IP/TCP/UDP/ICMP packets             |
| 🕵️ Packet Sniffing   | Capture and analyze network traffic               |
| 🔬 Packet Dissection | View detailed protocol fields                     |
| 🛠 Protocol Testing  | Send malformed packets to test stack resilience   |
| 🔥 Network Scanning  | Perform ARP scans, SYN scans, traceroutes         |
| 🧪 IDS Testing       | Simulate attacks to test firewalls or detection systems |

---

## ⚙️ Installation

### 🐍 Prerequisites:
- Python 3.6+
- `pip` package manager
- Root or admin privileges for sending/sniffing packets

### ✅ Install Scapy

```bash
pip install scapy
```

Or for the full feature set:

```bash
pip install --pre scapy[basic]
```

### 💡 Optional Dependencies for Advanced Features

- `tcpdump` (for sniffing on Linux/macOS)
- `libpcap` or `WinPcap/Npcap` (for packet capture)
- Graphing support: `matplotlib`, `pyx`

---

## 🚀 Getting Started with Scapy

### 🧪 Crafting and Sending a Packet

```python
from scapy.all import *

# ICMP Echo Request to 8.8.8.8
packet = IP(dst="8.8.8.8")/ICMP()
send(packet)
```

### 📡 Sniff Network Traffic

```python
packets = sniff(count=10)
packets.summary()
```

### 🔍 Customizing Packets

```python
pkt = IP(dst="1.1.1.1", ttl=64)/TCP(dport=80, flags="S")
pkt.show()
```

---

## 🧬 Scapy Protocol Layers

You can stack protocol layers like building blocks:

```python
Ether()/IP()/TCP()
```

- View fields with `show()`
- Modify fields by assigning: `pkt[IP].ttl = 128`

---

## 🖥 Launch Scapy Console (Optional)

```bash
sudo scapy
```

You'll enter an interactive Python-like shell preloaded with Scapy functions.

---

## ⚠️ Tips and Warnings

- Run as **root** (or admin) to send or sniff packets.
- Works best on **Linux/macOS**; Windows requires additional setup (Npcap).
- Scapy does **not** use the OS TCP/IP stack — it's fully custom packet handling.

---

## 🔍 When to Use Scapy

| Use Case                  | Why Use Scapy                            |
|---------------------------|------------------------------------------|
| Penetration Testing       | Test how firewalls and routers behave    |
| Protocol Research         | Inspect field-level behavior manually    |
| Network Troubleshooting   | Send crafted test packets                |
| Education/Labs            | Learn OSI model and packet structures    |

---

## 📚 Resources

- [Scapy Docs](https://scapy.readthedocs.io)
- [GitHub Repo](https://github.com/secdev/scapy)

