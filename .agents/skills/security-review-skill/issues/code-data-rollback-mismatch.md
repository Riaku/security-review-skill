---
categories: [database, deployment-release]
domains: [data, infrastructure]
---

# Code rollback without data rollback causes schema mismatch

**MUST NOT** roll application code back past a schema migration unless that migration is backward-compatible with the old code or a tested compensating migration exists.

**Why:** Migrations move the schema forward while old code expects the old shape: a dropped column or NOT NULL addition makes the rolled-back binary error out or silently write wrong data.

**Detect:** Review migrations paired with the deploy plan: flag destructive changes (`DROP COLUMN`, rename, narrowing types) in the same release; check the scheme is expand-contract — additive first, cleanup after old code is gone.

**Bad:**
```sql
-- release 41: destructive rename (and an index/query that still says `total`)
ALTER TABLE orders RENAME COLUMN total TO amount_cents;
-- rollback to 40: old code queries `total`, which no longer exists
```

**Good:**
```sql
-- expand: add nullable, backfill; contract in a later release
ALTER TABLE orders ADD COLUMN amount_cents bigint;
```

**References:** Fowler Evolutionary Database Design (expand/contract), Marten migration docs, DORA rollback practices
