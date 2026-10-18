---
categories: [authentication, web-api-security]
domains: [backend]
---

# Account recovery and password-reset flow security (tokens, helpdesk takeover)

**MUST NOT** allow helpdesk or support staff to reset a user's password without a verified second channel (e.g. confirmed email + MFA challenge) and full audit logging.

**Why:** Social-engineering the helpdesk is the cheapest path to takeover; a single unverified reset request bypasses every other control.

**Detect:** grep support/reset tooling for missing identity-verification step, no `audit_log` on manual resets, reset-by-username-only admin endpoints without MFA gate.

**References:** NIST SP 800-63B §5.1.1.2, CWE-287, OWASP A07:2021, CWE-354
