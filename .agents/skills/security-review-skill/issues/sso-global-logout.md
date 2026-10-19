---
categories: [authentication]
domains: [backend]
---

# SSO Global Logout

**MUST** terminate the session at every relying party when logout happens at the identity provider.

**Why:** A half-logout leaves the identity provider's session alive, so returning to the portal re-enters every application without authentication.

**Detect:** grep for back-channel or front-channel logout endpoints and for per-app session termination, then test logout-then-reenter.

**References:** OWASP WSTG Session Management Testing, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/06-Session_Management_Testing/
