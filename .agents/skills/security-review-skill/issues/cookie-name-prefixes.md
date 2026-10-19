---
categories: [web-client-security]
domains: [frontend]
---

# Cookie Name Prefixes

**MUST** use the `__Host-` prefix on session cookies that are not explicitly meant to be shared across hosts.

**Why:** Without `__Host-`, a sibling subdomain can set a cookie of the same name with `Domain=example.com`, and the server cannot tell it from its own.

**Detect:** grep `Set-Cookie` for session and auth cookies whose names lack `__Host-` or that carry a `Domain` attribute.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x12-V3-Web-Frontend-Security.md, RFC 6265bis (cookie prefixes)
