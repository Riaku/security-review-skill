---
categories: [authentication]
domains: [backend]
---

# Email Is Not a Factor

**MUST NOT** treat email possession as a single or second authentication factor; use a dedicated possession or knowledge factor.

**Why:** Email is guarded by the user's weakest password and readable by administrators, forwarding rules, and anyone who resets it.

**Detect:** grep MFA and step-up verification paths for `email` as the delivered or verified factor.

**References:** OWASP ASVS v5.0 V6.3.6, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B
