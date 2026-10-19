---
categories: [regulatory-frameworks]
domains: [government-compliance]
---

# AU ISM / IRAP (Australia)

**MUST** control and monitor the hosting environment per IRAP assessment scope against the Australian ISM baseline for the relevant classification level.

**Why:** Australian government workloads on unassessed cloud fail IRAP review; data residency and hosting-provider controls are checked, not assumed.

**Detect:** grep for "IRAP", "ISM", "PROTECTED", "hosting provider" in deployment docs; AU data in non-assessed regions, missing controls mapping.

**References:** Australian Information Security Manual (ISM), Protective Security Policy Framework (PSPF), IRAP (Information Security Registered Assessors Program)
