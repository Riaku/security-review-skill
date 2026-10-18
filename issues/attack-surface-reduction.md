# Attack Surface Reduction (deliberate exposure minimization)

**SHOULD NOT** expose administrative interfaces, dashboards, or debug endpoints directly to the public internet without an access broker such as VPN or zero-trust gateway.

**Why:** Every unnecessary open port is a tested entry point; exposed admin panels are routinely brute-forced or exploited via known CVEs.

**Detect:** `admin`, `console`, `/debug`, `:8080`, `:9200`, `kibana`, `phpmyadmin` in public ingress or SecurityGroup rules; Terraform `ingress = 0.0.0.0/0`.

**References:** OWASP ASVS V1.3, CWE-489, NIST SP 800-53 AC-3, CIS Benchmark 5.1

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [security-practices](../categories/security-practices.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
