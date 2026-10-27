---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# CORS

**MUST NOT** Pair wildcard or reflected `Access-Control-Allow-Origin` with `Allow-Credentials: true`; whitelist trusted origins.

**Why:** Wildcard-plus-credentials lets any site read authenticated responses cross-origin.

**Detect:** `Allow-Origin: *`, `allow_origins=['*']`, `@CrossOrigin` with credentials, origin reflection.

**References:** OWASP API8:2023 Security Misconfiguration, OWASP A05:2021, CWE-942, MDN CORS credentials
