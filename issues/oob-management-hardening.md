---
categories: [cloud-network]
domains: [infrastructure]
---

# Out-of-Band Management Hardening

**MUST** network-isolate baseboard and out-of-band management interfaces, replace their default credentials, and patch them on the same cadence as the hosts they control.

**Why:** Management processors sit below the operating system with network reachability, so one weak BMC credential is a lateral path past every host control.

**Detect:** nmap -sU -p623 --script ipmi-cipher-zero,ipmi-version <management-cidr>; firewall rules exposing 623/udp beyond the admin jump host

**References:** PreOS awesome-firmware-security, https://github.com/PreOS-Security/awesome-firmware-security
