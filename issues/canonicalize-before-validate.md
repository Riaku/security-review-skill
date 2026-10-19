---
categories: [web-api-security]
domains: [backend]
---

# Canonicalize Before Validate

**MUST** decode and canonicalize input to one normal form before validating or comparing it, and reject input that still changes when re-decoded.

**Why:** A validator that sees a different string from the component that later decodes it approves an attack; nested encodings survive single-pass checks.

**Detect:** grep decode/unescape calls placed after the validation or comparison (`urldecode`, `normalize`, `unquote`) and validators that run on the raw parameter.

**References:** OWASP Input Validation Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html, CWE-180: Validate Before Canonicalize, https://cwe.mitre.org/data/definitions/180.html
