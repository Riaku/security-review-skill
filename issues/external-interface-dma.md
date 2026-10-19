---
categories: [hardening-benchmarks]
domains: [infrastructure]
---

# DMA From External Interfaces

**MUST** confine external high-bandwidth interfaces — Thunderbolt, PCIe, USB4 — behind an IOMMU so a rogue peripheral cannot read or write host memory directly.

**Why:** A device plugged into a DMA-capable port operates below the OS, where no driver or endpoint agent can see it.

**Detect:** dmesg | grep -i iommu to confirm an active IOMMU domain, plus the firmware DMA-protection setting

**References:** awesome-firmware-security, https://github.com/PreOS-Security/awesome-firmware-security
