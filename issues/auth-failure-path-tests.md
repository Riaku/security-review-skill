---
categories: [authentication, testing-strategy]
domains: [backend]
---

# Auth Failure-Path Tests

**MUST** test each auth flow's failure paths as well as its success path: lockout on repeated wrong passwords, reset for an unknown address, a replayed verification link, and signup with an existing address.

**Why:** These are the paths where auth fails open — a reset that mints a token for an address that does not exist, a verification link that still works on the second click, a lockout counter that never increments — and no happy-path test can see any of them.

**Detect:** grep the auth test files for the negative cases (a repeated bad-password login, an `unknown`/`nonexistent` address reset, a second submit of a verification or reset token, a duplicate-address signup); a suite that exercises auth flows only through the success path is the finding.

**References:** OWASP WSTG Authentication Testing, https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/03-Identity_Management_Testing/, NIST SP 800-63B-4 §3.2.2, https://csrc.nist.gov/pubs/sp/800/63/b/4/final, CWE-287
