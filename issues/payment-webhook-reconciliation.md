---
categories: [messaging-async, payments-fraud]
domains: [data, governance]
---

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** OWASP API10:2023 Unsafe Consumption of APIs, CWE-347, Stripe webhook signing guide
