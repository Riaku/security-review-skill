# Insufficient Randomness for Tokens and IDs

**MUST** generate session tokens, password resets, API keys, and invite codes from a cryptographically secure RNG (`secrets`, `crypto.randomBytes`, `SecureRandom`), never `random`/`Math.random`/sequential IDs.

**Why:** Predictable randomness lets attackers guess reset links and session tokens, taking over accounts without ever touching the password.

**Detect:** `Math.random()`, Python `random.` for tokens, `uuid1`/sequential IDs in auth flows, `rand()` in token generation code.

**References:** OWASP ASVS V3.2.2, CWE-330, NIST SP 800-90A

---

**Part of:** [authentication](../categories/authentication.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
