---
categories: [caching]
domains: [reliability]
---

# CDNs

**MUST NOT** allow CDNs to cache authenticated or per-user responses unless the origin marks them `private` and cache rules exclude them.

**Why:** A CDN caching a personalized response serves one user's data — tokens, PII, balances — to others sharing the URL.

**Detect:** CDN config caching paths like `/account`, `/api/me`; missing `Cache-Control: private` on authenticated responses at edge rules.

**References:** OWASP A01:2021, CWE-525, RFC 9111 section 3.5, Cloudflare cache rules docs
