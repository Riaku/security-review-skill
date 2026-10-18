---
categories: [observability]
domains: [reliability]
---

# Beaconing Detection

**MUST** analyze outbound connection timing for fixed-interval patterns that indicate C2 beaconing.

**Why:** Compromised hosts calling home on rigid schedules (every 60s ± jitter) are a hallmark of implant traffic that volume-based alerts never flag.

**Detect:** grep SIEM for inter-arrival variance / jitter analysis queries over flow logs; check NetFlow/Egress rules bucket connection periodicity per destination.

**References:** MITRE ATT&CK T1071, T1029 Scheduled Transfer, CWE-358, Mandiant beaconing detection guidance

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
