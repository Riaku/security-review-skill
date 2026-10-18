---
categories: [correctness-pitfalls]
domains: [backend]
---

# Unicode

**MUST NOT** assume one character equals one byte or one code point when measuring, truncating, or comparing user text.

**Why:** Combining marks, surrogate pairs, and normalization variants break length checks, allow look-alike spoofing, and corrupt truncation.

**Detect:** `len(s)` as display width, `substr`/`slice` on user text, missing NFC/NFKC normalization, homoglyph or confusable comparisons absent.

**References:** CWE-176, CWE-645, Unicode TR36, OWASP ASVS 5.2

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
