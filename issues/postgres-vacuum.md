---
categories: [database]
domains: [data]
---

# Postgres VACUUM

**SHOULD** keep autovacuum enabled and tuned per-table rather than disabling it for hand-rolled cron vacuuming.

**Why:** MVCC leaves dead tuples behind; without regular vacuuming, tables bloat, plans degrade, and the transaction ID counter can approach wraparound, forcing emergency single-user mode to avoid corruption.

**Detect:** Grep configs for `autovacuum = off`, oversized `autovacuum_vacuum_scale_factor`, or `VACUUM FULL` in cron. Check `pg_stat_user_tables` for high `n_dead_tup` and missing per-table `reloptions` on high-churn tables.

**Bad:**
```ini
# postgresql.conf — "tuned for performance"
autovacuum = off
```

**Good:**
```sql
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 2ms
);
```

**References:** PostgreSQL Routine Vacuuming docs, CWE-400 Uncontrolled Resource Consumption, PG transaction-ID wraparound docs

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
