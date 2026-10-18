---
categories: [correctness-pitfalls]
domains: [backend]
---

# Dead Code

**SHOULD NOT** ship code paths that are never reached or never exercised by tests.

**Why:** Unreachable branches hide vulnerabilities that no test covers, rot silently, and mislead reviewers into trusting unverified logic.

**Detect:** Functions with zero call sites, `if False`, commented-out blocks, feature flags permanently off, coverage reports showing 0 hits.

**References:** CWE-561, CWE-1152
