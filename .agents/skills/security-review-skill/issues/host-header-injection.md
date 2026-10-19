---
categories: [web-api-security]
domains: [backend]
---

# Host Header Injection

**MUST** build URLs, cache keys, and routing decisions from the Host header only after validating it against an allow-list.

**Why:** Password-reset links, canonical URLs, and cache entries inherit whatever host the attacker sent, redirecting victims or poisoning shared caches.

**Detect:** grep for `request.host`, `get_host()`, `X-Forwarded-Host`, and URL builders outside the configured base-URL constant.

**References:** OWASP WSTG checklist, https://github.com/OWASP/wstg/blob/master/checklists/checklist.md
