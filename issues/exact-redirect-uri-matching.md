---
categories: [authentication]
domains: [backend]
---

# Exact Redirect URI Matching

**MUST** compare OAuth redirect URIs against a registered exact-match allowlist, rejecting wildcards, prefix matches, and unregistered ports or paths.

**Why:** Loose matching lets an attacker craft a URI that begins with the trusted value and receives the authorization code. One accepted prefix is a full account-takeover primitive.

**Detect:** grep OAuth client config and callback handlers for `redirect_uri` compared with `startsWith`, `contains`, a regex, or a wildcard entry; the comparison must be exact equality against a registered value.

**References:** OWASP OAuth 2.0 Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html, RFC 9700 OAuth 2.0 Security Best Current Practice, https://www.rfc-editor.org/rfc/rfc9700.txt
