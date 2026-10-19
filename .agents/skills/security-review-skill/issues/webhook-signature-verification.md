---
categories: [messaging-async, third-party-integrations, web-api-security]
domains: [backend, data]
---

# Webhook Signature & Origin Verification

**MUST** verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook, validate the `Origin` header against an explicit allowlist, and treat payload contents — identity fields included — as untrusted input.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes — from anyone who finds the URL; a handler that trusts payload identity fields blindly is the same exposure, and SaaS signing secrets rotate, so an unverified integration hides the breakage until it fails.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches; no origin check; no idempotency-key dedupe; provider SDK helpers (`constructEvent`) unused; handlers that trust payload identity fields blindly.

**References:** CWE-347, CWE-345, CWE-208, OWASP Webhook Security practices, Stripe/GitHub webhook signing/verification docs
