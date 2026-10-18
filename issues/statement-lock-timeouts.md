---
categories: [database]
domains: [data]
---

# Statement and lock timeouts set explicitly per workload

**SHOULD** configure statement and lock timeouts deliberately per role or connection profile instead of leaving unlimited defaults everywhere; PostgreSQL's `statement_timeout` and `lock_timeout` are the common case.

**Why:** Without a lock timeout, a query queues behind long-running DDL and piles up waiting sessions until the pool collapses. Without a statement timeout, a runaway full-table scan from a bad ORM query pegs CPU and starves latency-sensitive traffic indefinitely.

**Detect:** Grep Postgres configs and pool settings (PgBouncer per-user pools, JDBC `options=-c statement_timeout=...`) for the two keys. If OLTP and reporting roles share identical or absent timeouts, the setting was never considered per workload.

**Bad:**
```ini
statement_timeout = 0
lock_timeout = 0   # waits forever behind a migration
```

**Good:**
```ini
ALTER ROLE app_oltp SET statement_timeout = '5s';
ALTER ROLE app_oltp SET lock_timeout = '2s';
ALTER ROLE reports  SET statement_timeout = '30min';
```

**References:** PostgreSQL timeout config docs, PgBouncer per-user pools, CWE-400 Uncontrolled Resource Consumption
