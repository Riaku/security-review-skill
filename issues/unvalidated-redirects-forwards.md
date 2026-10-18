# Unvalidated Redirects & Forwards (open redirect in routing/SSO returns)

**MUST NOT** route users via unvalidated `redirect`/`returnUrl` parameters; destinations must pass an allow-list check.

**Why:** Open redirects turn your trusted domain into a phishing launchpad and can leak SSO tokens or OAuth codes externally.

**Detect:** grep `?redirect=`, `next=`, `returnUrl`, `rd=` reaching `redirect()` or `Location:` without allow-list validation.

**References:** OWASP Top 10 A01:2021, CWE-601, OWASP Redirects Cheat Sheet, RFC 6819
