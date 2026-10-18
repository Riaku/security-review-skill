---
categories: [caching, web-client-security]
domains: [frontend, reliability]
---

# Cache-Control Headers

**MUST** set explicit `Cache-Control` on every HTTP response; responses carrying auth tokens, PII, or CSRF values require `no-store`, never a bare default.

**Why:** Missing directives let browsers and proxies cache sensitive pages, exposing them via back-button or shared caches.

**Detect:** Responses lacking `Cache-Control`; `no-store` absent on login, account, admin routes; `public, max-age` on authenticated endpoints.

**References:** OWASP A04:2021, CWE-525, RFC 7234, NIST SP 800-63B 2.4.1.1
