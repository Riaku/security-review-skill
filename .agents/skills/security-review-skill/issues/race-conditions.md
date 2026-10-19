---
categories: [correctness-pitfalls, distributed-systems]
domains: [backend, data]
---

# Race Conditions

**MUST** guard shared-state mutations with proper synchronization (atomic ops, compare-and-set, or scoped locks) or immutability, never check-then-act on unsynchronized reads and never assume single-threaded execution.

**Why:** Interleaved read-modify-write across threads or nodes yields lost updates, double-spends, and intermittently corrupted data that surface only under production concurrency, carrying security holes that appear only under real load.

**Detect:** grep for `if (exists) then write`, `read(); modify(); write()` without CAS/`UPDATE ... WHERE version=`, non-atomic counters (`i++`), shared dict/list mutated without `Lock`/`mutex`/`synchronized`, cached mutable singletons, TOCTOU on file checks.

**References:** CWE-362 Race Condition, CWE-366, OWASP Race Condition guidance, NIST SP 800-53 SI-10, OWASP ASVS V11.1.6
