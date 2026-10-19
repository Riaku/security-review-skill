---
categories: [authentication]
domains: [backend]
---

# Retire Legacy OAuth Grants

**MUST** disable the implicit and resource-owner-password grants at the authorization server for every client, not only in individual client configuration.

**Why:** A per-client opt-out rots: any client added later inherits the dangerous flow because the capability still exists at the authority.

**Detect:** grep authorization-server config for `response_type=token`, `grant_types: [password]`, `allow_implicit`, `enable_ropc`.

**References:** OWASP ASVS v5.0 V10.4.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9700 (OAuth 2.0 Security BCP)
