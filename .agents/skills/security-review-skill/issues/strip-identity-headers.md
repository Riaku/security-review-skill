---
categories: [cloud-network]
domains: [infrastructure]
---

# Strip Identity Headers

**MUST** strip client-supplied identity headers at the edge and set them only from the authenticated session.

**Why:** An upstream that trusts an inbound `X-User-ID` or forwarding header hands any client the ability to name itself administrator.

**Detect:** grep ingress and proxy config for inbound `X-User-Id`, `X-Authenticated-User`, and `X-Remote-User` passed through, and for services that read them without a session check.

**References:** OWASP ASVS v5.0 V4, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x13-V4-API-and-Web-Service.md, RFC 7239 (Forwarded header)
