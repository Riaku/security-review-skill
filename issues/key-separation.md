---
categories: [secrets-crypto]
domains: [backend]
---

# Key Separation

**MUST** use distinct keys per purpose, environment, and tenant, keeping each key out of the store that holds its ciphertext.

**Why:** Reusing one key couples unrelated security domains, so a single leak spans all of them; co-located keys reduce encryption to obfuscation.

**Detect:** grep for one key identifier or alias used by both signing and encryption, the same key in staging and production configs, and key material in the same bucket, table, or repo as the ciphertext.

**References:** OWASP Key Management Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html
