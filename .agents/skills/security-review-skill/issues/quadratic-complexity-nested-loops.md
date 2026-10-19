---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Complexity on Hot Paths & Quadratic Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension; **SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone, and an unnoticed linear or worse scan inside a request turns moderate traffic into timeouts and CPU saturation.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides; `in` membership on lists in loops, sort-then-scan per request, no complexity note on hot functions.

**References:** CWE-407, CWE-834, OWASP API DoS guidance, OWASP ASVS V11.1.3/V11.1.4
