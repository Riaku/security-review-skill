---
categories: [database]
domains: [data]
---

# Foreign Keys

**MUST** declare foreign key constraints on relational columns rather than relying on application-level "we always check first" logic.

**Why:** Orphaned rows accumulate the moment a delete races an insert, a migration misses a table, or a new service writes directly to the DB. Orphans corrupt joins and make restores a forensic exercise.

**Detect:** `*_id` columns lacking `REFERENCES`; ORM models with bare integers instead of relationship definitions; manual existence checks before insert (TOCTOU window); FK enforcement disabled for migration speed and never re-enabled.

**Bad:**
```sql
CREATE TABLE orders (id INT, customer_id INT);  -- no constraint: orphans welcome
```

**Good:**
```sql
CREATE TABLE orders (
  id INT PRIMARY KEY,
  customer_id INT NOT NULL REFERENCES customers(id)
);
```

**References:** SQL:2016 referential integrity, PostgreSQL FOREIGN KEY constraints, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
