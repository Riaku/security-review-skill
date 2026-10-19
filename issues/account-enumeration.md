---
categories: [authentication]
domains: [backend]
---

# Account Enumeration

**SHOULD NOT** reveal whether an account exists through differing responses, timing, or error messages on login, registration, and password-reset endpoints.

**Why:** Distinct "user not found" vs "wrong password" responses let attackers build a valid username list for targeted phishing or credential stuffing.

**Detect:** grep for `user not found`, `email already exists`, `invalid username` strings; differing HTTP status codes (404 vs 401) on auth endpoints.

**References:** OWASP A07:2021, CWE-204, CWE-203, NIST SP 800-63B-4 §3.2.2
