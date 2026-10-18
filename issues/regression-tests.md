# Regression Tests

**MUST** add a permanent test for every fixed security bug before merging the fix, reproducing the exact exploit condition.

**Why:** Without a pinned regression case, the vulnerability can silently return in a later refactor and ship to production.

**Detect:** security fix PRs lacking a corresponding test case; CVE IDs or advisory references absent from test names/comments (e.g. `test_cve_2024_xxx`).

**References:** OWASP ASVS V4.1.1, CWE-757, NIST SP 800-218 RV.1 (verification after remediation)

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
