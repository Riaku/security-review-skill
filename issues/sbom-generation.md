# SBOM Generation & Retention (CycloneDX/SPDX per build, kept for incident response)

**MUST** generate a machine-readable SBOM (CycloneDX or SPDX) for every build artifact and retain it long enough to answer "were we affected?" during an incident.

**Why:** Without per-build inventories, Log4Shell-style emergencies become weeks of guesswork instead of minutes of lookup.

**Detect:** grep `bom-*.json`, `cyclonedx`, `spdx`, `syft`, `cdxgen`, `SBOM` in CI pipelines and artifact repos.

**References:** NTIA minimum elements, NIST SP 800-161, OWASP CycloneDX, CWE-1357
