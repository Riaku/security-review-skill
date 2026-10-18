---
categories: [web-api-security]
domains: [backend]
---

# Server-Side Template Injection (SSTI)

**MUST NOT** Render user input as a template; pass it only as context variables, never into dynamic template compilation.

**Why:** Expressions like `{{config}}` evaluate server-side, escalating to remote code execution.

**Detect:** `render_template_string(user_input)`, `Template(request...)`, `format_map` with user strings.

**References:** CWE-1336, OWASP A03:2021, PortSwigger SSTI research

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
