---
categories: [security-practices]
domains: [backend]
---

# Breach & Attack Simulation (adversary emulation vs controls)

**MAY** automate adversary emulation (BAS) to continuously replay known TTPs against controls, but only in environments with tested rollback and blast-radius limits.

**Why:** Point-in-time tests decay; continuous emulation catches control regressions — unbounded, it can itself cause outages.

**Detect:** BAS tool configs (SafeBreach, AttackIQ, Atomic Red Team), `atomic-red-team` in CI, simulation schedules with rollback plans

**References:** MITRE ATT&CK, Gartner BAS category, Atomic Red Team (T1059 etc.)

---

**Part of:** [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
