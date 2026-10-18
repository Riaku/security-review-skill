# Open Redirect

**SHOULD NOT** Redirect from query params (`next`, `returnTo`) without an allowlist or relative-path restriction.

**Why:** "login?next=evil.com" links land victims on phishing pages via your trusted domain.

**Detect:** `redirect(request.args['next'])`, `location=` from params without allowlist or leading-slash enforcement.

**References:** OWASP A01:2021, CWE-601, OWASP Unvalidated Redirects guide
