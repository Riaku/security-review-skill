# Time Zones

**MUST** store and compare timestamps in UTC, converting to local time only at the display layer.

**Why:** Mixing local and UTC times corrupts ordering, scheduling, and audit trails when users or servers span zones.

**Detect:** `datetime.now()` / `new Date()` without `tz=utc`, `localtime` in Postgres columns, `TIMESTAMP` instead of `TIMESTAMPTZ`, hardcoded `+08:00` offsets.

**References:** CWE-1091, NIST SP 800-53 AU-3, ISO 8601
