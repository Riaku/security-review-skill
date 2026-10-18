---
categories: [compliance-privacy, regulatory-frameworks]
domains: [governance, government-compliance]
---

# Breach notification clocks across jurisdictions

**MUST** detect and triage breaches fast enough to meet the strictest applicable notification deadline (72h GDPR, state laws).

**Why:** Missing statutory notification windows compounds breach penalties and destroys regulatory trust after an incident.

**Detect:** grep for incident response SLA timers, `notification_deadline`, `breach_clock` config; check monitoring-to-notification pipeline latency absent.

**References:** GDPR Art. 33, Cal. Civ. Code §1798.82, HIPAA Breach Rule 45 CFR 164.404, NIST SP 800-61
