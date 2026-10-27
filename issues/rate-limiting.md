---
categories: [web-api-security]
domains: [backend]
---

# Rate Limiting / Throttling

**SHOULD** Throttle auth, reset, and expensive endpoints per identity and IP, returning 429 with `Retry-After`.

**Why:** Unlimited endpoints enable credential stuffing, brute force, and cost amplification.

**Detect:** Login/reset routes with no `ratelimit`, `throttle`, `limit=` decorator or gateway policy.

**References:** OWASP API4:2023 Unrestricted Resource Consumption, OWASP A04:2021, CWE-770, OWASP Rate Limiting Cheat Sheet, NIST SP 800-63B
