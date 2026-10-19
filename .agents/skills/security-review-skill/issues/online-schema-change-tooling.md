---
categories: [database, deployment-release]
domains: [data, infrastructure]
---

# Online schema-change tooling for large tables (gh-ost, pt-osc)

**MUST** use a non-blocking migration strategy for schema changes on tables above a defined size instead of a plain blocking `ALTER TABLE`: gh-ost or `pt-online-schema-change` for MySQL, expand-contract/`pgroll` or concurrent-index patterns for Postgres.

**Why:** A naive `ALTER` on a multi-hundred-gigabyte MySQL table can block writes for the whole copy, freezing writes and cascading timeouts through dependent services — and retrying it mid-outage doubles the damage. (gh-ost/pt-osc are MySQL-only; Postgres 11+ makes `ADD COLUMN` with `DEFAULT` metadata-only, but rewrites still need online treatment.)

**Detect:** Scan migration directories for raw `ALTER TABLE` against known-large tables, missing size thresholds in the runbook, and absence of gh-ost/pt-osc in CI/CD. Migrations should declare expected duration and lock behavior.

**Bad:**
```sql
-- 400 GB table: changing a column's type rebuilds the table and blocks
-- concurrent DML (MySQL 8.0 online DDL: Instant No, Permits Concurrent DML No)
ALTER TABLE orders MODIFY promo_code text;
```

**Good:**
```bash
gh-ost --table=orders --alter="MODIFY promo_code text" \
  --execute   # ghost-table copy, seconds-long cutover
```

**References:** GitHub gh-ost docs (MySQL), Percona pt-online-schema-change docs (MySQL), pgroll docs (Postgres), PostgreSQL CREATE INDEX CONCURRENTLY docs
