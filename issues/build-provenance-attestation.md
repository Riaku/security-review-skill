---
categories: [supply-chain]
domains: [infrastructure]
---

# Build Provenance Attestation (SLSA-style signed provenance for artifacts)

**MUST** attach signed provenance (source, builder, inputs) to every published artifact so consumers can verify its origin.

**Why:** Unsigned artifacts let attackers substitute trojaned builds that look identical to legitimate releases downstream.

**Detect:** grep `slsa`, `provenance`, `cosign attest`, `sigstore`, `in-toto` in CI configs and release steps.

**References:** SLSA v1.0, in-toto attestation framework, NIST SP 800-218 (SSDF), CWE-494

---

**Part of:** [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
