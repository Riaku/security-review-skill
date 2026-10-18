---
categories: [sre-incidents]
domains: [reliability]
---

# Disaster Recovery

**MUST** maintain a rehearsed recovery plan for full-site loss, with restore verified from actual backups.

**Why:** Never-restored backups are unverified files; untested DR plans fail when the real disaster arrives.

**Detect:** `dr_plan.md`, `backup_schedule` cron, absence of restore-test logs, `wal_level`/PITR disabled, offsite sync jobs without checksums.

**References:** NIST SP 800-34, ISO 22301, CWE-190 (backup integrity gaps)

---

**Part of:** [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
