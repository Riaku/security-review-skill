# Quadratic Complexity & Nested Loops (O(n²) on unbounded input)

**MUST NOT** nest loops over two externally sized collections without a bound on either dimension.

**Why:** A modest payload (10k × 10k) becomes 100M operations, letting one cheap request saturate CPU for everyone.

**Detect:** `for ... for` over request arrays, `.map` inside `.filter` on user lists, join without index, no max-length on both sides.

**References:** CWE-407, CWE-834, OWASP API DoS guidance

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [scaling-capacity](../categories/scaling-capacity.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
