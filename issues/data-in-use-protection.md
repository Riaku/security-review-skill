---
categories: [compliance-privacy, secrets-crypto]
domains: [backend]
---

# Data In Use Protection

**MUST** minimize sensitive data held in process memory and encrypt or wipe it as soon as processing completes.

**Why:** Rest and transit get checked and memory does not, so plaintext secrets sit in heap dumps, crash reports, and swap long after the request ends.

**Detect:** grep for long-lived plaintext secret buffers and for zeroization calls (`memset_s`, `explicit_bzero`, `zeroize`, `SecureString`) around their use.

**References:** OWASP ASVS v5.0 V11.7.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-316
