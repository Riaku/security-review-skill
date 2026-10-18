---
categories: [messaging-async, payments-fraud]
domains: [data, governance]
---

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** OWASP WSTG-ATHN-02, CWE-347, PCI DSS 4.0 Req 6.2, Stripe webhook signing guide

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
