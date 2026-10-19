---
categories: [authentication]
domains: [backend]
---

# SAML Assertion Single Use

**MUST** process each SAML assertion at most once, rejecting any assertion ID already consumed within the assertion's validity window.

**Why:** Accepting an unsigned assertion is total authentication bypass, and a signed assertion replayed inside its window is the same bypass on a delay.

**Detect:** grep SAML validation for an assertion-ID replay cache keyed by `(issuer, assertion_id)` with retention at least the assertion lifetime.

**References:** OWASP ASVS v5.0 V6.8.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md
