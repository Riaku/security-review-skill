---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Key Holder Limits

**MUST** distribute each private key to a single holder and each shared secret to no more than two parties, listing every holder in the key policy.

**Why:** Each extra holder is a full copy of the key with no accounting, and for signing keys it also destroys any claim that one party produced the signature.

**Detect:** read the KMS key policy or secret distribution list and count principals per key.

**References:** OWASP ASVS v5.0 V11.1.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-57 Part 1
