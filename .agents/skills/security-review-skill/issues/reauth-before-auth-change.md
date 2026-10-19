---
categories: [authentication]
domains: [backend]
---

# Reauth Before Auth Change

**MUST** require full re-authentication before changing the email, phone, MFA enrolment, or recovery settings on an account.

**Why:** Those attributes are the account's recovery keys, so a hijacked session that can edit them converts temporary access into permanent ownership.

**Detect:** grep account-update handlers for those fields and check for a password or step-up check on the same path.

**References:** OWASP ASVS v5.0 V7, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x16-V7-Session-Management.md, CWE-620
