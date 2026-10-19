---
categories: [correctness-pitfalls]
domains: [backend]
---

# Use Standard Parsers

**SHOULD** use the platform's audited libraries for path, URL, and encoding handling instead of hand-rolled string splitting.

**Why:** Hand-rolled parsers rediscover the canonicalization and edge-case bugs the standard library already fixed, and disagree with the components downstream.

**Detect:** grep hand-rolled parsing: `split('/')` on paths, regex-based URL parsing, manual percent-decoding, and `indexOf('?')` query extraction.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
