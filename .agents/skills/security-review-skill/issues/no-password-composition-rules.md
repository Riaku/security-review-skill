---
categories: [authentication]
domains: [backend]
---

# No Password Composition Rules

**MUST NOT** impose character-class composition rules on passwords; enforce a minimum length and accept long passphrases instead.

**Why:** Composition rules push users toward predictable transforms of familiar words, producing passwords that satisfy the meter and fall to the first dictionary.

**Detect:** grep password validation for upper/lower/digit/symbol regexes and for a `maxlength` that blocks passphrases.

**References:** OWASP ASVS v5.0 V6.2.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B §5.1.1.2
