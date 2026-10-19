---
categories: [authentication]
domains: [backend]
---

# Weakest Auth Assumption

**MUST** assume the weakest authentication method when an identity provider omits strength or recency metadata, and document that fallback.

**Why:** Missing metadata resolves to the hoped-for value by default, so an upstream that cannot report MFA silently grants access reserved for MFA sessions.

**Detect:** grep `acr`, `amr`, and `auth_time` handling for branches that treat an absent claim as sufficient.

**References:** OWASP ASVS v5.0 V6.8.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x15-V6-Authentication.md, OpenID Connect Core §2
