# Vertical Privilege Escalation / Function-Level Authorization

**MUST** check authorization on every admin or elevated endpoint server-side; never rely on hiding buttons or menus in the UI.

**Why:** Attackers call hidden endpoints directly (IDOR-style), and client-side gating stops no one with curl or a proxy.

**Detect:** grep admin routes (`/admin`, `/settings`, `is_admin`, `@require_staff`) for missing auth decorators/middleware; compare UI-hidden actions to unprotected API paths.

**References:** OWASP A01:2021, CWE-269 Improper Privilege Management, CWE-862 Missing Authorization, OWASP ASVS V4.2
