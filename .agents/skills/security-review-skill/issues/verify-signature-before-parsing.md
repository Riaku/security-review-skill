---
categories: [authentication]
domains: [backend]
---

# Verify Signature Before Parsing

**MUST** verify the signature or MAC over a token or message before parsing its contents or making any decision from them.

**Why:** Parsing first runs attacker-chosen bytes through a parser with elevated trust and leaks oracle behaviour for tokens that will be rejected anyway.

**Detect:** grep decode-then-verify order: `jwt.decode(..., verify=False)`, `verify_signature: false`, claims read before `verify(`/`hmac.compare_digest`, and `json.loads` on a webhook body before its HMAC check.

**References:** OWASP JSON Web Token Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html, Critical vulnerabilities in JSON Web Token libraries, https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/
