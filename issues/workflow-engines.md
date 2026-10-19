---
categories: [distributed-systems, messaging-async]
domains: [data]
---

# Workflow Engines

**MUST** keep durable workflow steps idempotent and side-effect-free at replay time, since engines re-run step code (Temporal workflow code on every replay; Step Functions tasks on every retry) and execute activities at least once.

**Why:** Activities are at-least-once: a worker that dies after the external call but before the completion is recorded will run the step again, and Step Functions re-runs a failed task on retry. Non-idempotent steps (emails, charges, HTTP POSTs) therefore duplicate real-world effects, while Temporal's replay-visible failure mode is non-deterministic *workflow* code (clock reads, random, map order) that diverges from history.

**Detect:** grep workflow definitions for external calls outside activity/task wrappers, missing `idempotencyKey`, non-deterministic code (random, clock reads) inside workflow code.

**References:** Temporal determinism docs, AWS Step Functions error handling, CWE-662
