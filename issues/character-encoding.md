# Character Encoding

**SHOULD** declare and enforce UTF-8 end to end — files, databases, HTTP headers, and mail — rather than relying on defaults.

**Why:** Mismatched encodings mangle data, and permissive fallback decoding enables parser differentials and XSS via alternate charsets.

**Detect:** Missing `charset=utf-8` in `Content-Type`, `latin-1`/`cp1252` defaults, DB collation not `utf8mb4`, `open()` without `encoding=`.

**References:** CWE-172, CWE-836, OWASP XSS Cheat Sheet, RFC 3629

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
