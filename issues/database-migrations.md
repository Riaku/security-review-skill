---
categories: [database]
domains: [data]
---

# Database Migrations

**MUST** apply schema changes through versioned, reviewable migration files run as an explicit, observable deploy step — never ad-hoc SQL against production, never at application startup.

**Why:** Hand-applied DDL drifts from the repo, so the next deploy assumes a schema that isn't there; unreproducible schema state makes rollback guesswork and turns a routine release into an outage with no audit trail, while migrating at startup hands the app's role DDL rights and lets replicas race on the same change.

**Detect:** Check for framework migrations (Alembic, Flyway, Rails `db/migrate`); flag raw `ALTER TABLE` in ops scripts and a migration runner invoked at process start (`AUTO_MIGRATE`, `db.migrate()` in an entrypoint); diff live schema (`pg_dump --schema-only`) against the repo's migration head.

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
