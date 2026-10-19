---
categories: [secrets-crypto]
domains: [backend]
---

# RNG Output Validation

**MUST** confirm the random source stays secure under heavy demand and does not fall back to a non-cryptographic generator.

**Why:** Generators degrade under forking and pool exhaustion, and some produce keys that are factorable — the failure is in the output, not the call.

**Detect:** grep for fallback branches to `random`, `rand()`, or a `/dev/urandom` exhaustion handler, then load test the entropy path under concurrency.

**References:** OWASP ASVS v5.0 V11.5.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-90A/B
