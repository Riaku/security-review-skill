---
categories: [hardening-benchmarks, regulatory-frameworks]
domains: [governance]
---

# Compliance Rule Single Source

**MUST** author each hardening rule once in machine-readable form and map it to every regime it satisfies, instead of duplicating rules per framework.

**Why:** Per-regime copies drift, so the document an auditor reads and the check that actually runs stop describing the same control.

**Detect:** Grep the benchmark or policy repository for the same control implemented twice under different framework names; each rule should carry one canonical ID plus per-framework mapping tags.

**References:** ComplianceAsCode content, https://complianceascode.github.io/content-pages/guides/index.html, NIST SP 800-53 (control mapping)
