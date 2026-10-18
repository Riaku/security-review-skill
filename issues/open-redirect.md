# Open Redirect

**SHOULD NOT** Redirect from query params (`next`, `returnTo`) without an allowlist or relative-path restriction.

**Why:** "login?next=evil.com" links land victims on phishing pages via your trusted domain, and open redirects can also leak SSO tokens or OAuth codes to external destinations.

**Detect:** `redirect(request.args['next'])`, `location=` from params without allowlist or leading-slash enforcement; grep `?redirect=`, `next=`, `returnUrl`, `rd=` reaching `redirect()` or `Location:` headers.

**References:** OWASP A01:2021, CWE-601, OWASP Unvalidated Redirects guide, RFC 6819

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
