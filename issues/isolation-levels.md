---
categories: [database]
domains: [data]
---

# Isolation Levels

**SHOULD** set the transaction isolation level deliberately per workload instead of inheriting the driver or framework default blindly.

**Why:** Defaults differ wildly — Postgres ships READ COMMITTED, MySQL InnoDB defaults to REPEATABLE READ. The wrong level admits phantom reads or write skew into money paths, and bugs surface only under concurrency, months after launch.

**Detect:** Grep for `isolation_level` config and `SET TRANSACTION ISOLATION LEVEL`; flag read-modify-write logic running under READ COMMITTED where SERIALIZABLE or row locks are needed.

**Bad:**
```sql
-- READ COMMITTED: two sessions both read balance=100, both "reserve" it
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

**Good:**
```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- or explicit: SELECT ... FOR UPDATE on the row being modified
```

**References:** ANSI SQL-92 isolation levels, PostgreSQL Isolation docs, JEP-001 (Heroku), CWE-362
