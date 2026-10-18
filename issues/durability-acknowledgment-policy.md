---
categories: [database]
domains: [data]
---

# Durability Acknowledgment Policy

**MUST** acknowledge writes only after they are durably persisted (sync disk and/or quorum replication) for data where loss is unacceptable — payments, orders, credential changes; latency-first acks are permitted only for reversible data (likes, views, logs).

**Why:** Ack-before-persist means a crash between ack and write silently destroys confirmed data; the client believes the operation succeeded and never retries. Acking before durable persistence is tolerable only when the gap is explicitly backed by a durable queue or WAL (Kafka `acks=all`, Redis AOF `everysec`), never a bare in-memory buffer.

**Detect:** Review write paths for ack-before-flush/async-persist on critical entities; check DB durability settings (`synchronous_commit`, replication ack level, fsync) against the data's loss tolerance; trace the ack point relative to persistence — handler returning 2xx before the enqueue is fsynced, flusher threads with no crash-recovery path or backlog alerting.

**References:** DDIA durability/replication chapters, Postgres synchronous_commit docs, latency-vs-durability trade-off, Kafka semantics docs (acks, idempotent producer), Redis AOF persistence docs

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
