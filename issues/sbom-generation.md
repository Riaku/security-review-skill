---
categories: [supply-chain]
domains: [infrastructure]
---

# SBOM Generation & Retention (CycloneDX/SPDX per build, kept for incident response)

**MUST** generate a CycloneDX or SPDX SBOM per build and retain it long enough to answer "were we affected?" in incidents.

**Why:** Without per-build inventories, Log4Shell-style emergencies become weeks of guesswork instead of minutes of lookup.

**Detect:** grep `bom-*.json`, `cyclonedx`, `spdx`, `syft`, `cdxgen` in CI pipelines and artifact repos.

**References:** NTIA SBOM minimum elements, NIST SP 800-161, OWASP CycloneDX, CWE-1357

---

**Part of:** [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
