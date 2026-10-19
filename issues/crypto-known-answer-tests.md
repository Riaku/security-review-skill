---
categories: [secrets-crypto]
domains: [backend]
---

# Crypto Known-Answer Tests

**MUST** validate cryptographic code against published known-answer and edge-case test vectors, not only round-trip self-tests.

**Why:** A round trip passes for an implementation that is consistently wrong. Published vectors catch wrong curves, truncation and malformed-input handling.

**Detect:** Run the Wycheproof suite for every primitive in use; a custom wrapper needs its own harness over the same vectors.

**References:** Project Wycheproof, https://github.com/google/wycheproof, Tink, https://github.com/tink-crypto/tink
