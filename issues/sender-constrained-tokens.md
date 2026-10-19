---
categories: [authentication]
domains: [backend]
---

# Sender-Constrained Tokens

**SHOULD** bind access tokens to the client that requested them, using proof-of-possession or mTLS, wherever bearer theft is in scope.

**Why:** A pure bearer token is usable by anyone who copies it, from anywhere, for its whole lifetime.

**Detect:** grep token issuance and client config for `DPoP`, `cnf` claim, or mTLS binding; flag tokens stored in `localStorage` or `sessionStorage`.

**References:** OWASP OAuth 2.0 Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
