# OpenID Connect

**MUST** validate the ID token's signature, `iss`, `aud`, and `nonce` before trusting any identity claim.

**Why:** Skipping ID token validation lets an attacker replay a token from another client or provider and be accepted as a different user.

**Detect:** grep for `id_token` usage without `verify`/`validate` calls, missing `nonce` in auth request, `aud` not checked against client ID.

**References:** OIDC Core §3.1.3.7, CWE-347, OWASP A02:2021, NIST SP 800-63B

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
