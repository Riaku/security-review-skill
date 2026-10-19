---
categories: [authentication]
domains: [backend, mobile]
---

# Push Bombing Defense

**MUST** rate-limit push authentication prompts and require number or context matching so repeated approvals cannot be fatigued through.

**Why:** An approve-anything prompt under volume turns the user into the attacker's second factor, one reflexive tap at a time.

**Detect:** grep push MFA config for number matching and a prompt rate limit (`number_matching`, `push_rate_limit`, `max_attempts`).

**References:** OWASP ASVS v5.0 V6.6.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, NIST SP 800-63B
