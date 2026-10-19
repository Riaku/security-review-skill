---
categories: [authentication, web-client-security]
domains: [backend, frontend]
---

# Cookie Flags: Secure, HttpOnly, SameSite

**MUST** set `Secure`, `HttpOnly`, and `SameSite=Lax` (or `Strict`) on every session cookie issued by the application.

**Why:** Missing flags let cookies leak over HTTP, be read by injected scripts, or ride cross-site requests, enabling session hijacking and CSRF.

**Detect:** grep `Set-Cookie`, `res.cookie(`, `document.cookie=`; inspect ingress/Envoy/nginx cookie-rewrite annotations for stripped flags.

**References:** RFC 6265, draft-ietf-httpbis-rfc6265bis §4.1.2.7 (SameSite), OWASP Session Management Cheat Sheet, CWE-1004, CWE-1275
