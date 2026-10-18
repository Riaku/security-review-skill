# Branch Protection

**MUST** require reviewed, status-passing pull requests before merging into protected branches, with force-push and branch deletion disabled.

**Why:** Unprotected main branches let anyone push unreviewed or malicious code straight into production builds.

**Detect:** GitHub settings API `branches/*/protection`; grep repo scripts for `push --force` to main; missing `.github/settings.yml` `protected_branches`.

**References:** OWASP CI Security CS1, CWE-284, NIST SP 800-218 PW.7, GitHub branch protection docs
