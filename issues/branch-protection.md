---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# Branch Protection

**MUST** require reviewed, status-passing pull requests before merging into protected branches, with force-push and branch deletion disabled.

**Why:** Unprotected main branches let anyone push unreviewed or malicious code straight into production builds, bypassing every downstream control.

**Detect:** GitHub settings API `branches/*/protection` — check `enforce_admins`, `required_pull_request_reviews`, `required_status_checks`; grep repo scripts for `push --force` to main; missing `.github/settings.yml` `protected_branches`; CODEOWNERS files.

**References:** OWASP CI Security CS1, CWE-284, NIST SP 800-218 PW.7, GitHub branch protection docs

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
