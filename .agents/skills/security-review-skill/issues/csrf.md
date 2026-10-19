---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# CSRF

**MUST** Require a per-session token or origin check on every state-changing request.

**Why:** Without it, an attacker's page forges authenticated requests that change user state.

**Detect:** POST/PUT/DELETE routes lacking `csrf_protect`, `X-CSRF-Token`, `SameSite`; `csrf_exempt=True`.

**References:** OWASP A01:2021, CWE-352, OWASP CSRF Prevention Cheat Sheet
