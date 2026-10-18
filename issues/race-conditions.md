---
categories: [distributed-systems]
domains: [data]
---

# Race Conditions

**MUST** guard shared-state mutations with proper synchronization (atomic ops, compare-and-set, or scoped locks), never check-then-act on unsynchronized reads.

**Why:** Interleaved read-modify-write across threads or nodes yields lost updates and double-spends that surface only under production concurrency.

**Detect:** grep for `if (exists) then write`, `read(); modify(); write()` without CAS/`UPDATE ... WHERE version=`, non-atomic counters (`i++`), TOCTOU on file checks.

**References:** CWE-362 Race Condition, OWASP Race Condition guidance, NIST SP 800-53 SI-10
