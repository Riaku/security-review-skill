---
categories: [deployment-release]
domains: [infrastructure]
---

# Staging Environments

**MUST NOT** populate staging with production data copies unless they are masked, encrypted, and access-restricted to the same degree as prod.

**Why:** Staging typically has weaker auth, logging, and network controls, so a raw prod snapshot leaks real PII through a far softer target.

**Detect:** grep ETL/sync jobs for unmasked `SELECT *` from prod tables into staging; check staging ingress for absent auth, disabled audit logging, open security groups.

**References:** OWASP Top 10 A02:2021 Cryptographic Failures, GDPR Art. 32, CWE-201
