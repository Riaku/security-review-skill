---
categories: [testing-strategy]
domains: [backend]
---

# Security Re-Check on Fixes

**MUST** re-run the security review and security tests over the area any bug fix touches, including code that was not security-relevant before.

**Why:** Fixes to previously safe code routinely introduce new vulnerabilities, and fix discussion rarely mentions security, so an unreviewed fix is an unreviewed change to the attack surface.

**Detect:** `git show --stat` on the fix commit, then confirm the changed paths are covered by a security test; a conventional-commit 'fix:' prefix is a filter, not the evidence

**References:** Mozilla security-regression study, https://arxiv.org/abs/2207.01942
