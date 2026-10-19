---
categories: [secrets-crypto]
domains: [backend]
---

# Harvest-now-decrypt-later exposure of long-lived confidential data

**MUST** protect data whose confidentiality must outlast ~15 years (health records, identities, keys) with post-quantum or hybrid key agreement, since today's ciphertext can be stored and decrypted later and re-keying does not re-protect ciphertext already archived under the old key.

**Why:** Adversaries archive encrypted traffic and backups now, waiting for quantum or key-compromise advances to unlock them retroactively.

**Detect:** Long-retention archives encrypted only with RSA-2048/ECC, TLS sessions without hybrid KEM, backups with no key-rotation schedule.

**References:** NIST IR 8547, NSA CNSA 2.0 timeline, CISA post-quantum cryptography guidance
