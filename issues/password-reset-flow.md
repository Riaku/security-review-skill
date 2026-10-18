# Password Reset Flow Security

**MUST** issue single-use, high-entropy reset tokens with short expiry (≤15 min) over HTTPS, invalidated on use or password change.

**Why:** Reusable or long-lived reset tokens let an attacker who intercepts one take over an account at leisure, bypassing the password entirely.

**Detect:** grep reset handlers for tokens without `exp`/`used` flags, tokens in URL query strings logged by proxies, `md5(email)` as token, no rate limit on `/forgot-password`.

**References:** OWASP A07:2021, CWE-640, CWE-639, NIST SP 800-63B §5.1.1.2
