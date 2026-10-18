---
categories: [authentication, web-api-security]
domains: [backend]
---

# Missing Authentication Middleware / Default-Deny Routing

**MUST** default-deny: every route requires authentication unless explicitly marked public via an allowlist.

**Why:** Route-by-route opt-in means any forgotten or newly added endpoint ships unauthenticated, exposing internal APIs to the internet.

**Detect:** grep router config for missing global auth middleware, routes without `@authenticated`/`requireAuth`, `public: true` as default, admin endpoints outside auth filter chain.

**References:** OWASP A01:2021, CWE-306, NIST SP 800-53 AC-3, CIS Control 4.5

---

**Part of:** [authentication](../categories/authentication.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
