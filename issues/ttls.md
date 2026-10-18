# TTLs

**MUST NOT** cache authentication tokens, session identifiers, or password hashes with TTLs longer than the underlying credential's validity window.

**Why:** A cached session outliving its real expiry re-admits logged-out or rotated users for the full TTL.

**Detect:** `expires_in`, `ttl`, `EX` arguments on session/token cache writes exceeding session timeout config values.

**References:** OWASP A07:2021, CWE-613, NIST SP 800-63B 5.1.1

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
