---
categories: [cicd-pipeline-security, containers-k8s, deployment-release, supply-chain]
domains: [infrastructure]
---

# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** sign released artifacts and attach signed provenance (source, builder, inputs) plus an SBOM generated inside the trusted build pipeline, and **MUST** verify those signatures and checksums at every downstream boundary (before a deployment consumes an artifact, and at cluster admission) so unsigned or mismatched artifacts are rejected rather than merely signed.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream, and without provenance or an SBOM there is no record of which source and builder produced what.

**Detect:** `cosign sign --yes` / `cosign attest` in CI; `syft`/`bom` generation steps; grep `slsa`, `provenance`, `in-toto` in CI configs and release steps; registry entries lacking `.sig` bundles or SPDX/CycloneDX files; deploy jobs pulling images by mutable tag with no digest or checksum verification; grep `cosign verify`, `sigstore`, Kyverno `verifyImages`, `signature_verification: true`, and admission verify rules.

**References:** SLSA v1.0, Sigstore/cosign docs, in-toto attestation framework, NIST SP 800-218 (SSDF), NIST SP 800-161, NTIA SBOM minimum elements, OWASP CI/CD Top 10 CICD-SEC-9, NSA Kubernetes Hardening Guide, CIS K8s 5.5 (Extensible Admission Control), CWE-494, CWE-345
