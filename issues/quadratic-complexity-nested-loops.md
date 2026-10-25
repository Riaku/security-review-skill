---
categories: [correctness-pitfalls, scaling-capacity]
domains: [backend, reliability]
---

# Complexity on Hot Paths & Quadratic Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two collections whose size the code does not bound without a bound on one dimension; **SHOULD** know the complexity of hot paths against realistic input sizes before shipping, not just correctness.

**Why:** A 10k × 10k pairing becomes 100M operations, so one cheap request saturates CPU for everyone — and the same shape over data the application owns (a table that grows with tenants, a file that grows with history, a list parsed from a config) degrades with volume and not with traffic, which means no load test reproduces it and no attacker is needed for it to bite.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides; the same shape over an application-owned table, file, or parsed document whose row count is not bounded; sort-then-scan per request, no complexity note on hot functions. Decide from the product of the two sizes at realistic scale, not from the code looking tidy.

**References:** CWE-407, CWE-834, OWASP API DoS guidance, OWASP ASVS V11.1.3/V11.1.4
