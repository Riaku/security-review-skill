---
categories: [authentication]
domains: [backend]
---

# Trusted Time for TOTP

**MUST** validate time-based codes against a trusted server time source, never a client-supplied or unsynchronized clock.

**Why:** Reading the clock from the request turns the validity window into attacker-controlled slack that keeps a stolen code alive.

**Detect:** grep TOTP verification for a time value taken from the request body or headers instead of the server clock.

**References:** OWASP ASVS v5.0 V6.5.8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, RFC 6238 (TOTP)
