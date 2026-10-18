# Bot Protection

**MUST** rate-limit and challenge automated clients on sensitive endpoints (login, signup, password reset, API).

**Why:** Unprotected endpoints enable credential stuffing, account enumeration, and resource exhaustion attacks at scale.

**Detect:** grep for missing rate limiting, CAPTCHA, or bot detection middleware on auth/API routes; check `rate_limit`, `throttle`, `bot_detection` config absent.

**References:** OWASP A04:2021, CWE-770, OWASP Credential Stuffing Prevention Cheat Sheet
