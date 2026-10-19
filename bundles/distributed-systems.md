# distributed-systems — full checklist (21 items)

Consistency, consensus, coordination across nodes.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/distributed-systems.md](../categories/distributed-systems.md) · Index: [SKILL.md](../SKILL.md)

# ACID & Transactional Outbox

**MUST** rely on ACID guarantees only where the engine actually provides them; workflows spanning multiple stores MUST NOT assume cross-system atomicity, and domain changes along with their outbox events **MUST** be written in one atomic database transaction, never publishing before commit.

**Why:** ACID holds inside one database, not across a database plus a queue plus a third-party API. Treating "we use Postgres" as blanket safety leaves balances and event logs silently diverging whenever the second write fails after the first commits. Publishing outside the transaction causes phantom events on rollback or lost events on crash, corrupting downstream consumers.

**Detect:** A DB commit followed by a Kafka/queue publish with no outbox or saga pattern; no reconciliation job comparing stores; SQLite used for concurrent multi-writer workloads. Grep for `publish(` or `kafka.send` outside `@Transactional`/`BEGIN...COMMIT`; an outbox table missing `status`, `created_at`, or a relay poller is a gap.

**Bad:**
```python
db.commit()
kafka.publish("order-created", order)   # publish fails -> event lost forever
```

**Good:**
```python
with db.transaction():
    db.insert_order(order)
    outbox.enqueue("order-created", order)  # relay process publishes reliably
```

**References:** Kleppmann *DDIA* Ch. 7, Transactional Outbox pattern (Confluent), AWS Outbox Pattern, NIST SP 800-53 SI-7, CWE-662

# Bloom Filters

**MAY** use Bloom filters as a fast pre-check, but MUST NOT treat a positive match as authoritative since false positives are inherent.

**Why:** A Bloom hit means "maybe present": treating it as truth over-blocks denylisted lookups and silently admits never-seen items in allowlist or dedup checks. Only a negative is definitive (`BF.EXISTS` returns 1 for "may exist", 0 for "definitely does not exist"), so positives must be confirmed against the backing store.

**Detect:** grep for bloom/`guava BloomFilter`/`BitSet` gating authz or dedup without a backing store confirmation on positive, missing `expectedInsertions`/`fpp` (Guava) or `ERROR`/`CAPACITY` (RedisBloom) sizing.

**References:** Bloom 1970 paper, RedisBloom false-positive docs

# CAP Theorem

**SHOULD** document, per datastore, the explicit consistency-versus-availability tradeoff chosen under partition, and test it.

**Why:** Teams assume both guarantees; during a network partition the undeclared behavior surfaces as silent data loss or total outage.

**Detect:** grep config for `consistency=`, `read_preference=`, `quorum` vs `ONE`, `r/w` settings; missing partition-tolerance test in CI or runbook.

**References:** Gilbert and Lynch (CAP theorem), PACELC paper, AWS Well-Architected Reliability Pillar

# Change Data Capture

**MUST** authenticate and encrypt every CDC connector stream (debezium, binlog, WAL slot) with least-privilege read-only database credentials.

**Why:** Unprotected replication feeds expose entire database contents, including PII, to anyone who can reach the connector port.

**Detect:** grep debezium.properties / connector JSON for `snapshot.mode=never` absent, `sslmode=disable`, hardcoded `database.password`, exposed ports 8081/5432 without TLS.

**References:** OWASP A02 Cryptographic Failures, CWE-319, OWASP Data Validation Cheat Sheet

# Clock Skew

**SHOULD NOT** rely on wall-clock timestamps for ordering, leases, or token expiry across nodes without NTP/PTP discipline and bounded-skew checks.

**Why:** Skewed clocks make a token look valid past expiry or a lease appear unexpired, granting access or authority that was revoked.

**Detect:** grep for `time.time()`/`Date.now()` in lease/JWT logic, missing `ntp`/`chrony` in host config, `clock_drift` tolerance unset, no `logical clock`/HLC fallback.

**References:** Google Spanner TrueTime, NIST SP 800-53 AU-8 (Time Stamps), RFC 5905 (NTP)

# Consistent Hashing

**SHOULD** use virtual nodes (replicas per physical node) so key distribution stays balanced and node churn moves only a fraction of keys.

**Why:** Without virtual nodes, adding or removing a server remaps a disproportionate key share, triggering hotspots and mass cache-miss storms.

**Detect:** grep hash ring code for `vnodes`/`virtual_nodes` count near 1, plain `hash(key) % node_count` (breaks on scale), missing bounded-load or rendezvous hashing.

**References:** Karger et al. "Consistent Hashing and Random Trees" (1997), Cassandra vnodes docs, Mirrokni/Thorup/Zadimoghaddam "Consistent Hashing with Bounded Loads" (2016)

# CQRS

**SHOULD** validate and authorize commands against the write model's current state, never trusting the read model's possibly stale projection for access control.

**Why:** A command approved on lagging read data can violate invariants or grant access the write side has since revoked, opening a TOCTOU window.

**Detect:** grep command handlers reading from read-store/query-side for authz, missing `expected_version`/optimistic concurrency on command, projection lag unbounded.

**References:** Fowler CQRS, Greg Young CQRS docs, CWE-367 Time-of-Check Time-of-Use

# Database per Service

**SHOULD** give each service its own datastore and schema, accessed only through that service's API; **SHOULD NOT** let multiple services share a database instance or read each other's tables directly.

**Why:** Shared connection strings and cross-service table queries create hidden coupling — a schema change breaks unknown consumers — and widen the blast radius: one service's compromise or buggy migration can read or write another service's data, bypassing its authorization layer entirely.

**Detect:** identical DB connection strings across service repos; direct SQL against another service's tables; shared schema grants; cross-service joins in query code or reporting jobs.

**References:** martinfowler.com/articles/microservices.html (Decentralized Data Management), Martin Fowler Patterns of Enterprise Application Architecture (Shared Database anti-pattern)

# Database Selection by Workload (CAP Class Fit)

**SHOULD** choose each datastore deliberately for its workload's read/write consistency requirement and access pattern — strong consistency for transactions/permissions/inventory, tunable consistency for feeds/logs/caches, graph only for deep relationship traversal — and record the rationale, naming the store's configured behaviour under partition (quorum/R+W>N, read preference) rather than a product-level CP/AP label.

**Why:** A wrong datastore choice surfaces years later as a forced migration ("the worst pain imaginable"): an AP store backing balances, or a CP store blocking feeds during partitions.

**Detect:** review architecture docs/ADRs for datastore-per-workload rationale; grep for one store serving contradictory workloads (e.g. Redis as system-of-record, Postgres for firehose telemetry).

**References:** CAP theorem, DDIA ch. 4–9, AWS/Google datastore selection guides

# Distributed Locks

**MUST** attach a fencing token to every lock grant and have the resource reject operations carrying a stale token, never trusting lock-held-alone.

**Why:** A lock holder paused past its TTL acts after another node acquired the same lock; without fencing, both mutate the resource concurrently.

**Detect:** grep for `redis.lock`/`Redlock` usage without passing a monotonic token to the write path, missing `SET NX PX` expiry, lock release without owner-ID verification.

**References:** Kleppmann "How to do distributed locking" (2016), antirez "Is Redlock safe?" (2016), CWE-662

# Event Sourcing

**MUST** make stored events immutable and append-only, with schema-versioned payloads and cryptographic integrity checks on the event log.

**Why:** Mutable or unsigned events let an attacker rewrite history to forge balances or erase audit trails, destroying the ledger's trustworthiness.

**Detect:** grep for UPDATE/DELETE on events table, missing `event_version`/`schema_version`, no hash/signature chaining (`prev_hash`), events deserialized without version dispatch.

**References:** Fowler Event Sourcing, Greg Young versioning, CWE-393, NIST SP 800-53 AU-9

# Eventual Consistency

**SHOULD NOT** use eventually consistent reads for authorization, balance, or inventory decisions that gate money or access.

**Why:** A stale replica read lets a revoked user act or oversell stock during the replication lag window, an exploitable race.

**Detect:** grep for authz/balance queries hitting read replicas, `read_from=secondary`, replication-lag unchecked before decision logic, missing `session=` sticky reads.

**References:** OWASP A01 Broken Access Control, CWE-367 TOCTOU, NIST SP 800-162

# Leader Election

**MUST** fence stale leaders with a monotonically increasing epoch term before they may serve writes or issue commands.

**Why:** A partitioned old leader that has not noticed its demotion can double-issue work, corrupting state alongside the new leader.

**Detect:** grep election code for missing `epoch`/`term`/`fencing_token` checks, lease TTL longer than failover SLA, workers accepting commands without validating leader epoch.

**References:** Martin Kleppmann "How to do distributed locking", CWE-662, etcd lease documentation

# Quorums

**MUST** configure intersecting read/write quorums (R + W > N) wherever a read must observe the most recent acknowledged write, and use compare-and-set / lightweight transactions (or a single writer per key) wherever concurrent read-modify-write must not lose an update — quorum intersection alone does not prevent lost updates.

**Why:** Non-overlapping quorums return stale reads — a reader can miss the last acknowledged write entirely. But overlap is not atomicity: two concurrent read-modify-write cycles both succeed and the conflict is resolved last-write-wins (usually silently), so keys with lost-update risk need CAS/lightweight transactions or a designated writer.

**Detect:** grep for `replication_factor`, `read_consistency=ONE` with `write_consistency=ONE`, R+W<=N arithmetic in client config or driver defaults.

**References:** Dynamo paper quorum model, Cassandra R/W consistency levels, CWE-362 Race Condition

# Race Conditions

**MUST** guard shared-state mutations with proper synchronization (atomic ops, compare-and-set, or scoped locks) or immutability, never check-then-act on unsynchronized reads and never assume single-threaded execution.

**Why:** Interleaved read-modify-write across threads or nodes yields lost updates, double-spends, and intermittently corrupted data that surface only under production concurrency, carrying security holes that appear only under real load.

**Detect:** grep for `if (exists) then write`, `read(); modify(); write()` without CAS/`UPDATE ... WHERE version=`, non-atomic counters (`i++`), shared dict/list mutated without `Lock`/`mutex`/`synchronized`, cached mutable singletons, TOCTOU on file checks.

**References:** CWE-362 Race Condition, CWE-366, OWASP Race Condition guidance, NIST SP 800-53 SI-10, OWASP ASVS V11.1.6

# Raft Consensus

**MUST** run Raft clusters with an odd number of voters (3, 5) and mutually authenticated, TLS-encrypted peer transport.

**Why:** An even voter count wastes failure budget — with 4 voters quorum is 3, so a single failure leaves no further tolerance; an odd count maximizes fault tolerance per node. Unauthenticated peers allow a rogue node to hijack the log.

**Detect:** grep raft config for voter count, missing `--listen-peer-urls=https://`/`--initial-advertise-peer-urls=https://`, missing `--peer-client-cert-auth`/`--peer-cert-file`, single-node `bootstrap` left in production manifests.

**References:** Raft paper (Ongaro), HashiCorp Raft security guide, CWE-300

# Sharding

**MUST** choose a shard key that distributes write load evenly and keeps transactionally-related rows on the same shard; cross-shard transactions MUST be avoided by design, not discovered in production.

**Why:** A poor shard key creates hot shards that melt while others idle, and splitting related rows forces distributed transactions — where a partial commit leaves balances, inventories, and indexes permanently inconsistent.

**Detect:** Shard key reviewed against access patterns (tenant_id vs user_id vs time); queries that JOIN or transact across shards; resharding plan documented before the first shard ships; per-shard QPS/CPU variance in dashboards.

**Bad:**
```python
shard = hash(user_id) % 8
# transfers lock rows in two users' shards -> 2PC everywhere
```

**Good:**
```python
shard = hash(tenant_id) % 8   # all of a tenant's rows co-located
# cross-tenant work goes through async reconciliation
```

**References:** Vitess sharding guide, Azure sharding/catalog pattern guides, Kleppmann *DDIA* Ch. 6, CWE-662

# Split Brain

**MUST NOT** allow two nodes to both believe they are primary; enforce quorum-based fencing or STONITH before accepting dual-master state.

**Why:** Two active masters write divergent data that cannot be merged, causing irreversible corruption of databases and shared storage.

**Detect:** grep cluster config for `no-quorum-policy=ignore`, missing `stonith`, `skipped` fencing, heartbeat over untrusted network, `replication_mode=async` with dual-writable VIPs.

**References:** PACEMAKER fencing docs, CWE-662, NIST SP 800-34 Contingency Planning

# Strong Consistency

**MUST** route linearizable reads and writes through the consensus quorum, never bypassing it with direct node access for critical paths.

**Why:** A client reading a non-quorum node sees stale committed state, breaking invariants that strong consistency was purchased to guarantee.

**Detect:** grep for direct `:2379`/`:8500` single-node endpoints, `consistency=eventual` on critical reads, admin ports exposed without auth in ingress.

**References:** etcd consistency docs, Jepsen test reports, NIST SP 800-53 SC-8

# Two-Phase Commit

**MUST** ensure the coordinator's commit/abort decision is write-ahead logged so participants can resolve in-doubt transactions after a crash.

**Why:** 2PC blocks participants holding locks when the coordinator dies mid-vote; without durable decisions, resources stay locked or commit inconsistently.

**Detect:** grep for `XA PREPARE` without `XA RECOVER`/recovery manager, coordinator state not persisted, in-doubt transactions resolved by timeout or blind abort instead of from the logged decision, blocking `waitForCommit` loops.

**References:** Gray 2PC paper, CWE-662, PostgreSQL XA recovery docs, NIST SP 800-53 CP-9

# Workflow Engines

**MUST** keep durable workflow steps idempotent and side-effect-free at replay time, since engines re-run step code (Temporal workflow code on every replay; Step Functions tasks on every retry) and execute activities at least once.

**Why:** Activities are at-least-once: a worker that dies after the external call but before the completion is recorded will run the step again, and Step Functions re-runs a failed task on retry. Non-idempotent steps (emails, charges, HTTP POSTs) therefore duplicate real-world effects, while Temporal's replay-visible failure mode is non-deterministic *workflow* code (clock reads, random, map order) that diverges from history.

**Detect:** grep workflow definitions for external calls outside activity/task wrappers, missing `idempotencyKey`, non-deterministic code (random, clock reads) inside workflow code.

**References:** Temporal determinism docs, AWS Step Functions error handling, CWE-662

