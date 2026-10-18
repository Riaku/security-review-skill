# distributed-systems — full checklist (19 items)

Consistency, consensus, coordination across nodes.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [distributed-systems](../categories/distributed-systems.md) · index: [SKILL.md](../SKILL.md)

# Bloom Filters

**MAY** use Bloom filters as a fast pre-check, but MUST NOT treat a positive match as authoritative since false positives are inherent.

**Why:** Trusting a Bloom hit as truth admits items that were never present, bypassing denylists or corrupting existence-based security decisions.

**Detect:** grep for bloom/`guava BloomFilter`/`BitSet` gating authz or dedup without a backing store confirmation on positive, missing `expectedFpp`/`fpp` sizing config.

**References:** Bloom 1970 paper, CWE-364 Signal Error, RedisBloom false-positive docs

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# CAP Theorem

**SHOULD** document, per datastore, the explicit consistency-versus-availability tradeoff chosen under partition, and test it.

**Why:** Teams assume both guarantees; during a network partition the undeclared behavior surfaces as silent data loss or total outage.

**Detect:** grep config for `consistency=`, `read_preference=`, `quorum` vs `ONE`, `r/w` settings; missing partition-tolerance test in CI or runbook.

**References:** Gilbert and Lynch (CAP theorem), PACELC paper, AWS Well-Architected Reliability Pillar

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Change Data Capture

**MUST** authenticate and encrypt every CDC connector stream (debezium, binlog, WAL slot) with least-privilege read-only database credentials.

**Why:** Unprotected replication feeds expose entire database contents, including PII, to anyone who can reach the connector port.

**Detect:** grep debezium.properties / connector JSON for `snapshot.mode=never` absent, `sslmode=disable`, hardcoded `database.password`, exposed ports 8081/5432 without TLS.

**References:** OWASP A02 Cryptographic Failures, CWE-319, OWASP Data Validation Cheat Sheet

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Clock Skew

**SHOULD NOT** rely on wall-clock timestamps for ordering, leases, or token expiry across nodes without NTP/PTP discipline and bounded-skew checks.

**Why:** Skewed clocks make a token look valid past expiry or a lease appear unexpired, granting access or authority that was revoked.

**Detect:** grep for `time.time()`/`Date.now()` in lease/JWT logic, missing `ntp`/`chrony` in host config, `clock_drift` tolerance unset, no `logical clock`/HLC fallback.

**References:** Google Spanner TrueTime, CWE-1009 (Depends on time), NIST SP 800-186 time sync guidance

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Consistent Hashing

**SHOULD** use virtual nodes (replicas per physical node) so key distribution stays balanced and node churn moves only a fraction of keys.

**Why:** Without virtual nodes, adding or removing a server remaps a disproportionate key share, triggering hotspots and mass cache-miss storms.

**Detect:** grep hash ring code for `vnodes`/`virtual_nodes` count near 1, plain `hash(key) % node_count` (breaks on scale), missing bounded-load or rendezvous hashing.

**References:** Karger consistent hashing paper, Cassandra vnodes docs, NIST SP 800-190 §4.5

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# CQRS

**SHOULD** validate and authorize commands against the write model's current state, never trusting the read model's possibly stale projection for access control.

**Why:** A command approved on lagging read data can violate invariants or grant access the write side has since revoked, opening a TOCTOU window.

**Detect:** grep command handlers reading from read-store/query-side for authz, missing `expected_version`/optimistic concurrency on command, projection lag unbounded.

**References:** Fowler CQRS, Greg Young CQRS docs, CWE-367 Time-of-Check Time-of-Use

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Database per Service

**SHOULD** give each service its own datastore and schema, accessed only through that service's API; **SHOULD NOT** let multiple services share a database instance or read each other's tables directly.

**Why:** Shared connection strings and cross-service table queries create hidden coupling — a schema change breaks unknown consumers — and widen the blast radius: one service's compromise or buggy migration can read or write another service's data, bypassing its authorization layer entirely.

**Detect:** identical DB connection strings across service repos; direct SQL against another service's tables; shared schema grants; cross-service joins in query code or reporting jobs.

**References:** martinfowler.com/articles/microservices.html (Decentralized Data Management), Martin Fowler Patterns of Enterprise Application Architecture (Shared Database anti-pattern)

---

**Part of:** [database](../categories/database.md) · [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Distributed Locks

**MUST** attach a fencing token to every lock grant and have the resource reject operations carrying a stale token, never trusting lock-held-alone.

**Why:** A lock holder paused past its TTL acts after another node acquired the same lock; without fencing, both mutate the resource concurrently.

**Detect:** grep for `redis.lock`/`Redlock` usage without passing a monotonic token to the write path, missing `SET NX PX` expiry, lock release without owner-ID verification.

**References:** Kleppmann "How to do distributed locking", Martin Farber Redlock critique, CWE-662

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Event Sourcing

**MUST** make stored events immutable and append-only, with schema-versioned payloads and cryptographic integrity checks on the event log.

**Why:** Mutable or unsigned events let an attacker rewrite history to forge balances or erase audit trails, destroying the ledger's trustworthiness.

**Detect:** grep for UPDATE/DELETE on events table, missing `event_version`/`schema_version`, no hash/signature chaining (`prev_hash`), events deserialized without version dispatch.

**References:** Fowler Event Sourcing, Greg Young versioning, CWE-393, NIST SP 800-53 AU-9

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Eventual Consistency

**SHOULD NOT** use eventually consistent reads for authorization, balance, or inventory decisions that gate money or access.

**Why:** A stale replica read lets a revoked user act or oversell stock during the replication lag window, an exploitable race.

**Detect:** grep for authz/balance queries hitting read replicas, `read_from=secondary`, replication-lag unchecked before decision logic, missing `session=` sticky reads.

**References:** OWASP A01 Broken Access Control, CWE-367 TOCTOU, NIST SP 800-162

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Leader Election

**MUST** fence stale leaders with a monotonically increasing epoch term before they may serve writes or issue commands.

**Why:** A partitioned old leader that has not noticed its demotion can double-issue work, corrupting state alongside the new leader.

**Detect:** grep election code for missing `epoch`/`term`/`fencing_token` checks, lease TTL longer than failover SLA, workers accepting commands without validating leader epoch.

**References:** Martin Kleppmann "How to do distributed locking", CWE-662, etcd lease documentation

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Outbox Pattern

**MUST** write domain changes and their outbox events in one atomic database transaction, never publishing before commit.

**Why:** Publishing outside the transaction causes phantom events on rollback or lost events on crash, corrupting downstream consumers.

**Detect:** grep for `publish(` or `kafka.send` outside `@Transactional`/`BEGIN...COMMIT`; outbox table missing `status`, `created_at`, or relay poller queries.

**References:** CWE-662 Improper Synchronization, AWS Outbox Pattern, NIST SP 800-53 SI-7

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Quorums

**MUST** configure read and write sets that intersect (R + W > N) for any data where lost updates are unacceptable, and verify overlap under node loss.

**Why:** Non-overlapping quorums let concurrent writes silently overwrite each other, breaking the very consistency the replica count was bought for.

**Detect:** grep for `replication_factor`, `read_consistency=ONE` with `write_consistency=ONE`, R+W<=N arithmetic in client config or driver defaults.

**References:** Dynamo paper quorum model, Cassandra R/W consistency levels, CWE-362 Race Condition

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Race Conditions

**MUST** guard shared-state mutations with proper synchronization (atomic ops, compare-and-set, or scoped locks), never check-then-act on unsynchronized reads.

**Why:** Interleaved read-modify-write across threads or nodes yields lost updates and double-spends that surface only under production concurrency.

**Detect:** grep for `if (exists) then write`, `read(); modify(); write()` without CAS/`UPDATE ... WHERE version=`, non-atomic counters (`i++`), TOCTOU on file checks.

**References:** CWE-362 Race Condition, OWASP Race Condition guidance, NIST SP 800-53 SI-10

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Raft Consensus

**MUST** run Raft clusters with an odd number of voters (3, 5) and mutually authenticated, TLS-encrypted peer transport.

**Why:** An even voter count wastes failure budget — with 4 voters quorum is 3, so a single failure leaves no further tolerance; an odd count maximizes fault tolerance per node. Unauthenticated peers allow a rogue node to hijack the log.

**Detect:** grep raft config for `peers=` count, `raft.enable-tls=false`, missing `--peer-urls=https`, single-node `bootstrap` left in production manifests.

**References:** Raft paper (Ongaro), HashiCorp Raft security guide, CWE-300 Channel Endpoint Verify

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Split Brain

**MUST NOT** allow two nodes to both believe they are primary; enforce quorum-based fencing or STONITH before accepting dual-master state.

**Why:** Two active masters write divergent data that cannot be merged, causing irreversible corruption of databases and shared storage.

**Detect:** grep cluster config for `no-quorum-policy=ignore`, missing `stonith`, `skipped` fencing, heartbeat over untrusted network, `replication_mode=async` with dual-writable VIPs.

**References:** PACEMAKER fencing docs, CWE-662, NIST SP 800-34 Contingency Planning

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Strong Consistency

**MUST** route linearizable reads and writes through the consensus quorum, never bypassing it with direct node access for critical paths.

**Why:** A client reading a non-quorum node sees stale committed state, breaking invariants that strong consistency was purchased to guarantee.

**Detect:** grep for direct `:2379`/`:8500` single-node endpoints, `consistency=eventual` on critical reads, admin ports exposed without auth in ingress.

**References:** etcd consistency docs, Jepsen test reports, NIST SP 800-53 SC-8

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Two-Phase Commit

**MUST** ensure the coordinator's commit/abort decision is write-ahead logged so participants can resolve in-doubt transactions after a crash.

**Why:** 2PC blocks participants holding locks when the coordinator dies mid-vote; without durable decisions, resources stay locked or commit inconsistently.

**Detect:** grep for `XA PREPARE` without `XA RECOVER`/recovery manager, coordinator state not persisted, missing timeout/abort-on-coordinator-loss, blocking `waitForCommit` loops.

**References:** Gray 2PC paper, CWE-662, PostgreSQL XA recovery docs, NIST SP 800-53 CP-9

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Workflow Engines

**MUST** keep durable workflow steps idempotent and side-effect-free at replay time, since Temporal/Step Functions re-execute steps after failure or recovery.

**Why:** Non-idempotent steps (emails, charges, HTTP POSTs) fire again on every replay, duplicating real-world effects across restarts.

**Detect:** grep workflow definitions for external calls outside activity/task wrappers, missing `idempotencyKey`, non-deterministic code (random, clock reads) inside workflow code.

**References:** Temporal determinism docs, AWS Step Functions error handling, CWE-662

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

