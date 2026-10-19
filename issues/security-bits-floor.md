---
categories: [secrets-crypto]
domains: [backend]
---

# Security Bits Floor

**MUST** evaluate key strength in bits of security rather than nominal key length, and reject configurations below a documented floor.

**Why:** Nominal-size review passes combinations that are far below the intended strength: a short elliptic curve and a long RSA key are not comparable by length.

**Detect:** grep key configuration for `key_size`, RSA moduli under 3072 bits, and short curves; testssl.sh grade for negotiated strength.

**References:** OWASP ASVS v5.0 V11.2.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-57 Part 1
