# Secret Validity Checking (verify leaked keys are live)

**SHOULD** validate whether a reported leaked credential is still active before closing the finding, and confirm revocation actually took effect at the provider.

**Why:** Treating every leak report as stale lets live keys keep working; conversely, assuming revocation worked without verification leaves access open.

**Detect:** No post-rotation validation step, `git leak` findings closed without provider-side revoke check, missing `aws sts get-caller-identity` / GitHub `/rate_limit` verification.

**References:** OWASP ASVS V2.10.4, GitHub secret scanning docs, AWS IAM key revocation runbooks
