---
categories: [regulatory-frameworks]
domains: [government-compliance]
---

# CMMC (defense supply chain)

**MUST** achieve the CMMC 2.0 level required by contract (Level 1, 2, or 3) for each enclave processing FCI or CUI, with an assessed scope covering all connected vendor systems.

**Why:** Unassessed subcontractors are the classic supply-chain entry point; one compromised small vendor can expose the entire defense program.

**Detect:** grep vendor contracts/repos for "CMMC", "FCI", "CUI" scope statements; missing level-assessment evidence, unscoped integrations touching CUI flows.

**References:** CMMC 2.0, NIST SP 800-171, DFARS 252.204-7021
