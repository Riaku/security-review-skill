---
categories: [correctness-pitfalls]
domains: [backend]
---

# Strict Type Comparison

**MUST** validate that a value has the expected type and compare with strict equality at every trust boundary, never relying on implicit coercion.

**Why:** Type juggling makes an auth check pass for a value the author never imagined, such as an array or object satisfying a string comparison.

**Detect:** grep loose comparison in auth and validation paths: `==`/`!=` against request input, `in_array(` without the strict flag, `array_search` without strict.

**References:** OWASP ASVS v5.0 V15.3.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md, CWE-843, CWE-697
