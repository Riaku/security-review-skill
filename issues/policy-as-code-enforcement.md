# Policy-as-Code Enforcement (OPA/Sentinel/CEP gates in CI and admission)

**SHOULD** express security requirements as executable policies (OPA/Rego, Sentinel, CEF/Cloud Custodian) enforced in CI and at admission, not in wikis.

**Why:** Documented policies rot and get ignored; code-enforced gates make non-compliant infrastructure physically unable to deploy.

**Detect:** grep for `rego` files, `policy.rego`, `opa check`, `sentinel policy`, `admission webhook`, `conftest`, `gatekeeper constraint templates` in repos and cluster configs.

**References:** NIST SP 800-53 CM-6, OPA documentation, Open Policy Agent admission control,OPA Gatekeeper, CIS Kubernetes 5.2
