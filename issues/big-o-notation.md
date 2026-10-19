---
categories: [correctness-pitfalls]
domains: [backend]
---

# Big O Notation

**SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** An unnoticed linear or worse scan inside a request turns moderate traffic into timeouts and CPU saturation.

**Detect:** `in` membership on lists in loops, sort-then-scan per request, nested loops over collections, no complexity note on hot functions.

**References:** CWE-407, CWE-834, OWASP ASVS V11.1.3/V11.1.4
