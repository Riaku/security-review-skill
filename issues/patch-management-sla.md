---
categories: [cicd-pipeline-security, security-practices]
domains: [backend, infrastructure]
---

# Patch management SLAs (MTTR targets by severity, exception tracking)

**MUST** define mean-time-to-remediate targets per severity (critical 24h, high 30d, medium 90d) and log every exception with owner and expiry date.

**Why:** Undated exceptions silently become permanent debt; SLA clocks make drift visible and auditable.

**Detect:** `sla` / `mttr` keys in policy docs, `waiver` / `exception` tracker files with `expires` fields

**References:** NIST SP 800-40 Rev.4, CIS Control 7, PCI DSS 6.3.3

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
