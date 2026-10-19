---
categories: [authentication, authorization-access-control]
domains: [backend]
---

# Admin Reset Blindness

**MUST** let administrators trigger a password reset without ever setting, viewing, or learning the user's password.

**Why:** An admin who knows the user's password destroys non-repudiation: every later action by that account is plausibly the administrator's.

**Detect:** grep admin endpoints for a `new_password` or generated-password field targeting another user id.

**References:** OWASP ASVS v5.0 V6.4.6, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md
