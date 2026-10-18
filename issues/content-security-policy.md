---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# Content Security Policy

**SHOULD** Deliver CSP with nonce/hash-based `script-src`; avoid `unsafe-inline` and `unsafe-eval`.

**Why:** A weak CSP removes the last defense once an injection flaw exists.

**Detect:** `unsafe-inline`, `unsafe-eval`, `script-src *` in CSP config; no `Content-Security-Policy` header.

**References:** OWASP A05:2021, CWE-1021, Google CSP Evaluator
