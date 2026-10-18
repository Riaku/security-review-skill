# Branch Protection & Required Reviews (no direct pushes, enforced approval)

**MUST** block direct pushes to protected branches and require reviewed, up-to-date approvals before merge.

**Why:** Unprotected main branches let a single bad or malicious commit ship straight to production, bypassing every downstream control.

**Detect:** GitHub settings `required_status_checks`, `enforce_admins`, `required_pull_request_reviews`; grep CODEOWNERS, `branch_protection`, `protect_develop`.

**References:** OWASP SAMM Code Reviews, NIST SP 800-218 PW.7, CWE-1104, GitHub branch protection docs
