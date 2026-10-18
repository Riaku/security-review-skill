# Connection Pooling

**MUST** route application database access through a sized connection pool instead of opening a fresh connection per request.

**Why:** TCP plus TLS plus auth handshake per query adds tens of milliseconds each and, worse, unbounded connection creation exhausts the server's `max_connections`, locking out migrations, health checks, and every other service sharing the database.

**Detect:** Look for `new Pool()` per request or per lambda invocation (serverless cold-start churn); config keys `pool_size`, `max_connections`, `PGBOUNCER_POOL_SIZE`; absence of pgbouncer/pgpool in front of many short-lived workers; `FATAL: too many connections` in DB logs.

**Bad:**
```python
def handler(event, ctx):
    conn = psycopg2.connect(DSN)   # new connection per invocation
    rows = conn.execute(q)
```

**Good:**
```python
pool = psycopg2.pool.ThreadedConnectionPool(2, 20, DSN)  # module-level
def handler(event, ctx):
    with pool.getconn() as conn: ...
```

**References:** PgBouncer documentation, PostgreSQL Connection Pooling docs, OWASP ASVS V3.1, AWS Lambda connection management guide

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
