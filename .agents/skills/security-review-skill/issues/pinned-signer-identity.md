---
categories: [supply-chain]
domains: [backend]
---

# Pin The Expected Signer

**MUST** pin the expected signer identity for artifacts and code, not merely require that a signature validates.

**Why:** Valid code-signing certificates are sold through resellers, so signature validity answers who signed without saying whether that signer is trusted.

**Detect:** grep verification config for identity allowlists (`cosign verify --certificate-identity`, `codesign -R`, publisher rules) instead of a bare signature-valid check.

**References:** Issued for Abuse: purchasable code-signing certificates, https://arxiv.org/abs/1803.02931
