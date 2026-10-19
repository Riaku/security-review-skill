---
categories: [authentication]
domains: [backend]
---

# Discovery Metadata Binding

**MUST** verify that discovered configuration metadata declares exactly the identifier used to fetch it, and that its TLS identity covers that identifier.

**Why:** Without the binding, an attacker publishes metadata for someone else's identifier and the client trusts the attacker's issuer, scopes, or endpoints.

**Detect:** grep `/.well-known/` metadata fetch code for an exact-match comparison of the returned identifier against the request identifier.

**References:** RFC 9728 OAuth Protected Resource Metadata, https://www.rfc-editor.org/rfc/rfc9728.html, RFC 8414 Authorization Server Metadata, https://www.rfc-editor.org/rfc/rfc8414.html
