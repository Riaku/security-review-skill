---
categories: [correctness-pitfalls]
domains: [backend]
---

# Validation Covers the Invalid Set

**MUST** validate the property the code depends on — exists, in range, correctly terminated, structurally valid — rather than excluding the single bad value that was observed.

**Why:** A sentinel check is a partial fix: a `NULL` test passes a non-NULL pointer to unmapped memory, and `index >= 0` passes an index past the end of the array. The reported payload stops working, review sees a green test, and the next variant reaches the same fault — the exclusion list encodes the reporter's imagination, not the invalid set.

**Detect:** `if (x == null)`, `if (i >= 0)`, `!= -1`, a single `typeof`/`instanceof` guard, denylist regexes of known-bad tokens, a length check with no upper bound, an allowlist that admits a whole domain after one exclusion; validators whose tests replay only the reported payload.

**References:** CWE-20, CWE-1284, CWE-1285
