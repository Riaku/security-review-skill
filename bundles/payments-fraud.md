# payments-fraud — full checklist (6 items)

Payment flows, fraud, and money-movement safety.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [payments-fraud](../categories/payments-fraud.md) · index: [SKILL.md](../SKILL.md)

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes; retried requests, network timeouts, and scripted replays trigger refund cascades that erode customer trust.

**Detect:** Check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache; grep payment API routes and migration files for `dedupe`.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key, CWE-1394, AWS REL11-BP08, OWASP ASVS 14.3.3

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [resilience](../categories/resilience.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# 3D Secure / SCA

**MUST** trigger 3DS2 challenge flows for high-risk transactions and honor the issuer's authentication result before capturing funds.

**Why:** Skipping SCA shifts liability onto the merchant and exposes EU/UK cards to fraudulent chargebacks under PSD2 rules.

**Detect:** grep for `three_d_secure`, `sca_required`, `exemption`, `ds.transstatus` in payment service code and gateway config.

**References:** PSD2 Article 97, OWASP WSTG-ATHZ-04, CWE-287, Stripe 3DS2 docs

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** OWASP WSTG-ATHN-02, CWE-347, PCI DSS 4.0 Req 6.2, Stripe webhook signing guide

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# PCI DSS as Audit Regime (SAQ, CDE scoping)

**MUST** scope the cardholder data environment accurately and complete the correct SAQ level (or full ROC) for the actual card data flow, not the desired one.

**Why:** Under-scoped CDEs are the most common PCI failure: one stray database storing PANs drags the whole network into breach liability.

**Detect:** grep for "PAN", "cardholder", "CDE", "SAQ-" in configs; card data in logs, unsegmented networks, SAQ type mismatched to flow.

**References:** PCI DSS v4.0.1, SAQ A-D, PCI SSC scoping guidance

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)

# Ledger Invariant Checks

**MUST** enforce ledger invariants continuously: sum of debits equals sum of credits, no negative balances where prohibited, every money movement has a counter-entry.

**Why:** Silent ledger drift (rounding, partial writes, bugs) compounds into real financial loss; systems without invariant checks discover errors at reconciliation time — too late to cheaply fix.

**Detect:** check for invariant assertions in the ledger layer (double-entry enforcement, balance checks in transactions), scheduled integrity queries, and alarm (not just log) on violation.

**References:** Double-entry bookkeeping in software (Martin Fowler), Stripe financial-modeling talks, PCI-DSS 5/financial integrity practice

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [payments-fraud](../categories/payments-fraud.md) · [backend](../domains/backend.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Reconciliation Runbook

**SHOULD** maintain a tested reconciliation process between internal records and external sources (PSP settlement files, bank statements, partner reports) with discrepancy handling.

**Why:** Money systems disagree with their counterparties routinely; without a reconciliation runbook, every mismatch becomes a fire-drill, and real losses hide in the "we'll check later" pile.

**Detect:** look for reconciliation jobs comparing internal ledger vs PSP/bank files with tolerance thresholds; check discrepancy queue with owner and SLA; verify runbook covers partial settlements and currency mismatches.

**References:** Stripe reconciliation guidance, PCI-DSS 9/10 financial monitoring, payments-engineering practice guides

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

