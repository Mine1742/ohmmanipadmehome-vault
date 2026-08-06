#network

How to figure out what kind of device is behind an IP/MAC on the network, from quick-and-dirty to fairly reliable.

Basic reachability
	`ping <ip>` confirms it's alive. TTL can hint at OS: Windows defaults to TTL 128, Linux/most Unix/IoT to TTL 64, some network gear (Cisco) to TTL 255. User-configurable, so only a loose clue.

MAC address to vendor
	`arp -a` grabs the MAC address. Look up the OUI (first 6 hex digits) against the IEEE vendor database to get the manufacturer (e.g. Espressif = likely IoT/ESP32, Apple = iPhone/Mac, Raspberry Pi Foundation, a NAS or camera vendor). Most router admin pages already do this lookup and label devices for you.

Port/service scan (most informative)
	[nmap](https://nmap.org/) is the standard tool.
	`nmap -sV -O <ip>` — `-O` attempts OS fingerprinting (needs admin/root, not always accurate against modern stacks); `-sV` grabs service banners on open ports, which often reveal the device directly (port 9100 = printer, port 8009/8443 = Chromecast, port 62078 = iOS device, a web UI on 80/443 identifying itself as Synology/Hikvision/etc.)
	`nmap -sn 192.168.1.0/24` sweeps the whole subnet for live hosts first, then target unrecognized ones individually.

Easiest option for a home/office LAN
	Router client list, or a tool like Fing, or a UniFi/pfSense/OPNsense dashboard — these usually do the MAC-vendor lookup and hostname/DHCP-name matching automatically, no CLI needed.
