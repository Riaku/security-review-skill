---
categories: [secrets-crypto]
domains: [backend]
---

# Weak Crypto Primitives in Application Code

**MUST NOT** use DES, RC4, MD5, SHA-1, ECB mode, or hand-rolled ciphers in application code; standardize on AES-GCM or ChaCha20-Poly1305 via maintained libraries.

**Why:** Broken primitives are publicly broken — collisions, key recovery, and pattern leakage turn "encrypted" data into readable data.

**Detect:** `DES`, `RC4`, `ECB`, `md5(`, `sha1(` in security paths, `Cipher.getInstance("DES")`, custom XOR/"encryption" functions.

**References:** OWASP Cryptographic Storage Cheat Sheet, CWE-327, NIST SP 800-131A
