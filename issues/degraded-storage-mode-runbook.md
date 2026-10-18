---
categories: [scaling-capacity, sre-incidents]
domains: [reliability]
---

# Storage Operating Degraded (Degraded RAID/Mirror) Runbook

**MUST** provide a runbook for degraded RAID/mirror states: rebuild procedure, performance limits, escalation threshold.

**Why:** A degraded mirror silently loses redundancy; the next disk failure becomes an unrecoverable array collapse.

**Detect:** `mdadm --detail` showing `degraded`, `zpool status` DEGRADED, absence of `degraded` runbook, no rebuild-priority or scrub schedule.

**References:** NIST SP 800-34, RAID recovery procedures, ZFS administration guide, CWE-190

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
