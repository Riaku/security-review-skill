---
categories: [web-api-security]
domains: [backend]
---

# SSRF

**MUST** Restrict user-supplied URLs to an allowlist of hosts/schemes, blocking internal ranges after DNS resolution.

**Why:** Crafted URLs reach internal services and cloud metadata endpoints to steal credentials.

**Detect:** `requests.get(user_url)`, `urlopen`, `fetch(` on request-derived URLs without IP-blocklist checks.

**References:** OWASP A10:2021, CWE-918, SSRF-Defense list

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
