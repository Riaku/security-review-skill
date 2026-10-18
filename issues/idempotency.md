# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes.

**Detect:** check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key, CWE-1394, AWS REL11-BP08
