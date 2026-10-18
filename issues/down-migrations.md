# Down Migrations

**MUST** provide a tested `downgrade` (rollback) path for every schema migration that touches production data.

**Why:** Releases get rolled back mid-incident; a migration without a working reverse leaves the schema ahead of the old code, converting a five-minute revert into hours of manual surgery under pressure — and untested reversals frequently destroy data when finally attempted.

**Detect:** Alembic revisions with `pass` in `downgrade()`; Flyway migrations lacking `V__`/`U__` pairs; irreversible operations (`DROP TABLE`, `DROP COLUMN`, type narrowing) shipped without a backup-and-expand step; CI that never runs `upgrade -> downgrade -> upgrade`.

**Bad:**
```python
def downgrade():
    pass   # "we won't need this" — until the 2 a.m. rollback
```

**Good:**
```python
def downgrade():
    op.drop_column('users', 'trial_ends')   # exercised in CI against a prod clone
```

**References:** Alembic Rolling Back Migrations, Flyway Undo Migrations, Google SRE Book: Rollback, CWE-1105

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
