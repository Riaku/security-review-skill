---
categories: [compliance-privacy]
domains: [governance]
---

# Data Portability Export Mechanics

**SHOULD** provide a machine-readable export (JSON/CSV) of the personal data the user provided and that is processed on consent or contract (GDPR Art. 20), plus a fuller access response covering all personal data held about them (Art. 15), both generated within the regulatory SLA.

**Why:** Portability requests (GDPR Art. 20) that return only the primary profile row are non-compliant; building the export under the one-month statutory clock (Art. 12(3), extendable by two months) without pre-built tooling fails.

**Detect:** review export tooling coverage vs datastore inventory; check the Art. 20 export covers provided data while the Art. 15 response covers activity/logs/derived records per policy; verify self-service export exists and is access-controlled (export = bulk data risk).

**References:** GDPR Art. 20 (portability) and Art. 15 (access), Google Takeout architecture talks, DSAR platform docs
