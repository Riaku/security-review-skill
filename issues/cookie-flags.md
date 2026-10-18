# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265bis, OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275

---

**Part of:** [authentication](../categories/authentication.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
