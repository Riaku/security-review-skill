---
categories: [database]
domains: [data]
---

# Full Table Scans

**SHOULD NOT** ship list endpoints whose queries degrade to sequential scans once the table exceeds working-set size.

**Why:** A scan that reads every row to return ten is invisible at demo scale but pins disk and CPU at peak; a single crawler or retry storm hitting an unindexed filter can take the database down for everyone.

**Detect:** In `EXPLAIN` output look for `Seq Scan on <big_table>` with high `rows removed by filter`; monitor `pg_stat_user_tables.seq_scan` growth; flag `SELECT *` without LIMIT and unindexed sort columns (`ORDER BY created_at` with no index).

**Bad:**
```sql
SELECT * FROM events WHERE status = 'open' ORDER BY created_at DESC;
-- no index: scans all 40M rows every request
```

**Good:**
```sql
CREATE INDEX idx_events_status_created ON events (status, created_at DESC);
SELECT * FROM events WHERE status = 'open' ORDER BY created_at DESC LIMIT 50;
```

**References:** PostgreSQL EXPLAIN docs, Use The Index Luke: Sequential Scans, OWASP ASVS V3.1, CWE-400
