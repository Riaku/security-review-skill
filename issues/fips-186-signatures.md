---
categories: [regulatory-frameworks, secrets-crypto]
domains: [backend, government-compliance]
---

# FIPS 186 / Digital Signature Standards

**SHOULD** generate and verify digital signatures using approved algorithms (ECDSA, RSA per FIPS 186-5) with approved curves and key lengths only.

**Why:** Deprecated curves and short keys make signatures forgeable, undermining code signing, tokens, and non-repudiation guarantees.

**Detect:** grep for signature algorithm config: "RSA-1024", "DSA", "secp112", disabled curves; verify "P-256", "P-384", "RSA-2048+" in signing code.

**References:** FIPS 186-5, NIST SP 800-89, RFC 8785

---

**Part of:** [regulatory-frameworks](../categories/regulatory-frameworks.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
