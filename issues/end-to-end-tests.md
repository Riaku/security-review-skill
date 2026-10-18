# End-to-End Tests

**SHOULD** drive the full user journey through a real browser or client, including login, session expiry, and privilege escalation attempts.

**Why:** Security controls that pass in isolation can fail when wired through the real UI, proxies, and session handling.

**Detect:** Playwright/Cypress/Selenium specs under `e2e/`, scenarios asserting redirect on expired token and 403 on admin routes.

**References:** OWASP ASVS V4.1.3, OWASP WSTG v4.2 (session management), NIST SP 800-115

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
