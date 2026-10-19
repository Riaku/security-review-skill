---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Crypto Algorithm Lifecycle States

**MUST** classify every algorithm in use as acceptable, deprecated, legacy-verify-only or disallowed, with per-state rules and dated deadlines.

**Why:** Without explicit states, deprecated primitives keep generating new signatures because nothing distinguishes 'can still verify old data' from 'may be used today'.

**Detect:** Inspect the crypto inventory: each algorithm and key has a state, and code enforces it (legacy keys verify only, never sign).

**References:** NIST SP 800-131A Rev. 2, https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf, BSI TR-02102-2, https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102-2.pdf
