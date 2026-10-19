---
categories: [authentication]
domains: [backend]
---

# Per-Client Protocol Surface

**MUST** allow each client only the grant types, response types, response modes, and scopes it actually needs, validated at the authorization server.

**Why:** Client-chosen protocol parameters on a permissive endpoint are the raw material of downgrade and confusion attacks; removing the choice removes the class.

**Detect:** grep client registrations for `grant_types`, `response_types`, `response_modes`, and wildcard `scopes`.

**References:** OWASP ASVS v5.0 V10.4.11, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9700 (OAuth 2.0 Security BCP)
