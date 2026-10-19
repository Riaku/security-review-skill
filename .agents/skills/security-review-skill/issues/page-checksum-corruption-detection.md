---
categories: [database]
domains: [data]
---

# Page checksums enabled to catch silent data corruption

**MUST** enable data page checksums, where the engine offers them, at cluster creation so that bit-rot and storage-layer corruption raise hard errors at read time instead of being served silently; PostgreSQL's `--data-checksums` at `initdb` is the common case; on PostgreSQL 12+ an existing cluster can still be swept with `pg_checksums --enable` during a maintenance window, but the operation rewrites every relation, so schedule that window rather than assuming a rebuild is the only fix.

**Why:** Disks and network storage flip bits without complaint. A corrupted index page can return wrong results or stream corruption to replicas. Checksums make the database loud at the first bad read — loud beats wrong.

**Detect:** Run `pg_controldata | grep -i checksum` or check IaC templates for `data_checksums`. Absence on a new cluster is worth fixing deliberately: the checksums can be added later only by taking the cluster down for a full `pg_checksums --enable` sweep (PG 12+), so on a busy primary it is a maintenance-window decision, not a free toggle.

**Bad:**
```bash
initdb -D /var/lib/postgresql/data   # checksums off
```

**Good:**
```bash
initdb -D /var/lib/postgresql/data --data-checksums
# verify: 'Data page checksum version: 1'
```

**References:** PostgreSQL initdb --data-checksums docs, storage bit-rot literature
