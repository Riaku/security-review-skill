---
categories: [supply-chain]
domains: [infrastructure]
---

# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** sign released images and attach signed provenance (source, builder, inputs) plus an SBOM generated inside the trusted build pipeline to every published artifact, so consumers can verify both origin and contents.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream, and without provenance or an SBOM there is no record of which source and builder produced what.

**Detect:** `cosign sign --yes` / `cosign attest` in CI; `syft`/`bom` generation steps; grep `slsa`, `provenance`, `in-toto` in CI configs and release steps; registry entries lacking `.sig` bundles or SPDX/CycloneDX files.

**References:** SLSA v1.0, Sigstore/cosign docs, in-toto attestation framework, NIST SP 800-218 (SSDF), NIST SP 800-161, NTIA SBOM minimum elements, CWE-494
