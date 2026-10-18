# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills that prove backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups that were never restored are unverified guesses; ransomware crews routinely encrypt backup targets too, so only tested restores count.

**Detect:** grep for `restore_test`, `drill`, `pg_restore` in scheduled jobs, `velero restore create --from-backup`, AWS Backup restore testing plans, runbook docs with drill dates.

**References:** NIST SP 800-34 (Contingency Planning), CIS Control 11, NIST CSF PR.IP-4, CWE-190 (recovery failure context)
