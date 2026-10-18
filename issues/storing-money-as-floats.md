---
categories: [correctness-pitfalls]
domains: [backend]
---

# Storing Money as Floats

**MUST** represent currency as integers in minor units or an exact decimal type, never as binary floating point.

**Why:** Float rounding silently mis-charges customers, breaks reconciliation, and fails audit for financial records.

**Detect:** `float`/`double` in amount, price, balance, total columns or fields; `REAL`/`FLOAT` in migrations; `round(x*100)` casts.

**References:** CWE-1240, CWE-682, PCI DSS 6.5
