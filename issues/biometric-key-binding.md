---
categories: [mobile]
domains: [mobile]
---

# Biometric Key Binding

**MUST** bind biometric verification to a keystore key that requires a fresh biometric match and is invalidated when enrollment changes.

**Why:** A biometric check that only returns a boolean leaves the underlying secret valid after fingerprints are added or the device is compromised.

**Detect:** grep for setUserAuthenticationRequired and setInvalidatedByBiometricEnrollment (Android) or kSecAccessControlBiometryCurrentSet (iOS) on key generation

**References:** OWASP MASTG best practices, https://github.com/OWASP/mastg/tree/master/best-practices
