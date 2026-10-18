# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** attach cryptographically signed provenance (build source, builder, inputs) to every published artifact so consumers can verify origin.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream.

**Detect:** grep `slsa`, `provenance`, `attest`, `sigstore`, `cosign attest`, `build_provenance` in CI configs and release steps.

**References:** SLSA v1.0, in-toto, NIST SP 800-218 SSDF PW.4, CWE-494
