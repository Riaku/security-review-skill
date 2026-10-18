# database — full checklist (56 items)

Schema, queries, transactions, replication, backup/recovery.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [database](../categories/database.md) · index: [SKILL.md](../SKILL.md)

# ACID

**MUST** rely on ACID guarantees only where the engine actually provides them; workflows spanning multiple stores MUST NOT assume cross-system atomicity.

**Why:** ACID holds inside one database, not across a database plus a queue plus a third-party API. Treating "we use Postgres" as blanket safety leaves balances and event logs silently diverging whenever the second write fails after the first commits.

**Detect:** A DB commit followed by a Kafka/queue publish with no outbox or saga pattern; no reconciliation job comparing stores; SQLite used for concurrent multi-writer workloads.

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

**References:** Kleppmann *DDIA* Ch. 7, Transactional Outbox pattern (Confluent), CWE-662

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Backup Encryption & Immutable/Offsite Copies

**MUST** encrypt backups at rest and keep copies that are immutable (object-lock/WORM) and offsite, so a compromised production environment cannot destroy or tamper with every copy.

**Why:** Ransomware crews target backup repositories first: if backups are writable with production credentials, "we have backups" is an illusion. Encryption blocks exposure of regulated data; immutability survives both the ransomware and the burning building.

**Detect:** Bucket policies allowing `s3:BypassGovernanceRetention`, missing object lock/versioning, backup keys reachable from the production IAM role. Grep backup configs for absent encryption flags (`--encrypt`, SSE-KMS) and single-region destinations.

**Bad:**
```bash
# same writable bucket, same creds, plaintext
aws s3 cp /backups/db.tar s3://app-backups/db.tar
```

**Good:**
```bash
gpg --symmetric --cipher-algo AES256 db.tar
aws s3 cp db.tar.gpg s3://vault-backups/db/ \
  --server-side-encryption aws:kms
# bucket: object lock COMPLIANCE + cross-region replication
```

**References:** CIS Control 11 (immutable backups), NIST SP 800-53 CP-9, AWS S3 Object Lock docs, CWE-311

---

**Part of:** [database](../categories/database.md) · [sre-incidents](../categories/sre-incidents.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills proving backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups never restored are unverified guesses: truncated dumps, missing WAL segments, procedures that only work on one engineer's laptop — and ransomware crews routinely destroy backup targets too. Discovering a corrupt set during a real incident converts an outage into permanent loss.

**Detect:** Grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks; a backup job with no matching restore-test job is the finding. Ask for the last successful restore date and evidence: checksums, row counts, an app booting against restored data.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4

---

**Part of:** [database](../categories/database.md) · [sre-incidents](../categories/sre-incidents.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Backups

**MUST** back up every stateful datastore on a defined schedule with a documented recovery point objective (RPO) agreed with the data owner.

**Why:** Without scheduled backups, one disk failure, ransomware event, or accidental `DROP TABLE` becomes permanent data loss — and an undocumented cadence means nobody knows how much a restore will actually lose.

**Detect:** Look for absence of `pg_dump`/`mysqldump`/snapshot jobs, missing backup sidecars in Helm charts or StatefulSet manifests, and no `backup` keys in IaC. Confirm retention settings and that backup success is alerted, not just logged.

**Bad:**
```yaml
# StatefulSet with no backup job and no snapshot policy
kind: StatefulSet
metadata:
  name: postgres
```

**Good:**
```bash
# nightly, encrypted, shipped offsite
pg_dump -Fc mydb | age -r "$BACKUP_PUBKEY" \
  | aws s3 cp - s3://backups/mydb/$(date +%F).dump
```

**References:** NIST SP 800-34 Contingency Planning, CIS Controls v8 (data protection), OWASP ASVS V7

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Batching (many writes/calls, one trip)

**SHOULD** coalesce many small writes or downstream calls into batches sized to the workload instead of one network round trip per record.

**Why:** Per-record round trips multiply latency and connection consumption linearly; a burst that a batched writer absorbs in seconds can exhaust the connection pool and queue the whole service behind it — a self-inflicted availability problem.

**Detect:** Look for `for` loops calling `insert()`, `publish()`, or POST per item where a `bulk_insert`/`executemany`/bulk API exists. Check producers for missing batch tuning (Kafka `linger.ms`/`batch.size`, flush intervals in log and metrics shippers).

**Bad:**
```python
for row in rows:
    db.execute("INSERT INTO t VALUES (%s)", row)  # N trips
```

**Good:**
```python
execute_values(insert_stmt, rows, page_size=1000)  # one trip per page
```

**References:** Arjay McCandless System Design Cheat Sheet (batching), psycopg execute_values docs, Kafka batch.size/linger.ms docs

---

**Part of:** [api-design](../categories/api-design.md) · [database](../categories/database.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Cascading Deletes

**SHOULD NOT** use `ON DELETE CASCADE` on chains of tables holding financial, audit, or otherwise irreplaceable data.

**Why:** One careless delete of a parent row — a test account, a "leftover" tenant — silently erases an entire subtree: orders, payments, audit trails. The cascade executes exactly as designed; backups become the only recovery.

**Detect:** Schema grep for `ON DELETE CASCADE`, especially nested several levels deep; delete endpoints with no dry-run; absence of `RESTRICT` where children must survive.

**Bad:**
```sql
CREATE TABLE orders (id INT, user_id INT REFERENCES users(id) ON DELETE CASCADE);
CREATE TABLE payments (order_id INT REFERENCES orders(id) ON DELETE CASCADE);
-- DELETE user -> orders -> payments: audit trail gone
```

**Good:**
```sql
REFERENCES users(id) ON DELETE RESTRICT  -- force explicit, reviewed cleanup
```

**References:** PostgreSQL ON DELETE actions, OWASP ASVS V6.4 (data retention), CWE-459

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Long-running jobs checkpoint so restarts resume, not restart

**MUST** persist progress checkpoints in long-running batch jobs so an interrupted run resumes from the last checkpoint instead of reprocessing from the beginning.

**Why:** A six-hour job that restarts from zero after an hour-five crash can never finish — every attempt dies at the same wall, or completes while re-emitting side effects for the replayed range.

**Detect:** Inspect job code for a persisted cursor (last processed ID, offset, timestamp) written at intervals and read on startup. Grep for jobs that recompute `MIN(id)` at start instead of loading the stored watermark.

**Bad:**
```python
rows = db.rows.all()          # 6h job, from zero every crash
for r in rows: process(r)
```

**Good:**
```python
cur = store.get("job_cursor", 0)
for r in db.rows.gt(cur).limit(1000):
    process(r); store.put("job_cursor", r.id)
```

**References:** Arjay McCandless cheat sheet (checkpointing), Kafka consumer offset docs, AWS fault-tolerant batch guidance

---

**Part of:** [database](../categories/database.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Code rollback without data rollback causes schema mismatch

**MUST NOT** roll application code back past a schema migration unless that migration is backward-compatible with the old code or a tested compensating migration exists.

**Why:** Migrations move the schema forward while old code expects the old shape: a dropped column or NOT NULL addition makes the rolled-back binary error out or silently write wrong data.

**Detect:** Review migrations paired with the deploy plan: flag destructive changes (`DROP COLUMN`, rename, narrowing types) in the same release; check the scheme is expand-contract — additive first, cleanup after old code is gone.

**Bad:**
```sql
-- release 41: rename + drop; rollback to 40 breaks every query
ALTER TABLE orders RENAME COLUMN total TO amount_cents;
ALTER TABLE orders DROP COLUMN total;
```

**Good:**
```sql
-- expand: add nullable, backfill; contract in a later release
ALTER TABLE orders ADD COLUMN amount_cents bigint;
```

**References:** Fowler Evolutionary Database Design (expand/contract), Marten migration docs, DORA rollback practices

---

**Part of:** [database](../categories/database.md) · [deployment-release](../categories/deployment-release.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Connection Pooling

**MUST** route application database access through a sized connection pool instead of opening a fresh connection per request.

**Why:** TCP plus TLS plus auth handshake per query adds tens of milliseconds each and, worse, unbounded connection creation exhausts the server's `max_connections`, locking out migrations, health checks, and every other service sharing the database.

**Detect:** Look for `new Pool()` per request or per lambda invocation (serverless cold-start churn); config keys `pool_size`, `max_connections`, `PGBOUNCER_POOL_SIZE`; absence of pgbouncer/pgpool in front of many short-lived workers; `FATAL: too many connections` in DB logs.

**Bad:**
```python
def handler(event, ctx):
    conn = psycopg2.connect(DSN)   # new connection per invocation
    rows = conn.execute(q)
```

**Good:**
```python
pool = psycopg2.pool.ThreadedConnectionPool(2, 20, DSN)  # module-level
def handler(event, ctx):
    with pool.getconn() as conn: ...
```

**References:** PgBouncer documentation, PostgreSQL Connection Pooling docs, OWASP ASVS V3.1, AWS Lambda connection management guide

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Crash-consistent volume snapshots vs logical dumps distinguished

**SHOULD** document, per datastore, whether each backup is crash-consistent (volume snapshot) or logically consistent (`pg_dump`, `mysqldump`), and use the right one per recovery scenario.

**Why:** A raw volume snapshot of a running database captures whatever was in page cache at capture time; the engine may need crash recovery, and some configurations produce unrestorable sets. Mixing them up means discovering at restore time that the "backup" was never a valid restore point.

**Detect:** The backup matrix should state each method's consistency guarantee; volume-snapshot jobs over hot databases must pair with WAL/binlog archiving.

**Bad:**
```yaml
# snapshotting a hot Postgres PVC, no WAL archiving
backup: ebs-snapshot, volume: postgres-data
```

**Good:**
```yaml
backup: pg_basebackup + wal-archive  # restore-point capable
# volume snapshots reserved for whole-VM DR only
```

**References:** EBS/PersistentVolume snapshot consistency docs, PostgreSQL backup methods docs, NIST SP 800-34

---

**Part of:** [database](../categories/database.md) · [sre-incidents](../categories/sre-incidents.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Overlapping cron executions guarded by single-runner locks

**MUST** guard scheduled jobs with a single-runner lock (advisory lock, flock, or leader election) so a slow run cannot overlap the next scheduled tick.

**Why:** If a nightly job outlives its interval, two copies run at once: duplicate charges, double-sent emails, deadlocked locks, corrupted aggregates. The failure is intermittent — it appears only when data grows past the schedule window.

**Detect:** Inspect crontabs and systemd timers for jobs with no lock acquisition. Grep for `pg_try_advisory_lock`, `flock`, or distributed locks; check Kubernetes CronJobs for `concurrencyPolicy: Forbid`.

**Bad:**
```bash
# if the 02:00 run spills past 03:00, two run at once
0 2 * * * /app/report.sh
```

**Good:**
```bash
0 2 * * * flock -n /run/report.lock /app/report.sh || \
  logger "report skipped: already running"
```

**References:** Kubernetes CronJob concurrencyPolicy docs, PostgreSQL advisory locks, CWE-662 Improper Synchronization

---

**Part of:** [database](../categories/database.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Cursor-Based Pagination

**SHOULD** paginate large or frequently mutated collections with opaque cursors instead of OFFSET, which degrades and skips rows under concurrent inserts.

**Why:** `OFFSET 100000` forces the database to read and discard every preceding row — free at page 1, a denial-of-service vector at page 5000. Offset paging also shifts results mid-browse, so users see duplicates and miss records.

**Detect:** `?offset=`/`?page=` params on high-volume endpoints; large `LIMIT ... OFFSET ...` in SQL; missing stable sort key (created_at + id) backing cursors.

**Bad:**
```sql
SELECT * FROM events ORDER BY created_at LIMIT 50 OFFSET 100000;
```

**Good:**
```sql
SELECT * FROM events
WHERE (created_at, id) > (:cursor_ts, :cursor_id)
ORDER BY created_at, id LIMIT 50;   -- index seek, stable across inserts
```

**References:** PostgreSQL keyset pagination, Stripe API pagination design, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Data Retention & Deletion Pipelines

**MUST** automatically delete personal data when its retention period expires or a deletion request arrives, and prove deletion propagated to replicas, caches, and backups.

**Why:** Hoarding data beyond its purpose violates GDPR/CCPA erasure obligations and enlarges the breach blast radius — you cannot leak what you no longer hold.

**Detect:** Grep for retention jobs (`DELETE ... WHERE created_at < ...`), tombstone/outbox patterns feeding replicas, and whether deletion covers search indexes and backup expiry. A delete endpoint touching only the primary table is a gap.

**Bad:**
```python
@app.delete("/users/{id}")
def delete_user(id):
    db.users.delete(id)   # analytics replica keeps the row
```

**Good:**
```python
db.users.mark_deleted(id)          # tombstone
outbox.publish("user.deleted", id) # replicas, index, cache
```

**References:** GDPR Art. 17 Right to Erasure, CCPA deletion, NIST SP 800-53 MP-6, ISO 27018

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [database](../categories/database.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Database Migrations

**MUST** manage schema changes through versioned, reviewable migration files applied by tooling — never by ad-hoc SQL run against production.

**Why:** Hand-applied DDL drifts from the repo, so the next deploy assumes a schema that isn't there; unreproducible schema state makes rollback guesswork and turns a routine release into an outage with no audit trail.

**Detect:** Check for framework migrations (Alembic, Flyway, Rails `db/migrate`); flag raw `ALTER TABLE` in ops scripts; diff live schema (`pg_dump --schema-only`) against the repo's migration head.

**Bad:**
```bash
# Friday 17:58, pasted into psql on prod:
psql $PROD -c "ALTER TABLE users ADD COLUMN trial_ends TIMESTAMPTZ;"
```

**Good:**
```python
# alembic/versions/0042_add_trial.py
def upgrade():
    op.add_column('users', sa.Column('trial_ends', sa.DateTime(timezone=True)))
```

**References:** Flyway documentation, Alembic migrations guide, Google SRE Book: Migration Best Practices, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Database per Service

**SHOULD** give each service its own datastore and schema, accessed only through that service's API; **SHOULD NOT** let multiple services share a database instance or read each other's tables directly.

**Why:** Shared connection strings and cross-service table queries create hidden coupling — a schema change breaks unknown consumers — and widen the blast radius: one service's compromise or buggy migration can read or write another service's data, bypassing its authorization layer entirely.

**Detect:** identical DB connection strings across service repos; direct SQL against another service's tables; shared schema grants; cross-service joins in query code or reporting jobs.

**References:** martinfowler.com/articles/microservices.html (Decentralized Data Management), Martin Fowler Patterns of Enterprise Application Architecture (Shared Database anti-pattern)

---

**Part of:** [database](../categories/database.md) · [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Database Selection by Workload (CAP Class Fit)

**SHOULD** choose each datastore deliberately for its workload's CAP class and access pattern — CP for transactions/permissions/inventory, AP for feeds/logs/caches, graph only for deep relationship traversal — and record the rationale.

**Why:** A wrong datastore choice surfaces years later as a forced migration ("the worst pain imaginable"): an AP store backing balances, or a CP store blocking feeds during partitions.

**Detect:** review architecture docs/ADRs for datastore-per-workload rationale; grep for one store serving contradictory workloads (e.g. Redis as system-of-record, Postgres for firehose telemetry).

**References:** CAP theorem, DDIA ch. 4–9, AWS/Google datastore selection guides

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Deadlocks

**MUST** acquire locks on multiple resources in a consistent global order across all code paths, and retry deadlock aborts.

**Why:** Two transactions locking rows A and B in opposite orders will eventually deadlock; the database kills one, but without an idempotent retry users lose writes and queues jam. Timing-dependent, so they hide in testing and appear at peak traffic.

**Detect:** `deadlock detected` in DB logs (40P01/1213); transactions touching several tables in differing orders across services; updates inside loops over unordered result sets.

**Bad:**
```python
# service X: locks order then inventory
# service Y: locks inventory then order  -> circular wait
for item in items:
    inventory.decrement(item)
order.update(status='paid')
```

**Good:**
```python
with txn:
    lock_rows(sorted(table_names))   # every path locks in the same order
    ...
# plus: retry once on 40P01 / 1213
```

**References:** PostgreSQL Deadlock Detection docs, MySQL InnoDB deadlock docs, CWE-833

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Denormalization

**SHOULD NOT** denormalize for read speed unless the write path maintaining the copies is explicitly designed, tested, and reconciled.

**Why:** Denormalization trades consistency for latency; without reliable propagation, derived copies drift, and dashboards, search indexes, and caches each tell a slightly different story.

**Detect:** Redundant columns updated from multiple code paths; aggregates like `user.total_spent` written by scattered `UPDATE`s instead of one event handler; no drift-check job in monitoring.

**Bad:**
```python
# three different services each do:
user.total_spent += order.total   # races, double-counts on retry
```

**Good:**
```python
# single writer consumes order events; idempotent upsert
upsert_user_stats(user_id, computed_from(order_events))  # replayable
```

**References:** Kleppmann *DDIA* Ch. 1, materialized view maintenance patterns, DynamoDB denormalization guide, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Down Migrations

**MUST** provide a tested `downgrade` (rollback) path for every schema migration that touches production data.

**Why:** Releases get rolled back mid-incident; a migration without a working reverse leaves the schema ahead of the old code, converting a five-minute revert into hours of manual surgery under pressure — and untested reversals frequently destroy data when finally attempted.

**Detect:** Alembic revisions with `pass` in `downgrade()`; Flyway migrations lacking `V__`/`U__` pairs; irreversible operations (`DROP TABLE`, `DROP COLUMN`, type narrowing) shipped without a backup-and-expand step; CI that never runs `upgrade -> downgrade -> upgrade`.

**Bad:**
```python
def downgrade():
    pass   # "we won't need this" — until the 2 a.m. rollback
```

**Good:**
```python
def downgrade():
    op.drop_column('users', 'trial_ends')   # exercised in CI against a prod clone
```

**References:** Alembic Rolling Back Migrations, Flyway Undo Migrations, Google SRE Book: Rollback, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Dual-write plus backfill migration cutover rehearsed

**SHOULD** rehearse the full dual-write → backfill → verify → cutover sequence on a staging copy of production data before running it live, with tested rollback at each phase.

**Why:** These migrations have four independent failure modes — dual-write drift, backfill gaps, verifier blind spots, cutover races — and each discovered in production means reconciling divergent datasets by hand under an outage clock.

**Detect:** Require a runbook with phase gates and a rehearsal log. The verifier must compare full datasets with counts plus checksums, not spot checks; cutover and rollback need dry-run evidence.

**Bad:**
```text
runbook: "write to both DBs, backfill, switch reads"
rehearsal: none — the first live run is the test
```

**Good:**
```text
staging: dual-write 48h → backfill → checksum diff = 0
→ cutover drill → rollback drill, each timed and logged
```

**References:** AWS DMS dual-run/verification guidance, expand-migrate-contract migration pattern docs, NIST SP 800-34 rehearsal requirements

---

**Part of:** [database](../categories/database.md) · [deployment-release](../categories/deployment-release.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Durability Acknowledgment Policy

**MUST** acknowledge writes only after they are durably persisted (sync disk and/or quorum replication) for data where loss is unacceptable — payments, orders, credential changes; latency-first acks are permitted only for reversible data (likes, views, logs).

**Why:** Ack-before-persist means a crash between ack and write silently destroys confirmed data; the client believes the operation succeeded and never retries. Acking before durable persistence is tolerable only when the gap is explicitly backed by a durable queue or WAL (Kafka `acks=all`, Redis AOF `everysec`), never a bare in-memory buffer.

**Detect:** Review write paths for ack-before-flush/async-persist on critical entities; check DB durability settings (`synchronous_commit`, replication ack level, fsync) against the data's loss tolerance; trace the ack point relative to persistence — handler returning 2xx before the enqueue is fsynced, flusher threads with no crash-recovery path or backlog alerting.

**References:** DDIA durability/replication chapters, Postgres synchronous_commit docs, latency-vs-durability trade-off, Kafka semantics docs (acks, idempotent producer), Redis AOF persistence docs

---

**Part of:** [correctness-pitfalls](../categories/correctness-pitfalls.md) · [database](../categories/database.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Erasure Propagation to Secondary Stores

**MUST** propagate deletion/erasure requests to every secondary copy: search indexes, caches, analytics, replicas, export buckets — and verify completion.

**Why:** Deleting the user row is the easy 20%; GDPR erasure fails on the other 80% — the Elastic index, the marketing export, the warehouse snapshot that still shows their email.

**Detect:** map erasure workflow against datastore inventory; check each secondary store has a delete-by-user step with verification; flag stores reachable only by "rebuild the whole index" with no SLA.

**References:** GDPR Art. 17 + Art. 19 notification, Google erasure guidance, DSAR automation practice

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [database](../categories/database.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# EXPLAIN ANALYZE

**SHOULD** review `EXPLAIN ANALYZE` plans for every new hot query before merging, rather than trusting that an index exists in theory.

**Why:** Planners skip or misprice indexes when statistics are stale, types mismatch, or predicates are non-sargable; a query that looked fine in development can scan millions of rows in production.

**Detect:** Look for queries wrapping columns in functions (`LOWER(email) = ?`, `date(col) = ?`) which defeat indexes; check for implicit casts between int and varchar join keys; require plan output in PR descriptions for new list endpoints.

**Bad:**
```sql
SELECT * FROM users WHERE lower(email) = lower($1);  -- index on email unused
```

**Good:**
```sql
CREATE INDEX users_email_lower ON users (lower(email));
SELECT * FROM users WHERE lower(email) = lower($1);  -- index-only lookup
```

**References:** PostgreSQL EXPLAIN documentation, Use The Index Luke, OWASP ASVS V3.1, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Exposed Data-Service Ports

**MUST NOT** expose database, cache, search, and daemon ports (Redis 6379, Elasticsearch 9200, MongoDB 27017, Memcached 11211, Docker API 2375, Postgres 5432) beyond the trusted network without authentication and TLS.

**Why:** Internet-scanned services (Shodan/Censys) find unauthenticated Redis/Elasticsearch weekly — no creds needed to read or wipe the dataset.

**Detect:** scan own external IP range for 6379/9200/27017/11211/2375; grep security groups/firewall rules and Service type=LoadBalancer for data ports; check `bind`/`requirepass`/`xpack.security` settings.

**References:** MITRE ATT&CK T1190, CIS Docker 2.x, Shodan exposed-database reports

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [database](../categories/database.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Foreign Keys

**MUST** declare foreign key constraints on relational columns rather than relying on application-level "we always check first" logic.

**Why:** Orphaned rows accumulate the moment a delete races an insert, a migration misses a table, or a new service writes directly to the DB. Orphans corrupt joins and make restores a forensic exercise.

**Detect:** `*_id` columns lacking `REFERENCES`; ORM models with bare integers instead of relationship definitions; manual existence checks before insert (TOCTOU window); FK enforcement disabled for migration speed and never re-enabled.

**Bad:**
```sql
CREATE TABLE orders (id INT, customer_id INT);  -- no constraint: orphans welcome
```

**Good:**
```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT NOT NULL REFERENCES customers(id)
);
```

**References:** SQL:2016 referential integrity, PostgreSQL FOREIGN KEY constraints, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Full Table Scans

**SHOULD NOT** ship list endpoints whose queries degrade to sequential scans once the table exceeds working-set size.

**Why:** A scan that reads every row to return ten is invisible at demo scale but pins disk and CPU at peak; a single crawler or retry storm hitting an unindexed filter can take the database down for everyone.

**Detect:** In `EXPLAIN` output look for `Seq Scan on <big_table>` with high `rows removed by filter`; monitor `pg_stat_user_tables.seq_scan` growth; flag `SELECT *` without LIMIT and unindexed sort columns (`ORDER BY created_at` with no index).

**Bad:**
```sql
SELECT * FROM events WHERE status = 'open' ORDER BY created_at DESC;
-- no index: scans all 40M rows every request
```

**Good:**
```sql
CREATE INDEX idx_events_status_created ON events (status, created_at DESC);
SELECT * FROM events WHERE status = 'open' ORDER BY created_at DESC LIMIT 50;
```

**References:** PostgreSQL EXPLAIN docs, Use The Index Luke: Sequential Scans, OWASP ASVS V3.1, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Full-Text Search

**MUST NOT** implement user-facing search with `LIKE '%term%'` on large tables; use the database's full-text engine or a dedicated search service.

**Why:** Leading-wildcard LIKE cannot use a B-tree index, so every keystroke triggers a full scan — a cheap amplification attack for anyone with a search box. It also mishandles stemming, ranking, and language.

**Detect:** `LIKE '%' || ? || '%'` patterns in query code; search endpoints without rate limiting; missing tsvector/GIN index (Postgres) or external index (Meilisearch, Elasticsearch).

**Bad:**
```sql
SELECT * FROM articles WHERE body LIKE '%' || :q || '%';  -- full scan per keystroke
```

**Good:**
```sql
CREATE INDEX articles_fts ON articles USING gin(to_tsvector('english', body));
SELECT * FROM articles WHERE to_tsvector('english', body) @@ plainto_tsquery(:q);
```

**References:** PostgreSQL Full Text Search + GIN indexes, OWASP ASVS V3.1, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Hot Partitions

**MUST** distribute write load across partitions or shards so no single partition absorbs a disproportionate share of traffic.

**Why:** A partition keyed on a monotonic value like today's date concentrates all current writes on one node, throttling throughput and amplifying the blast radius of a single-node failure while the rest of the cluster idles.

**Detect:** Look for shard keys built from `CURRENT_DATE`, timestamps, or auto-increment IDs used directly as the partition key; check DDL for `PARTITION BY RANGE (created_at)` with no salting and per-partition write metrics for skew.

**Bad:**
```sql
CREATE TABLE events (
    id bigserial,
    created_at timestamptz,
    payload jsonb
) PARTITION BY RANGE (created_at);
-- every insert today hits one partition
```

**Good:**
```sql
CREATE TABLE events (
    shard smallint,
    created_at timestamptz,
    payload jsonb
) PARTITION BY HASH (shard), RANGE (created_at);
-- shard = hash(user_id) % N spreads writes
```

**References:** AWS Well-Architected hot-partition guidance, Azure Storage partition keys, Cassandra monotonic-key anti-patterns

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Idle-in-transaction sessions monitored and killed

**MUST** bound idle open transactions with a timeout, so that a session holding a transaction without activity is terminated automatically rather than pinning resources indefinitely (PostgreSQL's `idle_in_transaction_session_timeout`, unsafe default `0`, is the common case).

**Why:** A stalled transaction — a crashed app, a forgotten `BEGIN`, a debugger breakpoint — pins old row versions, blocks vacuum, and holds row locks against live traffic for hours. One leaked session can degrade the entire database.

**Detect:** Check `postgresql.conf` and per-role `ALTER ROLE ... SET` for the unsafe default `idle_in_transaction_session_timeout = 0` or its absence. Verify runbooks query `pg_stat_activity` for long-lived `idle in transaction` states and alert on session age.

**Bad:**
```ini
# postgresql.conf — default, never touched
idle_in_transaction_session_timeout = 0
```

**Good:**
```ini
idle_in_transaction_session_timeout = 60s
ALTER ROLE app_report SET idle_in_transaction_session_timeout = '300s'
```

**References:** PostgreSQL idle_in_transaction_session_timeout docs, CWE-404 Improper Resource Shutdown, pg_stat_activity guides

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Indexes

**MUST** add supporting indexes for every column used in WHERE, JOIN, and ORDER BY clauses on tables expected to grow beyond a few thousand rows.

**Why:** Missing indexes turn routine lookups into sequential reads; under load this saturates the buffer pool and can cascade into denial of service from what looks like ordinary traffic.

**Detect:** Grep query code for filter columns, then compare against migration files for `CREATE INDEX` / `add_index`. Check slow-query logs and `pg_stat_user_tables.seq_scan` counts.

**Bad:**
```sql
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, created_at TIMESTAMPTZ);
-- hot path: SELECT * FROM orders WHERE customer_id = ?  (no index -> full scan)
```

**Good:**
```sql
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, created_at TIMESTAMPTZ);
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

**References:** OWASP ASVS V3, Use The Index Luke, MySQL indexing best practices, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Isolation Levels

**SHOULD** set the transaction isolation level deliberately per workload instead of inheriting the driver or framework default blindly.

**Why:** Defaults differ wildly — Postgres ships READ COMMITTED, MySQL InnoDB defaults to REPEATABLE READ. The wrong level admits phantom reads or write skew into money paths, and bugs surface only under concurrency, months after launch.

**Detect:** Grep for `isolation_level` config and `SET TRANSACTION ISOLATION LEVEL`; flag read-modify-write logic running under READ COMMITTED where SERIALIZABLE or row locks are needed.

**Bad:**
```sql
-- READ COMMITTED: two sessions both read balance=100, both "reserve" it
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

**Good:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- or explicit: SELECT ... FOR UPDATE on the row being modified
```

**References:** ANSI SQL-92 isolation levels, PostgreSQL Isolation docs, JEP-001 (Heroku), CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Materialized Views

**MAY** serve data from materialized views, but the freshness contract MUST be explicit: every consumer must know the maximum staleness and refresh schedule.

**Why:** A materialized view is a snapshot; serving it where live data is assumed can leak stale authorization decisions — a revoked user still appearing entitled — or stale financial aggregates. A plain `REFRESH` also blocks all reads unless run `CONCURRENTLY`.

**Detect:** Find `CREATE MATERIALIZED VIEW` statements and trace whether a refresh job exists and exposes its lag. Grep for auth or permission logic sourced from a matview with no staleness check.

**Bad:**
```sql
CREATE MATERIALIZED VIEW user_perms AS
  SELECT user_id, can_admin FROM ...;
-- never refreshed; auth reads a months-old snapshot
```

**Good:**
```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY user_perms;
-- scheduled every 5 min; endpoint exposes last_refreshed_at
```

**References:** PostgreSQL MATERIALIZED VIEW / REFRESH CONCURRENTLY docs, OWASP A05 Security Misconfiguration

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# N+1 Queries

**MUST NOT** issue one query per row inside an application loop when a single batched query can fetch the same data.

**Why:** An endpoint that loads 200 parent records and lazily touches a relation per row fires 201 round trips; a modest page view becomes a database meltdown, and attackers deliberately hit such endpoints to exhaust connections.

**Detect:** ORM lazy-access patterns: `for x in items: x.author.name` in Django without `select_related`/`prefetch_related`; `.include()` missing in Parse/GraphQL resolvers; count queries per request in logs (one SELECT repeated N times with varying IDs).

**Bad:**
```python
books = Book.objects.all()
for b in books:
    print(b.author.name)   # one SELECT per book
```

**Good:**
```python
books = Book.objects.select_related('author').all()
for b in books:
    print(b.author.name)   # single JOIN
```

**References:** OWASP ASVS V3.1, Django ORM performance docs, nplusone (N+1 detection library), CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Normalization

**SHOULD** normalize transactional schemas to at least 3NF so each fact is stored once and updates cannot leave copies inconsistent.

**Why:** Duplicated attributes — a customer address copied into every order row — mean one correction requires updating N rows; miss any and reports, invoices, and shipping disagree about the same customer.

**Detect:** Repeated non-key columns across tables (same `customer_name` in orders, invoices, tickets); application code copying fields between tables on write; ad-hoc "sync" jobs patching copies.

**Bad:**
```sql
CREATE TABLE orders (id INT, customer_name TEXT, customer_addr TEXT, total NUMERIC);
-- address change = UPDATE across every order, forever
```

**Good:**
```sql
CREATE TABLE customers (id INT PRIMARY KEY, name TEXT, addr TEXT);
CREATE TABLE orders (id INT, customer_id INT REFERENCES customers(id), total NUMERIC);
```

**References:** Codd normal forms (1NF–3NF), Date *An Introduction to Database Systems*, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# NoSQL Query Injection

**MUST NOT** build queries by merging raw user input into query objects; validate types and use explicit field-level operators instead of user-controlled dicts or `$where` clauses.

**Why:** MongoDB-style engines interpret operator keys inside user JSON: `{"pass": {"$ne": ""}}` submitted into a naive `find(body)` authenticates without a password. `$where` with string concatenation goes further, executing arbitrary JavaScript server-side.

**Detect:** Grep for `find(req.body)`, `$where`, `mapReduce` with interpolation, and PyMongo/Mongoose filters whose dict originates from request payloads. Check for missing schema validation (Mongoose strict mode, JSON Schema) on inbound documents.

**Bad:**
```javascript
db.users.find({
  user: req.body.user,
  pass: req.body.pass   // {"$ne":""} bypasses auth
});
```

**Good:**
```javascript
const u = String(req.body.user), p = String(req.body.pass);
db.users.findOne({ user: u, pass: await verify(p) });
```

**References:** CWE-943 NoSQL injection, OWASP NoSQL Injection Prevention Cheat Sheet, MongoDB $where security notes

---

**Part of:** [database](../categories/database.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Online schema-change tooling for large tables (gh-ost, pt-osc)

**MUST** use a live-migration tool (gh-ost, `pt-online-schema-change`, or a non-blocking Postgres equivalent) for schema changes on tables above a defined size instead of a plain blocking `ALTER TABLE`.

**Why:** A naive `ALTER` on a multi-hundred-gigabyte table can hold an exclusive lock for hours, freezing writes and cascading timeouts through dependent services — and retrying it mid-outage doubles the damage.

**Detect:** Scan migration directories for raw `ALTER TABLE` against known-large tables, missing size thresholds in the runbook, and absence of gh-ost/pt-osc in CI/CD. Migrations should declare expected duration and lock behavior.

**Bad:**
```sql
-- 400 GB table, exclusive lock for hours
ALTER TABLE orders ADD COLUMN promo_code varchar(32);
```

**Good:**
```bash
gh-ost --table=orders --alter="ADD COLUMN promo_code varchar(32)" \
  --execute   # ghost-table copy, seconds-long cutover
```

**References:** GitHub gh-ost docs, Percona pt-online-schema-change docs, PostgreSQL CREATE INDEX CONCURRENTLY docs

---

**Part of:** [database](../categories/database.md) · [deployment-release](../categories/deployment-release.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Optimistic Locking

**SHOULD** use optimistic concurrency control (version or ETag column) for user-facing edits where concurrent modification is possible but rare.

**Why:** Without a version check, two admins editing the same record produce a silent lost update — last write wins and the first change vanishes with no error. A version column turns that collision into a detectable conflict.

**Detect:** UPDATEs over user-editable rows with no `WHERE version = :expected` guard; ORMs not configured for `optimistic_locking`; APIs accepting full-object PUTs with no ETag/If-Match header.

**Bad:**
```sql
UPDATE docs SET body = :new_body WHERE id = :id;  -- clobbers concurrent edit
```

**Good:**
```sql
UPDATE docs SET body = :new_body, version = version + 1
WHERE id = :id AND version = :expected;
-- 0 rows affected => conflict, tell the user
```

**References:** Hibernate `@Version` docs, Rails `lock_version`, RFC 7232 If-Match, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# ORM Lazy Loading

**SHOULD NOT** rely on lazy-loaded relationships inside request handlers or loops; fetch required associations eagerly or via explicit joins.

**Why:** Lazy loading turns one query into N+1: every iteration fires a fresh round trip, multiplying latency and connection pressure. An attacker who controls collection size can make a single request saturate the database — a cheap denial-of-service amplifier.

**Detect:** Grep for SQLAlchemy without `joinedload`/`selectinload`, Hibernate `FetchType.LAZY` traversed in controllers, Django template loops missing `select_related`/`prefetch_related`. Check query logs for repeated identical SELECTs under one request ID.

**Bad:**
```python
for order in session.query(Order).all():
    print(order.customer.email)  # one SELECT per order
```

**Good:**
```python
orders = session.query(Order).options(
    joinedload(Order.customer)).all()
for order in orders:
    print(order.customer.email)  # single joined query
```

**References:** OWASP ORM cautions in SQLi prevention cheat sheet, CWE-400, Hibernate N+1 docs, SQLAlchemy eager loading docs

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Page checksums enabled to catch silent data corruption

**MUST** enable data page checksums, where the engine offers them, at cluster creation so that bit-rot and storage-layer corruption raise hard errors at read time instead of being served silently; PostgreSQL's `--data-checksums` at `initdb` is the common case and cannot be turned on later.

**Why:** Disks and network storage flip bits without complaint. A corrupted index page can return wrong results or stream corruption to replicas. Checksums make the database loud at the first bad read — loud beats wrong.

**Detect:** Run `pg_controldata | grep -i checksum` or check IaC templates for `data_checksums`. Absence on a new cluster is a launch blocker: the setting is fixed at creation.

**Bad:**
```bash
initdb -D /var/lib/postgresql/data   # checksums off
```

**Good:**
```bash
initdb -D /var/lib/postgresql/data --data-checksums
# verify: 'Data page checksum version: 1'
```

**References:** PostgreSQL initdb --data-checksums docs, CWE-17 Unexpected Condition Handling, storage bit-rot literature

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Partitioning

**SHOULD** partition very large tables by a natural access dimension (time, tenant) and verify that queries prune partitions instead of scanning all of them.

**Why:** Without partitioning, retention means `DELETE FROM logs` locking millions of rows while indexes balloon past cache capacity. But a partitioned table whose queries omit the partition key performs worse than an unpartitioned one.

**Detect:** Huge tables with no `PARTITION BY`; queries missing the partition-key predicate (check `EXPLAIN` partitions selected vs total); retention via bulk DELETE instead of `DROP PARTITION`.

**Bad:**
```sql
DELETE FROM access_logs WHERE ts < now() - interval '90 days';  -- locks, bloats WAL
```

**Good:**
```sql
CREATE TABLE access_logs (...) PARTITION BY RANGE (ts);
ALTER TABLE access_logs DETACH PARTITION access_logs_2026_07;
DROP TABLE access_logs_2026_07;   -- instant retention, no lock storm
```

**References:** PostgreSQL partition management docs, MySQL partitioning docs, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Pessimistic Locking

**MAY** hold explicit row locks (`SELECT ... FOR UPDATE`) for hot contended resources, but only inside short transactions with a lock timeout configured.

**Why:** Pessimistic locks prevent lost updates on counters or seat inventory, yet a lock held across an external API call blocks every other writer — one slow dependency becomes a fleet-wide stall.

**Detect:** Audit what runs between `FOR UPDATE` acquisition and commit; missing `lock_timeout` / `NOWAIT`; locks spanning HTTP calls or user-input waits.

**Bad:**
```sql
SELECT * FROM seats WHERE id = 42 FOR UPDATE;
-- then the app calls the payment gateway... lock held for seconds
```

**Good:**
```sql
SET lock_timeout = '2s';
SELECT * FROM seats WHERE id = 42 FOR UPDATE NOWAIT;
-- payment happens after commit; reservation released fast
```

**References:** PostgreSQL SELECT FOR UPDATE docs, MySQL locking reads (InnoDB), CWE-662

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Point-in-Time Recovery

**SHOULD** configure continuous archiving (WAL archiving, binlog retention) so the database recovers to an arbitrary instant, not just the last nightly dump.

**Why:** A nightly backup only protects you to yesterday. An attacker's `DELETE` or a bad migration at 14:00 destroys half a day of transactions unless the write-ahead log is archived continuously and chains into base backups.

**Detect:** Check `archive_mode`/`archive_command` (Postgres) or `log_bin` plus retention (MySQL); confirm base backups record their start LSN/GTID. Verify the archived-log retention window matches the declared RPO.

**Bad:**
```ini
# postgresql.conf
archive_mode = off   # nightly dump only: up to 24h of loss
```

**Good:**
```ini
archive_mode = on
archive_command = 'wal-g wal-push %p'
# base backups every 6h; WAL pushed continuously
```

**References:** PostgreSQL Continuous Archiving & PITR docs, MySQL binlog PITR docs, NIST SP 800-34 RPO guidance

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Automatic database maintenance enabled and tuned

**SHOULD** keep the engine's automatic space-reclamation and maintenance enabled and tuned per table rather than disabling it in favour of hand-rolled cron jobs; PostgreSQL `autovacuum` and its scale factors are the common case.

**Why:** Superseded row versions accumulate; without regular maintenance tables bloat, plans degrade, and in PostgreSQL the transaction ID counter can approach wraparound, forcing emergency single-user mode to avoid corruption.

**Detect:** Grep configs for `autovacuum = off`, oversized `autovacuum_vacuum_scale_factor`, or `VACUUM FULL` in cron. Check `pg_stat_user_tables` for high `n_dead_tup` and missing per-table `reloptions` on high-churn tables.

**Bad:**
```ini
# postgresql.conf — "tuned for performance"
autovacuum = off
```

**Good:**
```sql
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 2ms
);
```

**References:** PostgreSQL Routine Vacuuming docs, CWE-400 Uncontrolled Resource Consumption, PG transaction-ID wraparound docs

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Read Replicas

**MUST** route write-critical reads to the primary and reserve replicas for traffic that tolerates staleness; never send a read-your-own-write query to a replica.

**Why:** Replicas lag by definition. A user who saves a profile and is routed to a replica sees the old data, concludes the save failed, and retries — duplicating records. Auth checks on replicas can honor revoked state for the lag window.

**Detect:** Read/write splitting config audited per query; INSERT-then-SELECT hitting a replica; permission lookups on replicas with no "primary after write" rule.

**Bad:**
```python
db.primary.create_order(o)
return db.replica.get_order(o.id)   # replica may not have it yet
```

**Good:**
```python
db.primary.create_order(o)
return db.primary.get_order(o.id)   # read-your-writes on primary
# analytics and reports go to replicas
```

**References:** PostgreSQL Hot Standby docs, AWS RDS replica lag guidance, Kleppmann *DDIA* Ch. 5, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Anonymization vs pseudonymization and re-identification risk in shared datasets

**MUST NOT** describe a dataset as anonymous unless re-identification is infeasible with auxiliary data; pseudonymized data — reversible keys, stable IDs — remains personal data under GDPR.

**Why:** Substituting user IDs is not anonymization. Linking "anonymized" exports against public sources (voter rolls, breach dumps, location traces) routinely re-identifies people, as the Netflix Prize showed.

**Detect:** Review shared exports for stable identifiers and quasi-identifiers (birth date + ZIP + gender), and whether k-anonymity or differential privacy was applied. Check whether the agreement's claimed classification matches custody of the mapping table.

**Bad:**
```python
export = df[["user_id", "zip", "dob", "purchase"]]  # "anonymous"
# join zip+dob against voter file -> names
```

**Good:**
```python
export = anonymize(df, k=20,
    generalize={"dob": "year", "zip": "5->3"})
# or differential-privacy aggregates, not row-level release
```

**References:** GDPR Recital 26 (anonymised vs pseudonymised), NIST SP 800-188 De-Identifying Datasets, Narayanan & Shmatikov

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [database](../categories/database.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Replication Lag

**SHOULD** monitor replication lag as a first-class SLO and make the application degrade explicitly when lag exceeds the tolerated threshold.

**Why:** Silent lag growth means replicas serve increasingly stale data while everything still looks green: dashboards under-report, caches serve outdated permissions, and failover decisions get made on data that stopped being current minutes ago.

**Detect:** Metrics for `pg_stat_replication.replay_lag` / Seconds_Behind_Master wired into alerting; app code that ignores lag when choosing a replica; no fallback to primary when lag > threshold; long-running replica queries and large batch writes identified as lag drivers.

**Bad:**
```python
replica = pick_replica_round_robin()   # 90s behind; nobody notices
return replica.query(report_sql)
```

**Good:**
```python
replica = pick_replica(max_lag='2s')  # skip lagging replicas
if replica is None:
    return primary.query(report_sql)   # explicit, monitored fallback
```

**References:** PostgreSQL Streaming Replication / synchronous replication, MySQL Seconds_Behind_Master, Google SRE Book: SLOs, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

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

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Slow query log captured, reviewed, and regression-tracked

**SHOULD** enable the slow query log (or `pg_stat_statements`) at an SLO-appropriate threshold, review it on a standing cadence, and treat new entrants as regressions worth a ticket.

**Why:** Slow queries are both outage-causing and attacker-friendly: an unindexed query on an auth path is a DoS lever at volume and the first domino of a connection-pool meltdown. A log nobody reads is telemetry theater.

**Detect:** Check `log_min_duration_statement` or MySQL `slow_query_log`/`long_query_time`, and whether `pg_stat_statements` is loaded. Ask for the review artifact — dashboard, weekly triage note, CI perf gate. Enabled-but-unread logs fail too.

**Bad:**
```ini
log_min_duration_statement = -1   # logging disabled
```

**Good:**
```ini
shared_preload_libraries = 'pg_stat_statements'
log_min_duration_statement = 200  # tied to p95 SLO
# weekly triage: new top queries -> tickets
```

**References:** PostgreSQL pg_stat_statements docs, MySQL slow query log docs, Google SRE Book saturation monitoring

---

**Part of:** [database](../categories/database.md) · [observability](../categories/observability.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Soft Deletes

**MUST** filter soft-deleted rows (`deleted_at IS NULL`) in every query path, and enforce that filter centrally rather than per-call.

**Why:** A tombstone column only hides data if every reader honors it; one forgotten predicate leaks "deleted" records into search results or exports — a privacy incident when the row held data a user asked to erase.

**Detect:** Audit each query against `deleted_at`/`is_deleted` tables; check whether the ORM applies a default scope or every call site repeats the condition by hand; inconsistent unique indexes over deleted rows.

**Bad:**
```python
User.query.all()   # includes users who requested deletion
```

**Good:**
```python
class UserQuery(db.Query):
    def all(self):
        return self.filter(User.deleted_at.is_(None)).all()  # default scope
```

**References:** OWASP ASVS V6.4, Rails default_scope docs, PostgreSQL Row Security, CWE-459

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Statement and lock timeouts set explicitly per workload

**SHOULD** configure statement and lock timeouts deliberately per role or connection profile instead of leaving unlimited defaults everywhere; PostgreSQL's `statement_timeout` and `lock_timeout` are the common case.

**Why:** Without a lock timeout, a query queues behind long-running DDL and piles up waiting sessions until the pool collapses. Without a statement timeout, a runaway full-table scan from a bad ORM query pegs CPU and starves latency-sensitive traffic indefinitely.

**Detect:** Grep Postgres configs and pool settings (PgBouncer per-user pools, JDBC `options=-c statement_timeout=...`) for the two keys. If OLTP and reporting roles share identical or absent timeouts, the setting was never considered per workload.

**Bad:**
```ini
statement_timeout = 0
lock_timeout = 0   # waits forever behind a migration
```

**Good:**
```ini
ALTER ROLE app_oltp SET statement_timeout = '5s';
ALTER ROLE app_oltp SET lock_timeout = '2s';
ALTER ROLE reports  SET statement_timeout = '30min';
```

**References:** PostgreSQL timeout config docs, PgBouncer per-user pools, CWE-400 Uncontrolled Resource Consumption

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Volume IOPS/throughput ceilings profiled before launch

**SHOULD** benchmark the storage volume's IOPS and throughput ceilings under a realistic workload before launch, and size expected database load against them with headroom.

**Why:** Cloud volumes advertise tiers, but the database discovers the ceiling at the worst moment: launch day. A volume pinned at its IOPS limit surfaces as mysterious slow queries and rising `await`, and the application gets blamed for a provisioning mistake.

**Detect:** Ask for fio results tied to the launch checklist. Compare peak read/WAL generation against provisioned IOPS in IaC (`aws_ebs_volume.iops`, StorageClass annotations). No storage numbers, no pass.

**Bad:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "gp2"   # burst credits; steady-state surprise
}
```

**Good:**
```hcl
resource "aws_ebs_volume" "pg" {
  type = "io2"
  iops = 8000   # fio peak 5.2k + 50% headroom
}
```

**References:** AWS EBS volume types docs, fio benchmarking guide, Google SRE Book capacity planning

---

**Part of:** [database](../categories/database.md) · [scaling-capacity](../categories/scaling-capacity.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Transactions

**SHOULD** wrap multi-statement writes that must all succeed together in a single database transaction, and keep those transactions short.

**Why:** Without atomicity a crash between statements leaves half-applied state — money debited but not credited. Long transactions are equally dangerous: they hold row locks across network calls, inviting contention and timeouts.

**Detect:** Consecutive writes outside `BEGIN/COMMIT` or a session context manager; `autocommit=True` around paired writes; HTTP or external API calls made inside an open transaction block.

**Bad:**
```python
conn.execute("UPDATE accounts SET bal = bal - 100 WHERE id = 1")
call_external_api()   # crash here = lost debit
conn.execute("UPDATE accounts SET bal = bal + 100 WHERE id = 2")
```

**Good:**
```python
with conn.transaction():
    conn.execute("UPDATE accounts SET bal = bal - 100 WHERE id = 1")
    conn.execute("UPDATE accounts SET bal = bal + 100 WHERE id = 2")
# external call moved outside the lock window
```

**References:** PostgreSQL Transactions docs, MySQL InnoDB Transaction Model, CWE-662

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Unauthenticated data stores exposed (Redis, Elasticsearch, MongoDB, Memcached)

**MUST NOT** expose any datastore port (Redis, Elasticsearch, MongoDB, Memcached, etcd) to a network where untrusted clients can reach it without authentication and network-level restriction.

**Why:** These engines shipped with auth off by default, and scanned-and-looted instances appear daily: Redis dumps of sessions, Elasticsearch clusters of leaked PII. An unauthenticated store on a reachable network is a breach with a countdown timer.

**Detect:** Scan inventories for default ports (6379, 9200, 27017, 11211) bound to `0.0.0.0`; check Redis `requirepass`/ACLs, MongoDB auth, Elasticsearch `xpack.security.enabled`, and security groups opening them beyond the app tier.

**Bad:**
```yaml
kind: Service
spec:
  type: LoadBalancer        # redis straight to the internet
  ports: [{ port: 6379 }]
```

**Good:**
```yaml
spec:
  type: ClusterIP   # plus requirepass and a NetworkPolicy
---
# NetworkPolicy: apps namespace -> redis:6379 only
```

**References:** CWE-306 Missing Authentication for Critical Function, OWASP A02, Redis security docs, Shodan exposed-database research

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [database](../categories/database.md) · [hardening-benchmarks](../categories/hardening-benchmarks.md) · [data](../domains/data.md) · [government-compliance](../domains/government-compliance.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)

# Unique Constraints

**MUST** enforce business-level uniqueness (email, username, SKU per tenant) with database UNIQUE constraints, not just a pre-insert existence check in code.

**Why:** A "check if absent, then insert" sequence is a race: two concurrent requests both pass and both insert, creating duplicate accounts that break login, billing, and support flows. Only the database can arbitrate atomically.

**Detect:** Existence-check-then-create patterns without a unique index behind them; login by email on a table lacking `UNIQUE(email)`; multi-tenant tables missing `UNIQUE(tenant_id, sku)`.

**Bad:**
```python
if not User.query.filter_by(email=e).first():
    db.add(User(email=e))   # two requests, two users, same email
```

**Good:**
```sql
CREATE UNIQUE INDEX users_email_uniq ON users (email);
-- races resolve: one wins, one gets a violation to handle
```

**References:** SQL UNIQUE constraint, OWASP ASVS V3.2, Rails uniqueness-validation index caveat, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# UUIDs vs Auto-Increment

**SHOULD NOT** expose sequential auto-increment identifiers in public URLs or API payloads for resources whose existence or volume is sensitive.

**Why:** Integer IDs leak business information — `orders/1001` today and `orders/1101` tomorrow reveals daily volume — and invite enumeration and IDOR probing. Random UUIDs remove the guesswork, though they carry indexing costs.

**Detect:** Routes using `:id` backed by serial integers on sensitive resources; UUID v1 leaking MAC/timestamps where v4 or ULID fits better.

**Bad:**
```
GET /invoices/4821          # sequential: attacker walks 4822, 4823...
```

**Good:**
```
GET /invoices/9f2c7a4e-1b3d-4e5f-8a6b-c0d1e2f3a4b5   # UUIDv4, unguessable
-- still pair with authorization checks; obscurity is not access control
```

**References:** OWASP ASVS V3.2 / V4.2.1, RFC 4122 (UUID), PostgreSQL uuid vs bigserial notes, CWE-639

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Stalled replication retention accumulating log segments until disk fills

**MUST** monitor log retention pinned by an absent replica or consumer, alerting well below free-disk headroom, since the primary cannot recycle the log segments those retention markers hold open (PostgreSQL replication slots, and their `restart_lag`, are the classic case).

**Why:** A dropped replica leaves its slot behind, and the primary keeps every WAL byte "just in case." Days later the disk fills and the primary — not the missing replica — stops accepting writes. A classic self-inflicted Postgres outage.

**Detect:** Check monitoring on `pg_replication_slots.restart_lag`, inactive-slot state, and disk alerts tied to `pg_wal` growth. Grep runbooks for `pg_drop_replication_slot` and whether replica decommissioning removes its slot.

**Bad:**
```sql
-- replica decommissioned; slot never dropped
SELECT * FROM pg_replication_slots;  -- inactive, lag growing daily
```

**Good:**
```sql
-- alert when restart_lag > 5GB or inactive > 15min
SELECT slot_name, active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag
FROM pg_replication_slots;
```

**References:** PostgreSQL replication slots & WAL retention docs, pgBackRest/WAL-G slot management, CWE-400 disk exhaustion

---

**Part of:** [database](../categories/database.md) · [scaling-capacity](../categories/scaling-capacity.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

