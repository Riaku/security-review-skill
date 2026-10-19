---
categories: [supply-chain]
domains: [infrastructure]
---

# Signing Transparency Log

**MUST** record signing events in an append-only transparency log that verifiers can audit independently of the signer.

**Why:** Without a public log a compromised signer can forge artifacts and nobody can prove it happened. The log makes signing history auditable after the fact.

**Detect:** `rekor-cli get --uuid` or `cosign verify --certificate-identity` resolving an inclusion proof for each released artifact.

**References:** Sigstore Rekor, https://github.com/sigstore/sigstore, Sigstore Fulcio, https://github.com/sigstore/fulcio
