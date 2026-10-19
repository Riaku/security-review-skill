---
categories: [secrets-crypto]
domains: [backend]
---

# No Custom Crypto

**MUST NOT** compose raw cryptographic primitives into a construction where a maintained high-level library provides it (AEAD, sealed box, password hashing, token format).

**Why:** Design errors in crypto are invisible to the designer and fatal in production; maintained libraries already bundle the correct modes and side-channel handling.

**Detect:** grep for hand-built constructions: encrypt-then-MAC assembled by hand, raw `AES`/`Cipher` calls with a separately computed MAC, non-standard token formats, base64 or hex treated as protection.

**References:** OWASP Cryptographic Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
