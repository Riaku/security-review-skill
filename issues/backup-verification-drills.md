---
categories: [database, sre-incidents]
domains: [data, reliability]
---

# Backup Verification Drills (scheduled restore tests, not just backup jobs)

**MUST** run scheduled restore drills proving backups actually recover systems, with results tracked and failures escalated.

**Why:** Backups never restored are unverified guesses: truncated dumps, missing WAL segments, procedures that only work on one engineer's laptop — and ransomware crews routinely destroy backup targets too. Discovering a corrupt set during a real incident converts an outage into permanent loss.

**Detect:** Grep `restore_test`, `velero restore create`, `pg_restore` in scheduled jobs, AWS Backup restore-testing plans, drill runbooks; a backup job with no matching restore-test job is the finding. Ask for the last successful restore date and evidence: checksums, row counts, an app booting against restored data.

**References:** NIST SP 800-34, CIS Control 11, NIST CSF PR.IP-4
