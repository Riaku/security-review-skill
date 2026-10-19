---
categories: [supply-chain]
domains: [governance]
---

# SBOM Minimum Elements

**MUST** publish an SBOM per build that names each component's supplier, version, and unique identifier with its dependency edges, and declares what the scan did not cover.

**Why:** An SBOM missing a minimum element cannot answer which version is affected or whom to notify, and an undeclared gap is read as coverage that was never produced.

**Detect:** grep each components[] entry for supplier, version, purl and dependencies, and for a declared scope or completeness field

**References:** NTIA SBOM minimum elements conformance checker, https://github.com/spdx/ntia-conformance-checker
