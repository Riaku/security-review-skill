---
categories: [third-party-integrations, web-api-security]
domains: [backend]
---

# SaaS Webhook Consumer Trust

**MUST** verify signature, origin, and replay-protection on every inbound webhook from third-party SaaS — and treat payload contents as untrusted input.

**Why:** Unverified webhook endpoints accept forged events ("payment captured", "user verified") from anyone who finds the URL; SaaS signing secrets also rotate, which unverified integrations hide until they break.

**Detect:** grep webhook handlers for signature verification (HMAC compare, provider SDK `constructEvent`), timestamp tolerance checks, idempotency-key dedupe; flag handlers that trust payload identity fields blindly.

**References:** OWASP Webhook Security practices, Stripe/GitHub webhook verification docs, CWE-345 insufficient verification of data authenticity
