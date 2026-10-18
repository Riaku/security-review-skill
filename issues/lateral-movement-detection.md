---
categories: [cloud-network, observability]
domains: [infrastructure, reliability]
---

# Lateral Movement Detection (post-compromise horizontal motion in cloud/host)

**SHOULD** alert on post-compromise horizontal motion: unusual SSH/RDP hops, mass SMB enumeration, anomalous cross-account role assumption.

**Why:** Without motion alerts, dwell time stretches to months while one foothold becomes total compromise of crown jewels.

**Detect:** grep detection rules for `T1021`, `remote_services`, `admin_shares`, `pass-the-hash`, unusual-login Sigma/YARA-L rules.

**References:** MITRE ATT&CK TA0008/T1021, NIST SP 800-61, Sigma rules, GuardDuty UnauthorizedAccess

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
