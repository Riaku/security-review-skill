---
categories: [secrets-crypto]
domains: [backend]
---

# Hashing vs Encryption

**MUST NOT** store passwords with reversible encryption; use one-way password hashing, and reserve encryption only for data that legitimately needs recovery.

**Why:** Encrypted password stores can be decrypted when the key leaks, exposing every credential at once in plaintext form.

**Detect:** `AES`, `encrypt(` near `password` fields, `Fernet`, `cryptography.fernet` applied to user credentials, ORM column named `encrypted_password`.

**References:** OWASP Password Storage Cheat Sheet, CWE-257, NIST SP 800-63B §5.1.1.2
