---
categories: [web-api-security]
domains: [backend]
---

# Server-Side Authorization

**MUST NOT** Trust the client for any authorization decision: hidden UI, client route guards, and client-supplied role or permission values are all forgeable, so permissions are re-derived server-side from the authenticated session on every request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly.

**Detect:** handlers reading role or permission from a request body, header, or unverified token claim; permission flags echoed to the client and trusted back; destructive actions gated only in the frontend router.

**References:** OWASP A01:2021, CWE-862, OWASP Authorization Cheat Sheet
