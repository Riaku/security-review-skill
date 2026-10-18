# Database Migrations

**MUST** manage schema changes through versioned, reviewable migration files applied by tooling — never by ad-hoc SQL run against production.

**Why:** Hand-applied DDL drifts from the repo, so the next deploy assumes a schema that isn't there; unreproducible schema state makes rollback guesswork and turns a routine release into an outage with no audit trail.

**Detect:** Check for framework migrations (Alembic, Flyway, Rails `db/migrate`); flag raw `ALTER TABLE` in ops scripts; diff live schema (`pg_dump --schema-only`) against the repo's migration head.

**Bad:**
```bash
# Friday 17:58, pasted into psql on prod:
psql $PROD -c "ALTER TABLE users ADD COLUMN trial_ends TIMESTAMPTZ;"
```

**Good:**
```python
# alembic/versions/0042_add_trial.py
def upgrade():
    op.add_column('users', sa.Column('trial_ends', sa.DateTime(timezone=True)))
```

**References:** Flyway documentation, Alembic migrations guide, Google SRE Book: Migration Best Practices, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
