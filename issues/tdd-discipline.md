# Test-Driven Development Discipline

**SHOULD** write the failing test before the security fix, watching it go red, then minimal code to green, so the test provably guards the behavior.

**Why:** Tests written after the fix often encode the buggy behavior or skip the exact condition the exploit used.

**Detect:** commit history showing fix commits with no preceding failing-test commit; PRs where tests and fixes arrive simultaneously with no red run in CI logs.

**References:** NIST SP 800-218 PW.7 (test-first practices), OWASP BSIMM TTD-1, CWE-1140 (attempt to use cached test results)
