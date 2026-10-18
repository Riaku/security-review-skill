---
categories: [authentication]
domains: [backend]
---

# Breached & Common Password Blocklist

**SHOULD** reject new or changed passwords found in known-breached or common-password lists (e.g. HaveIBeenPwned k-anonymity API).

**Why:** Reusing a password exposed in a prior breach means credential-stuffing bots will try it against your service within hours of exposure.

**Detect:** grep password policy code for absent blocklist/pwned-password check and no `k-anonymity`/`pwnedPasswords` call; flag policies enforcing character-class composition rules instead of length plus blocklist (NIST SP 800-63B forbids composition rules).

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-521, NCSC Pwned Passwords guidance
