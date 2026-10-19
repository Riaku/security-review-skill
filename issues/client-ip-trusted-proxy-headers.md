---
categories: [cloud-network]
domains: [infrastructure]
---

# Client IP From Trusted Hops

**MUST** derive the client address only from proxy headers written by a trusted hop, and treat even that value as weak evidence for rate limiting and logging.

**Why:** A client-supplied forwarding header lets an attacker pick the identity used for throttling and audit, so one host becomes many or many become one.

**Detect:** grep for `X-Forwarded-For` / `X-Real-IP` read straight from the request without a trusted-proxy list (`req.headers['x-forwarded-for']`); missing `trust proxy` / `ForwardedHeaderFilter` config.

**References:** OWASP ASVS v5.0 V15.3.4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md, RFC 7239 (Forwarded header), CWE-348
