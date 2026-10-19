---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# Security Headers

**MUST** Set HSTS, `X-Content-Type-Options: nosniff`, CSP, `Referrer-Policy`, and frame protection on every response.

**Why:** Missing headers leave transport, sniffing, and framing attacks unmitigated.

**Detect:** Config lacking `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`; nginx/ingress snippets absent.

**References:** OWASP A05:2021, CWE-693, securityheaders.com checklist
