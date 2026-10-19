---
categories: [web-api-security]
domains: [backend]
---

# Filename Header Encoding

**MUST** generate the download filename server-side and encode it per RFC 6266 rather than echoing the uploaded name.

**Why:** A user-chosen filename reaches a response header, where a newline or quote breaks out of the header or the disposition entirely.

**Detect:** grep for `Content-Disposition` values built from a request filename parameter.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md, RFC 6266 (Content-Disposition), CWE-113
