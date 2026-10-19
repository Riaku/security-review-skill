---
categories: [secrets-crypto]
domains: [backend]
---

# Unique Nonces

**MUST** generate a fresh nonce or IV for every encryption under a key, and treat AEAD nonce reuse as a release blocker.

**Why:** Nonce reuse under counter-mode AEAD leaks the authentication key, so one repeated nonce breaks every message under that key.

**Detect:** grep fixed or reused IV/nonce material: `iv = b'\x00'`, `nonce = 0`, a module-level `IV` constant, `Random.new(1)` seeds, and counters reset per process.

**References:** OWASP Cryptographic Storage Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
