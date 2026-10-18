---
categories: [database]
domains: [data]
---

# Materialized Views

**MAY** serve data from materialized views, but the freshness contract MUST be explicit: every consumer must know the maximum staleness and refresh schedule.

**Why:** A materialized view is a snapshot; serving it where live data is assumed can leak stale authorization decisions — a revoked user still appearing entitled — or stale financial aggregates. A plain `REFRESH` also blocks all reads unless run `CONCURRENTLY`.

**Detect:** Find `CREATE MATERIALIZED VIEW` statements and trace whether a refresh job exists and exposes its lag. Grep for auth or permission logic sourced from a matview with no staleness check.

**Bad:**
```sql
CREATE MATERIALIZED VIEW user_perms AS
  SELECT user_id, can_admin FROM ...;
-- never refreshed; auth reads a months-old snapshot
```

**Good:**
```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY user_perms;
-- scheduled every 5 min; endpoint exposes last_refreshed_at
```

**References:** PostgreSQL MATERIALIZED VIEW / REFRESH CONCURRENTLY docs, OWASP A05 Security Misconfiguration

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
