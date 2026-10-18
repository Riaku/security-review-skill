---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# CI Runner Isolation

**MUST** run untrusted build jobs on ephemeral, per-job isolated runners with no shared workspace, persistent credentials, or network access to production networks.

**Why:** Reused or shared runners let one malicious job harvest secrets and artifacts left behind by previous builds.

**Detect:** Self-hosted runner labels in workflow `runs-on`; persistent `/var/run/docker.sock` mounts; runner config `ephemeral=false`; shared cache dirs across jobs.

**References:** OWASP CI/CD Top 10 CICD-SEC-7, CWE-419, NIST SP 800-218 (SSDF), GitHub Actions security hardening guide

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
