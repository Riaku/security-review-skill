---
categories: [web-api-security]
domains: [backend]
---

# File Upload Validation

**MUST** Check uploads by magic bytes, enforce extension/size limits, store outside the web root with randomized names.

**Why:** Unvalidated uploads accept webshells that execute when fetched from a served directory.

**Detect:** `save(request.files[...])` without type/size checks; uploads under static paths; trusting client `Content-Type`.

**References:** OWASP A03:2021, CWE-434, OWASP File Upload Prevention Cheat Sheet
