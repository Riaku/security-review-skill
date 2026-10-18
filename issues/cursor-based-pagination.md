# Cursor-Based Pagination

**SHOULD** paginate large or frequently mutated collections with opaque cursors instead of OFFSET, which degrades and skips rows under concurrent inserts.

**Why:** `OFFSET 100000` forces the database to read and discard every preceding row — free at page 1, a denial-of-service vector at page 5000. Offset paging also shifts results mid-browse, so users see duplicates and miss records.

**Detect:** `?offset=`/`?page=` params on high-volume endpoints; large `LIMIT ... OFFSET ...` in SQL; missing stable sort key (created_at + id) backing cursors.

**Bad:**
```sql
SELECT * FROM events ORDER BY created_at LIMIT 50 OFFSET 100000;
```

**Good:**
```sql
SELECT * FROM events
WHERE (created_at, id) > (:cursor_ts, :cursor_id)
ORDER BY created_at, id LIMIT 50;   -- index seek, stable across inserts
```

**References:** PostgreSQL keyset pagination, Stripe API pagination design, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
