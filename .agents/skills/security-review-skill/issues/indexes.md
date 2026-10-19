---
categories: [database]
domains: [data]
---

# Indexes

**SHOULD** add supporting indexes for the selective predicates, joins, and sorts a hot query actually uses, verified with `EXPLAIN`, rather than indexing every column named in WHERE, JOIN, or ORDER BY.

**Why:** Missing indexes turn routine lookups into sequential reads; under load this saturates the buffer pool and can cascade into denial of service from what looks like ordinary traffic.

**Detect:** Grep query code for filter columns, then compare against migration files for `CREATE INDEX` / `add_index`. Check slow-query logs and `pg_stat_user_tables.seq_scan` counts.

**Bad:**
```sql
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, created_at TIMESTAMPTZ);
-- hot path: SELECT * FROM orders WHERE customer_id = ?  (no index -> full scan)
```

**Good:**
```sql
CREATE TABLE orders (id SERIAL PRIMARY KEY, customer_id INT, created_at TIMESTAMPTZ);
CREATE INDEX idx_orders_customer ON orders (customer_id);
```

**References:** Use The Index Luke, MySQL indexing best practices, PostgreSQL CREATE INDEX docs, CWE-400
