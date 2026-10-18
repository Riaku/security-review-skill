# Testing Your Restores

**MUST** restore backups onto a scratch environment on a recurring schedule and verify the data — an untested backup is not a backup.

**Why:** Backups fail silently: truncated dumps, missing WAL segments, procedures that only work on one engineer's laptop. Discovering a corrupt set during a real incident converts an outage into permanent loss.

**Detect:** Backup jobs with no matching restore-test job or CI pipeline. Ask for the last successful restore date and evidence: checksums, row counts, an app booting against restored data.

**Bad:**
```bash
# runs nightly; nobody has ever restored it
0 2 * * * pg_dump mydb > /backups/mydb.sql
```

**Good:**
```bash
# weekly drill into a throwaway database
pg_restore -d scratch_test --no-owner /backups/latest.dump \
  && scripts/verify_checksums.sh
```

**References:** NIST SP 800-34 (restore testing), CIS Control 11 (tested data recovery), AWS Backup restore testing docs
