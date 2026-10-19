---
categories: [authentication]
domains: [backend]
---

# Hashed One-Time Secrets

**MUST** store one-time and recovery codes as salted hashes, so a database read does not hand an attacker the second factor.

**Why:** A plaintext code store hands an attacker the second factor along with the database.

**Detect:** grep for plaintext `otp`/`recovery_code` columns and confirm generation and verification both go through the hash.

**References:** OWASP ASVS v5.0 V6.5.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B
