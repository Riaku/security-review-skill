---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# XSS

**MUST NOT** Emit user-controlled data into HTML without context-aware escaping or raw/filter bypasses.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
