---
categories: [compliance-privacy]
domains: [governance]
---

# Data Portability Export Mechanics

**SHOULD** provide a complete, machine-readable export of a user's data (JSON/CSV) covering all stores where they appear, generated within the regulatory SLA.

**Why:** Portability requests (GDPR Art. 20) that return only the primary profile row are non-compliant; building the export under a 30-day clock without pre-built tooling fails.

**Detect:** review export tooling coverage vs datastore inventory; check export includes activity/logs/derived records per policy; verify self-service export exists and is access-controlled (export = bulk data risk).

**References:** GDPR Art. 20 data portability, Google Takeout architecture talks, DSAR platform docs

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
