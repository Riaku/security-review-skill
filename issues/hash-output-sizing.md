---
categories: [secrets-crypto]
domains: [backend]
---

# Hash Output Sizing

**MUST** use the full digest wherever collision resistance is relied on, and document the property that justifies any truncation.

**Why:** The two properties cost differently, so sizing by habit either trusts a short digest where collisions matter or pays for resistance nobody needs.

**Detect:** grep for `sha1`, `md5`, and truncated digests (`digest()[:16]`, `substr($hash, 0, 16)`) in integrity or identifier code.

**References:** OWASP ASVS v5.0 V11.4.3, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, NIST SP 800-107
