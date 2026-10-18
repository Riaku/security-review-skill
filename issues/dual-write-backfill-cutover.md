# Dual-write plus backfill migration cutover rehearsed

**SHOULD** rehearse the full dual-write → backfill → verify → cutover sequence on a staging copy of production data before running it live, with tested rollback at each phase.

**Why:** These migrations have four independent failure modes — dual-write drift, backfill gaps, verifier blind spots, cutover races — and each discovered in production means reconciling divergent datasets by hand under an outage clock.

**Detect:** Require a runbook with phase gates and a rehearsal log. The verifier must compare full datasets with counts plus checksums, not spot checks; cutover and rollback need dry-run evidence.

**Bad:**
```text
runbook: "write to both DBs, backfill, switch reads"
rehearsal: none — the first live run is the test
```

**Good:**
```text
staging: dual-write 48h → backfill → checksum diff = 0
→ cutover drill → rollback drill, each timed and logged
```

**References:** AWS DMS dual-run/verification guidance, expand-migrate-contract migration pattern docs, NIST SP 800-34 rehearsal requirements
