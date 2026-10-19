---
categories: [authentication]
domains: [backend]
---

# Token Replay Prevention

**MUST** give every single-use token a unique identifier and reject a second presentation of an identifier already consumed.

**Why:** Without a unique identifier a token replays indefinitely inside its validity window, and revocation cannot tell the stolen copy from the original. A reuse cache is what makes single use enforceable.

**Detect:** grep issuance of reset, verification, invitation and refresh tokens for a `jti`/nonce claim plus a store that records consumed identifiers; absence of either, or a record that is written after the action instead of atomically with it, is the finding.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html, RFC 7519 §4.1.7 (jti)
