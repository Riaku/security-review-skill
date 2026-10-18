---
categories: [correctness-pitfalls]
domains: [backend]
---

# Floating Point Math

**SHOULD NOT** compare binary floating-point values for exact equality or accumulate them over many operations.

**Why:** Rounding error makes `0.1 + 0.2 == 0.3` false and compounds into wrong totals, broken idempotency, and flaky tests.

**Detect:** `== 0.1`, `assert x == y` on floats, `sum(floats)`, `float(` in money/rate code, missing `math.isclose`/`abs(a-b) < eps`.

**References:** CWE-1339, CWE-682, IEEE 754
