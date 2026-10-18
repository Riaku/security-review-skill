---
categories: [api-design, database]
domains: [backend, data]
---

# Batching (many writes/calls, one trip)

**SHOULD** coalesce many small writes or downstream calls into batches sized to the workload instead of one network round trip per record.

**Why:** Per-record round trips multiply latency and connection consumption linearly; a burst that a batched writer absorbs in seconds can exhaust the connection pool and queue the whole service behind it — a self-inflicted availability problem.

**Detect:** Look for `for` loops calling `insert()`, `publish()`, or POST per item where a `bulk_insert`/`executemany`/bulk API exists. Check producers for missing batch tuning (Kafka `linger.ms`/`batch.size`, flush intervals in log and metrics shippers).

**Bad:**
```python
for row in rows:
    db.execute("INSERT INTO t VALUES (%s)", row)  # N trips
```

**Good:**
```python
execute_values(insert_stmt, rows, page_size=1000)  # one trip per page
```

**References:** Arjay McCandless System Design Cheat Sheet (batching), psycopg execute_values docs, Kafka batch.size/linger.ms docs

---

**Part of:** [api-design](../categories/api-design.md) · [database](../categories/database.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
