---
categories: [secrets-crypto]
domains: [backend]
---

# Encrypt Then MAC

**MUST** use authenticated encryption, or encrypt-then-MAC ordering when composing primitives, and never verify after decrypting.

**Why:** Decrypt-before-verify is what powers padding-oracle classes; the ordering, not the primitive choice, is the control.

**Detect:** grep for ciphertext decryption followed by a MAC or tag check (`decrypt(` then `hmac.compare`), and for `AES/CBC/PKCS5Padding` with a separate MAC.

**References:** OWASP ASVS v5.0 V11.3.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-353
