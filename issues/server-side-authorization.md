---
categories: [authorization-access-control, web-api-security]
domains: [backend]
---

# Server-Side Authorization

**MUST** check authorization on every admin or elevated endpoint server-side and **MUST NOT** trust the client for any authorization decision: hidden UI, client route guards, and client-supplied role or permission values are all forgeable, so permissions are re-derived from the authenticated session on every request.

**Why:** Hidden buttons and guarded routes are bypassed by calling the API directly: attackers hit hidden admin endpoints with curl or a proxy, and client-side gating stops no one.

**Detect:** handlers reading role or permission from a request body, header, or unverified token claim; permission flags echoed to the client and trusted back; destructive actions gated only in the frontend router; grep admin routes (`/admin`, `/settings`, `is_admin`, `@require_staff`) for missing auth decorators or middleware and compare UI-hidden actions to unprotected API paths.

**References:** OWASP A01:2021, CWE-862, CWE-269 Improper Privilege Management, OWASP Authorization Cheat Sheet, OWASP ASVS V4.2
