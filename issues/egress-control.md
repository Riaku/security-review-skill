---
categories: [cloud-network, containers-k8s]
domains: [infrastructure]
---

# Egress Control (outbound traffic allow-listed; exfil paths narrowed)

**SHOULD** restrict outbound traffic to an explicit allow-list so compromised hosts cannot freely phone home or exfiltrate.

**Why:** Default-open egress is the exfiltration highway: malware, reverse shells, and data staging all reach arbitrary endpoints.

**Detect:** grep `NetworkPolicy` egress rules, `egress gateway`, proxy allow-lists, `default-deny` outbound rules.

**References:** NIST SP 800-207 Zero Trust, CIS Control 12, MITRE ATT&CK TA0011

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
