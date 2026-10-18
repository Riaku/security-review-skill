---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# Clickjacking

**MUST** Send `X-Frame-Options: DENY` or CSP `frame-ancestors 'none'` on authenticated pages.

**Why:** Invisible iframes overlay trusted buttons onto attacker pages for unintended clicks.

**Detect:** Missing `X-Frame-Options`/`frame-ancestors` in headers or middleware; `ALLOWALL` frame options.

**References:** OWASP A05:2021, CWE-1021, OWASP Clickjacking Defense Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
