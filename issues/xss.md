---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# XSS

**MUST NOT** emit user-controlled data into HTML without context-aware escaping; raw-output helpers and escaping-filter bypasses (`|safe`, `Markup(`, `dangerouslySetInnerHTML`) MUST NOT receive request-controlled data.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
