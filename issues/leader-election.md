# Leader Election

**MUST** fence stale leaders with a monotonically increasing epoch term before they may serve writes or issue commands.

**Why:** A partitioned old leader that has not noticed its demotion can double-issue work, corrupting state alongside the new leader.

**Detect:** grep election code for missing `epoch`/`term`/`fencing_token` checks, lease TTL longer than failover SLA, workers accepting commands without validating leader epoch.

**References:** Martin Kleppmann "How to do distributed locking", CWE-662, etcd lease documentation
