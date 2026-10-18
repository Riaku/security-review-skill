# Unvalidated Redirects & Forwards (open redirect in routing/SSO returns)

**MUST NOT** send users to attacker-controlled destinations via unvalidated `redirect`, `next`, or `returnUrl` parameters; validate against an allow-list.

**Why:** Open redirects turn your trusted domain into a phishing launchpad and can leak SSO tokens or authorization codes to external hosts.

**Detect:** grep for `?redirect=`, `next=`, `returnUrl`, `rd=`, `url=` passed to `redirect()`/`Location:` without allow-list checks; Semgrep `open-redirect` rules.

**References:** OWASP Top 10 A01:2021, CWE-601, OWASP Unvalidated Redirects and Forwards Cheat Sheet, OAuth 2.0 redirect_uri validation (RFC 6819)
