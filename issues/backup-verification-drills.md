---
categories: [database, sre-incidents]
domains: [data, reliability]
---

# Disaster Recovery & Backup Verification (rehearsed full-site restore drills)

**MUST** maintain a rehearsed recovery plan for full-site loss, with restores verified from actual backups by scheduled restore drills whose results are tracked and failures escalated.

**Why:** Backups never restored are unverified guesses, and DR plans never rehearsed fail when the real disaster arrives: truncated dumps, missing WAL segments, procedures that only work on one engineer's laptop — and ransomware crews routinely destroy backup targets too. Discovering a corrupt set during a real incident converts an outage into permanent loss.

**Detect:** Grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks; a backup job with no matching restore-test job is the finding, as are a missing `dr_plan.md`, disabled `wal_level`/PITR, and offsite sync jobs without checksums. Ask for the last successful restore date and evidence: checksums, row counts, an app booting against restored data.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4, ISO 22301
