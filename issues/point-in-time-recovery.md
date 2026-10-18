# Point-in-Time Recovery

**SHOULD** configure continuous archiving (WAL archiving, binlog retention) so the database recovers to an arbitrary instant, not just the last nightly dump.

**Why:** A nightly backup only protects you to yesterday. An attacker's `DELETE` or a bad migration at 14:00 destroys half a day of transactions unless the write-ahead log is archived continuously and chains into base backups.

**Detect:** Check `archive_mode`/`archive_command` (Postgres) or `log_bin` plus retention (MySQL); confirm base backups record their start LSN/GTID. Verify the archived-log retention window matches the declared RPO.

**Bad:**
```ini
# postgresql.conf
archive_mode = off   # nightly dump only: up to 24h of loss
```

**Good:**
```ini
archive_mode = on
archive_command = 'wal-g wal-push %p'
# base backups every 6h; WAL pushed continuously
```

**References:** PostgreSQL Continuous Archiving & PITR docs, MySQL binlog PITR docs, NIST SP 800-34 RPO guidance

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
