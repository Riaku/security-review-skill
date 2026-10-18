# Cyber Supply Chain Risk Management (supplier vetting and ongoing risk review, NIST SP 800-161)

**MUST** vet critical suppliers at onboarding and re-review their security posture on a fixed cadence.

**Why:** One compromised or negligent vendor becomes your breach; SolarWinds showed a single upstream can poison thousands of downstream users.

**Detect:** grep `vendor_risk`, `supplier_assessment`, `C-SCRM` in third-party inventories, due-diligence records, SBOM ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), ISO/IEC 27036
