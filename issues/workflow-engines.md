---
categories: [distributed-systems, messaging-async]
domains: [data]
---

# Workflow Engines

**MUST** keep durable workflow steps idempotent and side-effect-free at replay time, since Temporal/Step Functions re-execute steps after failure or recovery.

**Why:** Non-idempotent steps (emails, charges, HTTP POSTs) fire again on every replay, duplicating real-world effects across restarts.

**Detect:** grep workflow definitions for external calls outside activity/task wrappers, missing `idempotencyKey`, non-deterministic code (random, clock reads) inside workflow code.

**References:** Temporal determinism docs, AWS Step Functions error handling, CWE-662

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
