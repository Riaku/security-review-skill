---
categories: [database, deployment-release]
domains: [data, infrastructure]
---

# Online schema-change tooling for large tables (gh-ost, pt-osc)

**MUST** use a live-migration tool (gh-ost, `pt-online-schema-change`, or a non-blocking Postgres equivalent) for schema changes on tables above a defined size instead of a plain blocking `ALTER TABLE`.

**Why:** A naive `ALTER` on a multi-hundred-gigabyte table can hold an exclusive lock for hours, freezing writes and cascading timeouts through dependent services — and retrying it mid-outage doubles the damage.

**Detect:** Scan migration directories for raw `ALTER TABLE` against known-large tables, missing size thresholds in the runbook, and absence of gh-ost/pt-osc in CI/CD. Migrations should declare expected duration and lock behavior.

**Bad:**
```sql
-- 400 GB table, exclusive lock for hours
ALTER TABLE orders ADD COLUMN promo_code varchar(32);
```

**Good:**
```bash
gh-ost --table=orders --alter="ADD COLUMN promo_code varchar(32)" \
  --execute   # ghost-table copy, seconds-long cutover
```

**References:** GitHub gh-ost docs, Percona pt-online-schema-change docs, PostgreSQL CREATE INDEX CONCURRENTLY docs

---

**Part of:** [database](../categories/database.md) · [deployment-release](../categories/deployment-release.md) · [data](../domains/data.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
