---
categories: [web-api-security]
domains: [backend]
---

# No Silent TLS Upgrade

**MUST** reject cleartext requests on programmatic endpoints rather than redirecting them, so a misconfigured client fails loudly.

**Why:** A redirect turns a broken client into a working one that still believes it is speaking plaintext, hiding the defect until something else relies on it.

**Detect:** grep for 301/308 redirects on `/api`, `/v1`, or RPC routes, and for TLS enforcement implemented only as a redirect rule.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, CWE-319
