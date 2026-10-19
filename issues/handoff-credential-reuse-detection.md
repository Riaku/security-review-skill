---
categories: [authentication]
domains: [backend]
---

# Handoff Credential Reuse Detection

**MUST** reject a second redemption of an already-used authorization code or refresh token and revoke every token issued from that grant.

**Why:** Reuse of a redeemed credential is proof of theft, and quietly returning an error leaves the attacker's stolen tokens alive.

**Detect:** grep for a consumed-code or rotated-refresh store (`used_jti`, `code_consumed`, `refresh_token` family id) and for a revocation cascade on reuse.

**References:** OWASP ASVS v5.0 V10.4.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 6749 §4.1.2
