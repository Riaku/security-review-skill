# JWT Algorithm Confusion / alg=none / Unverified Signatures

**MUST NOT** accept `alg: none` or allow the token header to select the verification algorithm; pin the expected algorithm server-side.

**Why:** If the verifier trusts the header's `alg`, an attacker switches to `none` or swaps RS256→HS256 to forge unsigned or HMAC-forged tokens.

**Detect:** grep for `jwt.decode` without `algorithms=[...]`, `alg.*none`, dynamic algorithm selection from token header, missing algorithm allowlist.

**References:** CWE-347, OWASP A02:2021, RFC 8725 §3.1, Auth0 JWT Algorithm Confusion advisory

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
