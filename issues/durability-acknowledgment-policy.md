# Durability Acknowledgment Policy

**MUST** acknowledge writes only after they are durably persisted (sync disk and/or quorum replication) for data where loss is unacceptable — payments, orders, credential changes; latency-first acks are permitted only for reversible data (likes, views, logs).

**Why:** Ack-before-persist means a crash between ack and write silently destroys confirmed data; the client believes the operation succeeded and never retries.

**Detect:** review write paths for ack-before-flush/async-persist on critical entities; check DB durability settings (`synchronous_commit`, replication ack level, fsync) against the data's loss tolerance.

**References:** DDIA durability/replication chapters, Postgres synchronous_commit docs, latency-vs-durability trade-off
