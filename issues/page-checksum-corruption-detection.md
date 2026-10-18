# Page checksums enabled to catch silent data corruption

**MUST** enable data page checksums (`--data-checksums` at initdb, or vendor equivalent) so bit-rot and storage-layer corruption raise hard errors at read time instead of being served silently.

**Why:** Disks and network storage flip bits without complaint. A corrupted index page can return wrong results or stream corruption to replicas. Checksums make the database loud at the first bad read — loud beats wrong.

**Detect:** Run `pg_controldata | grep -i checksum` or check IaC templates for `data_checksums`. Absence on a new cluster is a launch blocker: the setting is fixed at creation.

**Bad:**
```bash
initdb -D /var/lib/postgresql/data   # checksums off
```

**Good:**
```bash
initdb -D /var/lib/postgresql/data --data-checksums
# verify: 'Data page checksum version: 1'
```

**References:** PostgreSQL initdb --data-checksums docs, CWE-17 Unexpected Condition Handling, storage bit-rot literature

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
