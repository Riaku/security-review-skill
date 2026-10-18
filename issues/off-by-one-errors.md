---
categories: [correctness-pitfalls]
domains: [backend]
---

# Off-by-One Errors

**MUST NOT** mix inclusive and exclusive bounds in loops, slices, pagination, and buffer sizes without a stated convention.

**Why:** A single misplaced `<` versus `<=` drops or duplicates records and can read one element past a buffer's end.

**Detect:** `range(len(x)-1)`, `i <= len(`, `arr[n]` where `n == len(arr)`, `LIMIT`/`OFFSET` arithmetic, `pageSize * page` mismatches.

**References:** CWE-193, CWE-119, MISRA-Loop

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
