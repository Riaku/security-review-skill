---
categories: [database]
domains: [data]
---

# Database Selection by Workload (CAP Class Fit)

**SHOULD** choose each datastore deliberately for its workload's read/write consistency requirement and access pattern — strong consistency for transactions/permissions/inventory, tunable consistency for feeds/logs/caches, graph only for deep relationship traversal — and record the rationale, naming the store's configured behaviour under partition (quorum/R+W>N, read preference) rather than a product-level CP/AP label.

**Why:** A wrong datastore choice surfaces years later as a forced migration ("the worst pain imaginable"): an AP store backing balances, or a CP store blocking feeds during partitions.

**Detect:** review architecture docs/ADRs for datastore-per-workload rationale; grep for one store serving contradictory workloads (e.g. Redis as system-of-record, Postgres for firehose telemetry).

**References:** CAP theorem, DDIA ch. 4–9, AWS/Google datastore selection guides
