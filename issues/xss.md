---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# XSS

**MUST NOT** emit user-controlled data into HTML without context-aware escaping; raw-output helpers and escaping-filter bypasses (`|safe`, `Markup(`, `dangerouslySetInnerHTML`) MUST NOT receive request-controlled data, and user-controlled data MUST NOT be interpolated into server-rendered HTML (`__NEXT_DATA__`, `window.__INITIAL_STATE__`, inline `<script>` blocks, unescaped `{{ }}` templates) without context-aware escaping for script, attribute, and URL contexts.

**Why:** Injected scripts run in victims' sessions, stealing cookies and acting as them; unescaped state serialized into `__NEXT_DATA__` or inline scripts executes on every page load before hydration, bypassing CSP unsafe-inline allowances.

**Detect:** `innerHTML`, `dangerouslySetInnerHTML`, `|safe`, `Markup(` fed by request data; `JSON.stringify` inside `<script>`, `window.__INITIAL_STATE__`, and unescaped `{{ }}` templates in server-rendered HTML.

**References:** OWASP A03:2021, CWE-79, OWASP XSS Prevention Cheat Sheet
