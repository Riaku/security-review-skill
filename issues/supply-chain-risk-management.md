# Cyber Supply Chain Risk Management (supplier vetting and ongoing risk review, NIST SP 800-161)

**MUST** vet each critical supplier and dependency for security posture and re-review it on a fixed cadence, not just at onboarding.

**Why:** A compromised or negligent vendor becomes your breach; SolarWinds showed one upstream can poison thousands of downstream users.

**Detect:** grep `vendor_risk`, `supplier_assessment`, `C-SCRM`, third-party inventory files, `SBOM` ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), ISO/IEC 27036
