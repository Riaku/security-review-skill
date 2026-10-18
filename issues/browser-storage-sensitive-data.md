---
categories: [web-client-security]
domains: [frontend]
---

# Sensitive Data in Browser Storage (localStorage/sessionStorage)

**MUST NOT** store session tokens, refresh tokens, PII, or cryptographic keys in localStorage or sessionStorage.

**Why:** Web storage has no expiry or HttpOnly protection, so any XSS exfiltrates it persistently and it survives browser restarts and shared machines.

**Detect:** grep `localStorage.setItem`, `sessionStorage.setItem` for `token`, `jwt`, `password`, `secret`, `ssn`; review auth libraries' persistence config.

**References:** CWE-922, OWASP A02:2021, OWASP Authentication Cheat Sheet (token storage)

---

**Part of:** [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
