---
categories: [web-api-security]
domains: [backend]
---

# Decode Once Before Validation

**MUST** decode and normalize input exactly once, before validation, and never after a check has approved it.

**Why:** Decoding after the check re-injects the characters the check removed, so the sanitized value and the used value differ.

**Detect:** grep for decode or normalize calls after validation (`urldecode`, `decodeURIComponent`, `unquote`, `html.unescape`) on the same value.

**References:** OWASP ASVS v5.0 V1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md, CWE-174
