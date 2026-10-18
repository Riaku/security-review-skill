# Post-quantum cryptography migration plan and crypto-agility

**SHOULD** maintain a documented PQC migration plan and crypto-agile design (algorithm negotiation, centralized crypto config) so ciphers can be swapped without rewrites.

**Why:** Systems hard-coded to RSA/ECC today cannot absorb the eventual quantum break of current public-key crypto without costly emergency rework.

**Detect:** Hardcoded `RSA-2048`/`ECDH P-256` with no config indirection, absence of `ML-KEM`/`X25519` hybrid plans, TLS library pinned without upgrade path.

**References:** NIST FIPS 203/204/205, NIST IR 8547 PQC migration, NSA CNSA 2.0
