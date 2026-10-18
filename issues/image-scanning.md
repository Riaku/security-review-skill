---
categories: [supply-chain]
domains: [infrastructure]
---

# Image Scanning

**SHOULD** scan every container image for vulnerabilities and malware at build time and again before deployment, blocking on policy violations.

**Why:** Untested images ship known-exploitable OS packages into production, where runtime patching is rarely possible.

**Detect:** CI steps invoking `trivy image`, `grype`, or `docker scout`; absence of any scan stage in pipeline YAML; registry scan config disabled.

**References:** OWASP A06:2021, CIS Docker 4.9, NIST SP 800-190

---

**Part of:** [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
