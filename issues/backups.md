# Backups

**MUST** back up every stateful datastore on a defined schedule with a documented recovery point objective (RPO) agreed with the data owner.

**Why:** Without scheduled backups, one disk failure, ransomware event, or accidental `DROP TABLE` becomes permanent data loss — and an undocumented cadence means nobody knows how much a restore will actually lose.

**Detect:** Look for absence of `pg_dump`/`mysqldump`/snapshot jobs, missing backup sidecars in Helm charts or StatefulSet manifests, and no `backup` keys in IaC. Confirm retention settings and that backup success is alerted, not just logged.

**Bad:**
```yaml
# StatefulSet with no backup job and no snapshot policy
kind: StatefulSet
metadata:
  name: postgres
```

**Good:**
```bash
# nightly, encrypted, shipped offsite
pg_dump -Fc mydb | age -r "$BACKUP_PUBKEY" \
  | aws s3 cp - s3://backups/mydb/$(date +%F).dump
```

**References:** NIST SP 800-34 Contingency Planning, CIS Controls v8 (data protection), OWASP ASVS V7

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
