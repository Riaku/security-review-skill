---
categories: [authentication]
domains: [backend]
---

# Token Type Verification

**MUST** verify a token's declared type and required event claims before acting on it, including logout and error tokens.

**Why:** Without a type check any signed token is accepted anywhere, so a re-purposed identity token becomes a logout trigger or a session mint.

**Detect:** grep for `typ` and `events` claim validation in token consumers; a logout endpoint that accepts any well-signed JWT is the finding.

**References:** OWASP ASVS v5.0 V10.5.5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 8417 (Security Event Tokens), CWE-290
