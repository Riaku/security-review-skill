---
categories: [authentication]
domains: [backend]
---

# Token Payload Confidentiality

**MUST NOT** put sensitive data or personal identifiers in client-readable token payloads; a signature proves origin, it does not hide content.

**Why:** Tokens are readable by the client and by every system they pass through, and encoded payloads get logged and cached like any other header.

**Detect:** grep token signing call sites for claims carrying `email`, `phone`, `ssn`, `address`, `dob`, `role` lists, or internal identifiers.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html
