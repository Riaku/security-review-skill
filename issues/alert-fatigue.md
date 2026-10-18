---
categories: [observability]
domains: [reliability]
---

# Alert Fatigue

**MUST NOT** page humans for alerts that are routinely ignored or auto-resolved without action.

**Why:** Operators drowning in noise stop responding entirely, so the one genuine breach notification arrives inside a wall of dismissed noise.

**Detect:** review alert manager for rules with high fire-to-ack ratio, no `runbook_url`, or silence patterns; grep for `for: 0m` thresholds and catch-all severity mappings.

**References:** Google SRE Workbook alerting chapter, PagerDuty alert fatigue guidance, NIST SP 800-61

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
