---
categories: [supply-chain]
domains: [governance]
---

# End-of-Support Components

**MUST NOT** keep components, runtimes, or platforms in production past their vendor support end date without a dated replacement plan.

**Why:** Unsupported software receives no advisories or patches, so vulnerabilities accumulate silently while the component still passes a routine scan.

**Detect:** the dependency and runtime inventory against each vendor's published end-of-support dates

**References:** NIST SP 800-161r1 (C-SCRM, supplier support status)
