---
categories: [authentication]
domains: [backend]
---

# Non-Reassignable Identity

**MUST** identify users by an issuer-and-subject pair that cannot be reassigned, never by email, username, or phone number.

**Why:** Recycled identifiers hand a new holder the previous user's account: the email is reassigned and every grant keyed to it comes along.

**Detect:** grep for user lookup and account linking keyed on `email`, `username`, or `phone` instead of `(iss, sub)` or an immutable internal id.

**References:** OWASP ASVS v5.0 V10.3.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, CWE-287
