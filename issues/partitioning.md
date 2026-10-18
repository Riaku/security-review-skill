# Partitioning

**SHOULD** partition very large tables by a natural access dimension (time, tenant) and verify that queries prune partitions instead of scanning all of them.

**Why:** Without partitioning, retention means `DELETE FROM logs` locking millions of rows while indexes balloon past cache capacity. But a partitioned table whose queries omit the partition key performs worse than an unpartitioned one.

**Detect:** Huge tables with no `PARTITION BY`; queries missing the partition-key predicate (check `EXPLAIN` partitions selected vs total); retention via bulk DELETE instead of `DROP PARTITION`.

**Bad:**
```sql
DELETE FROM access_logs WHERE ts < now() - interval '90 days';  -- locks, bloats WAL
```

**Good:**
```sql
CREATE TABLE access_logs (...) PARTITION BY RANGE (ts);
ALTER TABLE access_logs DETACH PARTITION access_logs_2026_07;
DROP TABLE access_logs_2026_07;   -- instant retention, no lock storm
```

**References:** PostgreSQL partition management docs, MySQL partitioning docs, CWE-400

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
