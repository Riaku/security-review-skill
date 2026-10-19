---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Cryptographic Inventory

**MUST** maintain a discovered inventory of every key, certificate, and algorithm, recording where each may be used and what it may protect.

**Why:** You cannot rotate, migrate, or audit cryptography you do not know exists, and an unscoped key quietly accumulates uses it was never designed for.

**Detect:** diff the KMS and keystore listings against service configs; `openssl x509 -noout -text` over deployed certificates to capture algorithms and expiry.

**References:** OWASP ASVS v5.0 V11.1.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md
