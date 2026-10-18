---
categories: [database]
domains: [data]
---

# Database Selection by Workload (CAP Class Fit)

**SHOULD** choose each datastore deliberately for its workload's CAP class and access pattern — CP for transactions/permissions/inventory, AP for feeds/logs/caches, graph only for deep relationship traversal — and record the rationale.

**Why:** A wrong datastore choice surfaces years later as a forced migration ("the worst pain imaginable"): an AP store backing balances, or a CP store blocking feeds during partitions.

**Detect:** review architecture docs/ADRs for datastore-per-workload rationale; grep for one store serving contradictory workloads (e.g. Redis as system-of-record, Postgres for firehose telemetry).

**References:** CAP theorem, DDIA ch. 4–9, AWS/Google datastore selection guides
