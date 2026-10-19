---
categories: [distributed-systems]
domains: [data]
---

# Two-Phase Commit

**MUST** ensure the coordinator's commit/abort decision is write-ahead logged so participants can resolve in-doubt transactions after a crash.

**Why:** 2PC blocks participants holding locks when the coordinator dies mid-vote; without durable decisions, resources stay locked or commit inconsistently.

**Detect:** grep for `XA PREPARE` without `XA RECOVER`/recovery manager, coordinator state not persisted, in-doubt transactions resolved by timeout or blind abort instead of from the logged decision, blocking `waitForCommit` loops.

**References:** Gray 2PC paper, CWE-662, PostgreSQL XA recovery docs, NIST SP 800-53 CP-9
