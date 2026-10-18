---
categories: [database, sre-incidents]
domains: [data, reliability]
---

# Crash-consistent volume snapshots vs logical dumps distinguished

**SHOULD** document, per datastore, whether each backup is crash-consistent (volume snapshot) or logically consistent (`pg_dump`, `mysqldump`), and use the right one per recovery scenario.

**Why:** A raw volume snapshot of a running database captures whatever was in page cache at capture time; the engine may need crash recovery, and some configurations produce unrestorable sets. Mixing them up means discovering at restore time that the "backup" was never a valid restore point.

**Detect:** The backup matrix should state each method's consistency guarantee; volume-snapshot jobs over hot databases must pair with WAL/binlog archiving.

**Bad:**
```yaml
# snapshotting a hot Postgres PVC, no WAL archiving
backup: ebs-snapshot, volume: postgres-data
```

**Good:**
```yaml
backup: pg_basebackup + wal-archive  # restore-point capable
# volume snapshots reserved for whole-VM DR only
```

**References:** EBS/PersistentVolume snapshot consistency docs, PostgreSQL backup methods docs, NIST SP 800-34

---

**Part of:** [database](../categories/database.md) · [sre-incidents](../categories/sre-incidents.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
