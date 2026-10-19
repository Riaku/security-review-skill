---
categories: [database]
domains: [data]
---

# Replication Lag

**SHOULD** monitor replication lag as a first-class SLO and make the application degrade explicitly when lag exceeds the tolerated threshold.

**Why:** Silent lag growth means replicas serve increasingly stale data while everything still looks green: dashboards under-report, caches serve outdated permissions, and failover decisions get made on data that stopped being current minutes ago.

**Detect:** Metrics for `pg_stat_replication.replay_lag` / Seconds_Behind_Source wired into alerting; app code that ignores lag when choosing a replica; no fallback to primary when lag > threshold; long-running replica queries and large batch writes identified as lag drivers.

**Bad:**
```python
replica = pick_replica_round_robin()   # 90s behind; nobody notices
return replica.query(report_sql)
```

**Good:**
```python
replica = pick_replica(max_lag='2s')  # skip lagging replicas
if replica is None:
    return primary.query(report_sql)   # explicit, monitored fallback
```

**References:** PostgreSQL Streaming Replication / synchronous replication, MySQL Seconds_Behind_Source, Google SRE Book: SLOs, CWE-362
