---
categories: [correctness-pitfalls]
domains: [backend]
---

# Dead Code

**SHOULD NOT** ship code paths that cannot be reached (no call site, permanently-off feature flag, disabled branch); a reachable branch that no test exercises is a coverage finding, not dead code.

**Why:** Unreachable branches hide vulnerabilities that no test covers, rot silently, and mislead reviewers into trusting unverified logic.

**Detect:** Functions with zero call sites, `if False`, commented-out blocks, feature flags permanently off.

**References:** CWE-561
