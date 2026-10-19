---
categories: [cloud-network, web-api-security]
domains: [backend, infrastructure]
---

# No Plaintext API Endpoints

**MUST** refuse plaintext HTTP on API endpoints rather than redirect it, and scope any unavoidable cleartext exception to named hosts.

**Why:** A redirect still exposes the first request - headers, tokens, payload - to anyone on the path. Clients that follow redirects then resend credentials to the redirect target.

**Detect:** Listeners on port 80 that only `return 301`, plain `http://` upstreams, and `usesCleartextTraffic`/`cleartextTrafficPermitted="true"` without a per-domain exception.

**References:** Mozilla Web Security Guidelines, https://infosec.mozilla.org/guidelines/web_security, OWASP ASVS Communications chapter
