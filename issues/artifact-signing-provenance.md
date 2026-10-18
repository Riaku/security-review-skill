---
categories: [supply-chain]
domains: [infrastructure]
---

# Artifact Signing & Provenance (cosign/Sigstore/SBOM)

**MUST** sign released images and attach provenance attestations plus an SBOM generated inside the trusted build pipeline.

**Why:** Unsigned artifacts can be swapped or forged after build with no way to trace who produced what, defeating every downstream integrity check.

**Detect:** `cosign sign --yes` / `cosign attest` in CI; `syft`/`bom` generation steps; registry entries lacking `.sig` bundles or SPDX/CycloneDX files.

**References:** SLSA L3, Sigstore docs, NIST SP 800-161, NTIA SBOM minimum elements
