# JWT Expiry

**MUST** set short-lived access tokens (15 minutes or less) with an explicit `exp` claim that the verifier rejects when past.

**Why:** A stolen or leaked long-lived JWT stays usable indefinitely, giving an attacker persistent API access with no way to expire out.

**Detect:** grep for `expiresIn`, `exp:` with values like `86400`, `7d`, `never`; missing `exp` claim in token payloads or verifier code.

**References:** OWASP A02:2021, CWE-613, RFC 7519 §4.1.4, NIST SP 800-107

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
