---
categories: [messaging-async, web-api-security]
domains: [backend, data]
---

# Webhook Signature Verification

**MUST** Verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches.

**References:** CWE-347, CWE-208, Stripe/GitHub webhook signing docs

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
