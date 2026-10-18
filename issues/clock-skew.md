# Clock Skew

**SHOULD NOT** rely on wall-clock timestamps for ordering, leases, or token expiry across nodes without NTP/PTP discipline and bounded-skew checks.

**Why:** Skewed clocks make a token look valid past expiry or a lease appear unexpired, granting access or authority that was revoked.

**Detect:** grep for `time.time()`/`Date.now()` in lease/JWT logic, missing `ntp`/`chrony` in host config, `clock_drift` tolerance unset, no `logical clock`/HLC fallback.

**References:** Google Spanner TrueTime, CWE-1009 (Depends on time), NIST SP 800-186 time sync guidance
