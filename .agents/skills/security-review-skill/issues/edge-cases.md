---
categories: [correctness-pitfalls]
domains: [backend]
---

# Edge Cases

**SHOULD** test empty, single-element, maximum, zero, negative, and null inputs explicitly rather than trusting the happy path.

**Why:** Unhandled boundary values are where crashes, silent data loss, and auth bypasses surface in production.

**Detect:** Missing tests for `[]`, `0`, `-1`, `None`/`null`, `""`; `if len(x)` guards without else branch; untested max page size.

**References:** CWE-754, CWE-1284, OWASP ASVS 5.1
