---
categories: [database]
domains: [data]
---

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
    conn = pool.getconn()
    try:
        ...
    finally:
        pool.putconn(conn)   # `with conn:` would only end the transaction
```

**References:** PgBouncer documentation, PostgreSQL Connection Pooling docs, psycopg2 pool docs (getconn/putconn), AWS Lambda connection management guide
