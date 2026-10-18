# payments-fraud — full checklist (5 items)

Payment flows, fraud, and money-movement safety.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes.

**Detect:** check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key, CWE-1394, AWS REL11-BP08

# 3D Secure / SCA

**MUST** trigger 3DS2 challenge flows for high-risk transactions and honor the issuer's authentication result before capturing funds.

**Why:** Skipping SCA shifts liability onto the merchant and exposes EU/UK cards to fraudulent chargebacks under PSD2 rules.

**Detect:** grep for `three_d_secure`, `sca_required`, `exemption`, `ds.transstatus` in payment service code and gateway config.

**References:** PSD2 Article 97, OWASP WSTG-ATHZ-04, CWE-287, Stripe 3DS2 docs

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** OWASP WSTG-ATHN-02, CWE-347, PCI DSS 4.0 Req 6.2, Stripe webhook signing guide

# Double-Charge Prevention

**MAY** rely on client-side button disabling alone; a server-side idempotency key per charge request is the real safeguard.

**Why:** Retried requests, network timeouts, and scripted replays duplicate charges, eroding customer trust and triggering refund cascades.

**Detect:** grep for `Idempotency-Key`, `idempotency_key UNIQUE`, `dedupe` in payment API routes and migration files.

**References:** Stripe idempotency docs, CWE-360, OWASP ASVS 14.3.3, NIST SP 800-53 SI-7

# PCI DSS as Audit Regime (SAQ, CDE scoping)

**MUST** scope the cardholder data environment accurately and complete the correct SAQ level (or full ROC) for the actual card data flow, not the desired one.

**Why:** Under-scoped CDEs are the most common PCI failure: one stray database storing PANs drags the whole network into breach liability.

**Detect:** grep for "PAN", "cardholder", "CDE", "SAQ-" in configs; card data in logs, unsegmented networks, SAQ type mismatched to flow.

**References:** PCI DSS v4.0.1, SAQ A-D, PCI SSC scoping guidance

