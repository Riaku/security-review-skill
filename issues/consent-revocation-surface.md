---
categories: [authentication, compliance-privacy]
domains: [backend]
---

# Consent Revocation Surface

**MUST** give users a self-service view of granted authorizations and active tokens, with the ability to revoke each one.

**Why:** Consent without a revocation path accumulates invisible standing privilege that outlives the user's intent and the client's trustworthiness.

**Detect:** locate the connected-applications and active-sessions screens and check each grant can be revoked individually.

**References:** OWASP ASVS v5.0 V10.4.9, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md
