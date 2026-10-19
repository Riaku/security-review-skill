---
categories: [authentication]
domains: [backend]
---

# OAuth Mix-Up Defense

**MUST** validate the issuer identifier in both the authorization and token responses whenever a client can talk to more than one authorization server.

**Why:** Without per-response attribution, a malicious provider hands the client another provider's code, and the client completes the flow against the wrong authority.

**Detect:** grep the callback and token handlers for `iss` validation; a client configured with several providers that reads only `code` is exposed.

**References:** OWASP ASVS v5.0 V10.2.2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 9207 (iss parameter), CWE-290
