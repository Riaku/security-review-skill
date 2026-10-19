---
categories: [compliance-privacy, supply-chain]
domains: [governance, infrastructure]
---

# Vendor/third-party risk management and subprocessor registers

**MUST** vet critical suppliers at onboarding and re-review their security posture on a fixed cadence.
**SHOULD** maintain a current register of every vendor and its subprocessors with review dates, data access scope, and breach-notification terms.

**Why:** Breaches frequently originate downstream; without a register you cannot assess exposure or notify affected parties when a vendor falls. A single compromised or negligent vendor becomes your breach: SolarWinds showed one upstream can poison thousands of downstream users.

**Detect:** Missing vendor register doc or spreadsheet; SaaS admin lists without subprocessor pages checked; contracts lacking breach-notification SLA clauses; no `vendor_risk`/`supplier_assessment`/`C-SCRM` records in third-party inventories, due-diligence records, or SBOM ingestion configs.

**References:** NIST SP 800-161, NIST SSDF (SP 800-218), SOC 2 CC9.2, GDPR Art. 28, ISO 27036
