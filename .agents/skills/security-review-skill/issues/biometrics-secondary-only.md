---
categories: [authentication]
domains: [backend, mobile]
---

# Biometrics Secondary Only

**MUST** use biometrics only as a secondary factor paired with something the user has or knows.

**Why:** Biometrics cannot be revoked or reissued, and a copied or coerced fingerprint authenticates forever.

**Detect:** walk the login flow and check whether a biometric success alone issues a session.

**References:** OWASP ASVS v5.0 V6.5.7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B
