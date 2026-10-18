# Stalled replication slots accumulating WAL until disk fills

**MUST** monitor replication slot retention (`restart_lag`, slot activity) with alerts well below free-disk headroom, since an inactive slot pins WAL the primary cannot recycle.

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

---

**Part of:** [database](../categories/database.md) · [scaling-capacity](../categories/scaling-capacity.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
