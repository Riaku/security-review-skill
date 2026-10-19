---
categories: [secrets-crypto]
domains: [backend]
---

# KDF Input Handling

**MUST NOT** pre-hash, truncate, or case-fold a password in a way that shrinks its verifier space before the key-derivation function.

**Why:** A fast unsalted pre-hash recreates pass-the-hash, and naive truncation silently shortens every password past the limit.

**Detect:** grep `password[:N]`, `substr(password`, `md5(password)`, `sha1(password)` inside the hashing helper, and client-side hashing before the request is sent.

**References:** OWASP Password Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
