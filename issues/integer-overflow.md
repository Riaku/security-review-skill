# Integer Overflow

**MUST NOT** perform arithmetic on externally influenced integers without width or range checks.

**Why:** Wraparound turns a large quantity or price into a negative or tiny value, enabling balance manipulation and buffer misallocation.

**Detect:** `int32`/`uint` on user-supplied counts, `*`/`+` on request fields with no bounds, `parseInt` into fixed-width types, missing `checked_add`/`Math.addExact`.

**References:** CWE-190, CWE-682, CERT INT32-C

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
