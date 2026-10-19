---
categories: [distributed-systems]
domains: [data]
---

# Quorums

**MUST** configure intersecting read/write quorums (R + W > N) wherever a read must observe the most recent acknowledged write, and use compare-and-set / lightweight transactions (or a single writer per key) wherever concurrent read-modify-write must not lose an update — quorum intersection alone does not prevent lost updates.

**Why:** Non-overlapping quorums return stale reads — a reader can miss the last acknowledged write entirely. But overlap is not atomicity: two concurrent read-modify-write cycles both succeed and the conflict is resolved last-write-wins (usually silently), so keys with lost-update risk need CAS/lightweight transactions or a designated writer.

**Detect:** grep for `replication_factor`, `read_consistency=ONE` with `write_consistency=ONE`, R+W<=N arithmetic in client config or driver defaults.

**References:** Dynamo paper quorum model, Cassandra R/W consistency levels, CWE-362 Race Condition
