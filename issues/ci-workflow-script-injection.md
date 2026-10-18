---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# CI Workflow Injection via Untrusted PR Content (pull_request_target)

**MUST NOT** check out or execute pull request code inside a `pull_request_target` or other privileged-trigger job that holds write tokens or secrets.

**Why:** Attacker-controlled PR text interpolated into shell steps runs arbitrary commands with full repo and secret access.

**Detect:** Grep workflows for `pull_request_target` combined with `secrets.`, `${{ github.event.* }}` in `run:` blocks, or `checkout` of `github.event.pull_request.head.sha`.

**References:** OWASP CI Security CS2, CWE-94, NIST SP 800-218 PW.8, GitHub Actions security hardening guide

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
