# Data Classification & Labeling (PII/confidential tagged at rest and in pipelines)

**SHOULD** tag PII and confidential data at creation and carry labels through storage and ETL so downstream controls act on them.

**Why:** Ungoverned data spreads into logs, analytics, and backups unnoticed, turning a small leak into a regulatory breach.

**Detect:** grep `data_classification`, `pii_tagging`, Macie sensitive-data jobs, dbt `pii: true` tags.

**References:** NIST SP 800-122, GDPR Art. 4/32

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
