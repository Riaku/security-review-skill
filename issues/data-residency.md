# Data Residency

**MUST** store and process data within the geographic boundaries mandated by applicable regulation or customer contract.

**Why:** Storing data in unauthorized jurisdictions violates sovereignty laws and can trigger regulatory enforcement or contract breach.

**Detect:** grep for region/zone config in storage, compute, CDN settings; check `data_residency`, `region_constraint`, `geo_fence` keys absent or misconfigured.

**References:** GDPR Ch. V, Russian 152-FZ, China PIPL Art. 40, ISO 27018

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
