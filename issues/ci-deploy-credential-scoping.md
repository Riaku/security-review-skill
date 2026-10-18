---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# CI Deploy-Credential Scoping

**MUST NOT** grant deploy credentials to every workflow; scope each secret and token to the single job and target environment that needs it.

**Why:** Broadly shared deploy keys mean any compromised workflow can push to every environment, including production.

**Detect:** Repo-level `secrets.*` used in many workflows instead of environment-scoped ones; cloud IAM policies with `*` resources attached to CI roles; missing `environment:` stanzas.

**References:** OWASP CI Security CS4, CWE-250, NIST SP 800-218 PS.2, GitHub environments and OIDC deploy docs

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
