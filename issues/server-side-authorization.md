---
categories: [web-api-security]
domains: [backend]
---

# Server-Side Authorization

**MUST NOT** Rely on UI hiding or client route guards; enforce permissions in server code per request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly.

**Detect:** Routes without auth middleware or policy decorators; authorization only in frontend routers.

**References:** OWASP A01:2021, CWE-862, OWASP Authorization Cheat Sheet
