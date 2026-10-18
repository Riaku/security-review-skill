# SSR Hydration XSS

**MUST NOT** interpolate user-controlled data into server-rendered HTML without context-aware escaping, especially inside script, attribute, or URL contexts.

**Why:** Unescaped state serialized into `__NEXT_DATA__` or inline scripts executes on every page load before hydration, bypassing CSP unsafe-inline allowances.

**Detect:** grep `dangerouslySetInnerHTML`, `innerHTML`, `JSON.stringify` inside `<script>`, `window.__INITIAL_STATE__`, unescaped `{{ }}` templates.

**References:** CWE-79, OWASP XSS Prevention Cheat Sheet, OWASP A03:2021

---

**Part of:** [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
