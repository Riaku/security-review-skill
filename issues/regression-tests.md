---
categories: [testing-strategy]
domains: [backend]
---

# Regression Tests

**MUST** add a permanent test for every fixed security bug before merging the fix, reproducing the reported exploit condition.
**MUST** also cover the variations the fix has to survive — the adjacent sentinel, the ±1 bound, the sibling field — because a guard that excludes only the reported payload passes this test and still misses the bug.

**Why:** Without a pinned regression case, the vulnerability can silently return in a later refactor and ship to production, and a test pinned to the advisory's exact payload certifies a fix that blocks that payload and nothing else.

**Detect:** security fix PRs lacking a corresponding test case; CVE IDs or advisory references absent from test names/comments (e.g. `test_cve_2024_xxx`); a test that replays only the reported payload with no boundary variant beside it.

**References:** OWASP ASVS V1.1.1, NIST SP 800-218 (SSDF) (verification after remediation)
