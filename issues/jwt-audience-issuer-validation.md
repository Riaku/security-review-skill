---
categories: [authentication]
domains: [backend]
---

# JWT Audience/Issuer Validation & kid/JWKS Abuse

**MUST** verify `iss` and `aud` claims against an explicit allowlist and pin `kid` to a trusted JWKS entry before accepting a token.

**Why:** Unpinned `kid` lets an attacker point the verifier at a rogue JWKS or reuse a token minted for a different service as valid here.

**Detect:** grep verifier config for missing `issuer`/`audience` checks, `jwks_uri` fetched without TLS pinning, `kid` resolved dynamically with no allowlist.

**References:** RFC 8725 §3.8-3.9, CWE-345, OWASP A02:2021, OIDC Core §3.1.3.7
