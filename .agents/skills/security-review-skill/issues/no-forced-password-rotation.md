---
categories: [authentication]
domains: [backend]
---

# No Forced Password Rotation

**MUST NOT** force periodic password rotation; keep credentials valid until compromise is suspected or the user rotates them.

**Why:** Calendar rotation produces minimal-delta variants of the same password and floods the reset channel, without removing any attacker's access.

**Detect:** grep for expiry-driven password policy (`password_expires`, `max_password_age`, `chage -M`, `pwdLastSet` enforcement).

**References:** OWASP ASVS v5.0 V6.2.10, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B §5.1.1.2
