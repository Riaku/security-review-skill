---
categories: [authentication]
domains: [backend]
---

# Session invalidation on credential change and logout

**MUST** invalidate all existing sessions and tokens when a user changes their password, email, or MFA settings.

**Why:** If old sessions survive a credential change, an attacker's stolen session stays alive after the victim rotates their password in response to a breach.

**Detect:** grep password/email-change handlers for missing `invalidate_all_sessions`, `revoke_tokens`, or session-store purge; old JWTs still accepted post-change.

**References:** NIST SP 800-63B §5.1.1.2, OWASP A07:2021, CWE-613, RFC 7009
