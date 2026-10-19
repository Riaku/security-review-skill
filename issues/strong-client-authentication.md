---
categories: [authentication]
domains: [backend]
---

# Strong Client Authentication

**MUST** authenticate confidential clients with proof-of-possession methods such as mutual TLS or signed assertions, not shared client secrets.

**Why:** Shared secrets leak through config, logs, and support tickets, and knowledge alone cannot show that the caller is the client it claims to be.

**Detect:** grep OAuth client config and token requests for `client_secret` where `private_key_jwt` or `tls_client_auth` is available.

**References:** OWASP ASVS v5.0 V10.4.16, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x19-V10-OAuth-and-OIDC.md, RFC 8705 (mTLS client auth)
