# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills proving backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups never restored are unverified guesses; ransomware crews routinely destroy backup targets too.

**Detect:** grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4
