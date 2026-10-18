# Policy-as-Code Enforcement (OPA/Sentinel/CEP gates in CI and admission)

**SHOULD** express security requirements as executable policies (OPA/Rego, Sentinel, Cloud Custodian) enforced in CI and admission, not wikis.

**Why:** Documented policies rot and get ignored; code-enforced gates make non-compliant infrastructure physically unable to deploy.

**Detect:** grep `policy.rego`, `opa check`, `sentinel`, `conftest`, Gatekeeper `ConstraintTemplate`, admission webhook policy configs.

**References:** NIST SP 800-53 CM-6, OPA/Gatekeeper docs, CIS Kubernetes Benchmark 5.2

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [deployment-release](../categories/deployment-release.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
