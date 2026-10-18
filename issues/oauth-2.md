---
categories: [authentication]
domains: [backend]
---

# OAuth 2.0

**MUST** validate the `state` parameter on every authorization callback and use PKCE for public clients.

**Why:** Missing state/PKCE enables CSRF and authorization-code interception, letting an attacker bind a victim's code to their own session.

**Detect:** grep callback handlers for absent `state` checks, `response_type=token` in public clients, missing `code_verifier`/`code_challenge` in auth URL construction.

**References:** OWASP A01:2021, CWE-352, RFC 6749 §10.12, OAuth Security BCP §7
