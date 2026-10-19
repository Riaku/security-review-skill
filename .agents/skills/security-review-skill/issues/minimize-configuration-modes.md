---
categories: [api-design]
domains: [backend]
---

# Minimize Configuration Modes

**SHOULD** delete configuration modes and options the actual use case does not need, rather than shipping every mode the design can express.

**Why:** Each mode multiplies the testable surface and adds a deployable-insecure state that no test covers.

**Detect:** grep for mode/algorithm/profile switches reading from config or environment, and count the combinations the test suite actually exercises.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf
