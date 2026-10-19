---
categories: [cloud-network, web-api-security]
domains: [backend]
---

# Outbound Fetch Policy

**MUST** re-apply the outbound destination policy on every redirect and retry, not only to the initial request URL.

**Why:** An allowlist checked once is defeated by a 302 to an internal address or a retry that resolves a new host; only per-hop enforcement covers the whole chain.

**Detect:** grep HTTP client construction for `follow_redirects=True` with no re-validation hook, and for retry policies that re-resolve the original hostname; a policy check performed once before the first request is the finding.

**References:** OWASP SSRF Prevention Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html, CWE-918 Server-Side Request Forgery
