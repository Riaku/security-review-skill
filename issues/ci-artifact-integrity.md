---
categories: [cicd-pipeline-security, supply-chain]
domains: [infrastructure]
---

# CI Artifact Integrity Handoff

**MUST** sign built artifacts and verify signatures and checksums before downstream deployment consumes them.

**Why:** Unsigned artifacts can be swapped or tampered with between build and deploy with no way to detect the substitution.

**Detect:** Missing `cosign sign`/`sigstore`/`gpg --sign` steps; deploy jobs pulling images by mutable tag without digest pinning; no `.sha256` or provenance attestations in artifact stores.

**References:** OWASP CI Security CS5, CWE-345, NIST SP 800-218 PW.6, SLSA provenance levels, sigstore/cosign docs

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
