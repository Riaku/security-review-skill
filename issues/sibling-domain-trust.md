---
categories: [web-client-security]
domains: [frontend]
---

# Sibling Domain Distrust

**MUST** treat every sibling subdomain as potentially hostile: no parent-domain cookies, wildcard CORS, or postMessage trust that assumes the domain family is one zone.

**Why:** An attacker who takes over or registers any sibling domain inherits the trust that cookies, CORS rules, and CSP allowances extend to the whole family.

**Detect:** grep for `Domain=.example.com` cookies, `Access-Control-Allow-Origin` wildcard-subdomain regex, `document.domain`, and `postMessage` targets on `*.example.com`.

**References:** Related-domain attacker framework, https://arxiv.org/abs/2012.01946
