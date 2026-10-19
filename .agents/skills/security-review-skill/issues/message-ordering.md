---
categories: [messaging-async]
domains: [data]
---

# Message Ordering

**SHOULD** preserve ordering only where required (per-key, not global) and document where reordering is tolerated; never assume FIFO across partitions.

**Why:** Out-of-order events corrupt state machines — a "cancel" processed before its "create" leaves orphaned records.

**Detect:** grep for `partition_key`, `ordering_key`, `enable.idempotence`, consumers processing multi-partition topics with order-dependent logic.

**References:** Kafka ordering guarantees, CWE-362, AWS SQS FIFO ordering notes
