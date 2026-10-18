---
categories: [messaging-async, payments-fraud, resilience]
domains: [data, governance, reliability]
---

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes; retried requests, network timeouts, and scripted replays trigger refund cascades that erode customer trust.

**Detect:** Check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache; grep payment API routes and migration files for `dedupe`.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key-header, CWE-1394, AWS REL11-BP08

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [resilience](../categories/resilience.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
