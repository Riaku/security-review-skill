---
categories: [distributed-systems]
domains: [data]
---

# Quorums

**MUST** configure read and write sets that intersect (R + W > N) for any data where lost updates are unacceptable, and verify overlap under node loss.

**Why:** Non-overlapping quorums let concurrent writes silently overwrite each other, breaking the very consistency the replica count was bought for.

**Detect:** grep for `replication_factor`, `read_consistency=ONE` with `write_consistency=ONE`, R+W<=N arithmetic in client config or driver defaults.

**References:** Dynamo paper quorum model, Cassandra R/W consistency levels, CWE-362 Race Condition
