# Branch Protection

**MUST** require reviewed, status-passing pull requests before merging into protected branches, with force-push and branch deletion disabled.

**Why:** Unprotected main branches let anyone push unreviewed or malicious code straight into production builds, bypassing every downstream control.

**Detect:** GitHub settings API `branches/*/protection` — check `enforce_admins`, `required_pull_request_reviews`, `required_status_checks`; grep repo scripts for `push --force` to main; missing `.github/settings.yml` `protected_branches`; CODEOWNERS files.

**References:** OWASP CI/CD Top 10 CICD-SEC-1, CWE-284, NIST SP 800-218 (SSDF), GitHub branch protection docs