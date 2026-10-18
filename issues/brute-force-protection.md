---
categories: [authentication]
domains: [backend]
---

# Brute Force Protection

**MUST** rate-limit and lock out repeated failed authentication attempts per account and per source IP.

**Why:** Without throttling, automated credential-stuffing and dictionary attacks can try millions of passwords against a login form unimpeded.

**Detect:** grep login endpoints for missing `rate_limit`, `attempt_count`, `lockout` logic; no backoff on 401 responses; unlimited POST to `/login`.

**References:** OWASP A07:2021, CWE-307, NIST SP 800-63B §5.2.2, CIS Control 6.2

---

**Part of:** [authentication](../categories/authentication.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
