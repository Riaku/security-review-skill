---
categories: [compliance-privacy]
domains: [frontend]
---

# Informative Consent Prompt

**MUST** show the requested scopes and the verified identity of the requesting application on every consent prompt.

**Why:** A prompt that omits the scope or the client's verified identity gives the user nothing to consent to, so approval becomes a click-through.

**Detect:** render the consent screen and check the scope list and verified app identity are both present.

**References:** OWASP ASVS v5.0 V10.7.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 6819 (OAuth 2.0 threat model)
