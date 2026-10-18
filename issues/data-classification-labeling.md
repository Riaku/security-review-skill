# Data Classification & Labeling (PII/confidential tagged at rest and in pipelines)

**SHOULD** tag PII and confidential data at creation and carry labels through storage and ETL so downstream controls act on them.

**Why:** Ungoverned data spreads into logs, analytics, and backups unnoticed, turning a minor leak into a regulatory breach.

**Detect:** grep `data_classification`, `pii_tagging`, Macie sensitive-data jobs, dbt `meta: {pii: true}`, catalog label configs.

**References:** NIST SP 800-122 (PII), GDPR Art. 4/32, ISO/IEC 27701, NIST SP 800-53 PT-2/PT-3
