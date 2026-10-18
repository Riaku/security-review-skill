---
categories: [database]
domains: [data]
---

# Automatic database maintenance enabled and tuned

**SHOULD** keep the engine's automatic space-reclamation and maintenance enabled and tuned per table rather than disabling it in favour of hand-rolled cron jobs; PostgreSQL `autovacuum` and its scale factors are the common case.

**Why:** Superseded row versions accumulate; without regular maintenance tables bloat, plans degrade, and in PostgreSQL the transaction ID counter can approach wraparound, forcing emergency single-user mode to avoid corruption.

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
