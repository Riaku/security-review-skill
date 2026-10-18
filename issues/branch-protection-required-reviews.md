# Branch Protection & Required Reviews (no direct pushes, enforced approval)

**MUST** block direct pushes to protected branches and require reviewed, up-to-date approvals before merge.

**Why:** Unprotected main branches let one bad or malicious commit ship straight to production, bypassing every downstream control.

**Detect:** grep `enforce_admins`, `required_pull_request_reviews`, `required_status_checks` in repo settings-as-code; CODEOWNERS files.

**References:** OWASP SAMM Code Reviews, NIST SP 800-218 PW.7, CWE-1104, GitHub branch protection docs
