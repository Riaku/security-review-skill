---
categories: [distributed-systems]
domains: [data]
---

# Split Brain

**MUST NOT** allow two nodes to both believe they are primary; enforce quorum-based fencing or STONITH before accepting dual-master state.

**Why:** Two active masters write divergent data that cannot be merged, causing irreversible corruption of databases and shared storage.

**Detect:** grep cluster config for `no-quorum-policy=ignore`, missing `stonith`, `skipped` fencing, heartbeat over untrusted network, `replication_mode=async` with dual-writable VIPs.

**References:** PACEMAKER fencing docs, CWE-662, NIST SP 800-34 Contingency Planning
