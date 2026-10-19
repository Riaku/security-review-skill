# database

Schema, queries, transactions, replication, backup/recovery.

## What this category covers

This category covers the persistent data tier: how schemas are shaped and changed, how queries and transactions behave under concurrency, and how data survives failure. Its member items span schema design (normalization, foreign keys, unique constraints, cascading and soft deletes), query performance (indexes, sequential scans, N+1 access, pagination, full-text search, EXPLAIN review), transactions and locking (ACID, isolation levels, deadlocks, optimistic and pessimistic locking), migrations and rollback, replication and read replicas, backup, restore, and point-in-time recovery, partitioning and sharding, connection pooling, storage throughput, retention and deletion, and exposure of the datastore itself. A reviewer here should look at the database as a system with explicit limits: transaction scope, lock timeouts, replica lag, and recovery objectives, each set deliberately. The recurring failure is a guarantee assumed but never configured: cross-store atomicity, an index that only exists in theory, or a backup that has never been restored.

- Schema design and integrity: normalization, foreign keys, unique constraints, delete semantics.
- Query and index performance: EXPLAIN review, scans, N+1 access, pagination, full-text search.
- Transactions and concurrency: isolation levels, locking, deadlocks, timeout settings.
- Migrations and rollback, including online schema change and cutover for large tables.
- Replication, read replicas, and lag monitoring.
- Backup, restore drills, point-in-time recovery, and durable acknowledgment.

## What it does not cover

- [distributed-systems](../categories/distributed-systems.md) — coordination between nodes (consensus, leader election, quorums, cross-service consistency) belongs there; single-store internals belong here even when the store is replicated.
- [caching](../categories/caching.md) — the application or CDN cache layer belongs there; materialized views and read replicas inside the database belong here.
- [data-pipelines](../categories/data-pipelines.md) — warehouse, ETL, and lineage concerns belong there; the OLTP store and its own retention enforcement belong here.
- [compliance-privacy](../categories/compliance-privacy.md) — the policy of what data may be retained and why belongs there; implementing and verifying deletion across stores belongs here.

## What a finding here looks like

- a commit followed by a queue publish with no outbox, so the event is lost when the publish fails.
- a list endpoint that degrades to a sequential scan once the table outgrows the working set.
- three services updating the same denormalized counter, double-counting on retry.
- nightly dumps with no restore drill ever run and no WAL archiving.
- a replica serving a read-your-own-write query immediately after a write to the primary.
