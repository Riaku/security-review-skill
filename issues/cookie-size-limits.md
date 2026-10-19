---
categories: [web-client-security]
domains: [frontend]
---

# Cookie Size Limits

**MUST** keep each cookie's name and value under 4096 bytes combined.

**Why:** Browsers drop an oversized cookie without an error, so a session or CSRF cookie simply stops existing and the control it carried disappears.

**Detect:** grep for cookie assembly that concatenates unbounded values, and count `Set-Cookie` headers per response.

**References:** RFC 6265, https://www.rfc-editor.org/rfc/rfc6265.html, OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md
