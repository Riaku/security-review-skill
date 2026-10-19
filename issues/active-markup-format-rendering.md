---
categories: [web-client-security]
domains: [backend, frontend]
---

# Active Markup Format Rendering

**MUST** sanitize or disable user-controlled Markdown, CSS, XSL, and BBCode processing, because each is rendered by an expression engine, not as text.

**Why:** Markdown with raw-HTML passthrough, CSS expressions, and XSL scripts each reach an interpreter, so escaping for HTML alone leaves an execution path.

**Detect:** grep renderers for `markdown` with raw HTML enabled, `style=` interpolation, and XSL/`transform` calls on uploaded documents.

**References:** OWASP ASVS v5.0 V1 Encoding and Sanitization, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
