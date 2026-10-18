# Idle-in-transaction sessions monitored and killed

**MUST** set a bounded `idle_in_transaction_session_timeout` so sessions holding open transactions without activity are terminated automatically.

**Why:** A stalled transaction — a crashed app, a forgotten `BEGIN`, a debugger breakpoint — pins old row versions, blocks vacuum, and holds row locks against live traffic for hours. One leaked session can degrade the entire database.

**Detect:** Check `postgresql.conf` and per-role `ALTER ROLE ... SET` for the unsafe default `idle_in_transaction_session_timeout = 0` or its absence. Verify runbooks query `pg_stat_activity` for long-lived `idle in transaction` states and alert on session age.

**Bad:**
```ini
# postgresql.conf — default, never touched
idle_in_transaction_session_timeout = 0
```

**Good:**
```ini
idle_in_transaction_session_timeout = 60s
ALTER ROLE app_report SET idle_in_transaction_session_timeout = '300s'
```

**References:** PostgreSQL idle_in_transaction_session_timeout docs, CWE-404 Improper Resource Shutdown, pg_stat_activity guides

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
