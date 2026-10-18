---
categories: [database, scaling-capacity]
domains: [data, reliability]
---

# Stalled replication retention accumulating log segments until disk fills

**MUST** monitor log retention pinned by an absent replica or consumer, alerting well below free-disk headroom, since the primary cannot recycle the log segments those retention markers hold open (PostgreSQL replication slots, and their `restart_lag`, are the classic case).

**Why:** A dropped replica leaves its slot behind, and the primary keeps every WAL byte "just in case." Days later the disk fills and the primary — not the missing replica — stops accepting writes. A classic self-inflicted Postgres outage.

**Detect:** Check monitoring on `pg_replication_slots.restart_lag`, inactive-slot state, and disk alerts tied to `pg_wal` growth. Grep runbooks for `pg_drop_replication_slot` and whether replica decommissioning removes its slot.

**Bad:**
```sql
-- replica decommissioned; slot never dropped
SELECT * FROM pg_replication_slots;  -- inactive, lag growing daily
```

**Good:**
```sql
-- alert when restart_lag > 5GB or inactive > 15min
SELECT slot_name, active,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag
FROM pg_replication_slots;
```

**References:** PostgreSQL replication slots & WAL retention docs, pgBackRest/WAL-G slot management, CWE-400 disk exhaustion
