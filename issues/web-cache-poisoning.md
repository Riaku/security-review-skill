---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# Web Cache Poisoning & Cache Deception

**SHOULD NOT** cache responses that vary on unkeyed inputs like headers, query params, or cookies without declaring `Vary` or normalizing them.

**Why:** An attacker can get a poisoned response stored in CDN/proxy cache and served to every subsequent visitor of that URL.

**Detect:** grep `Vary:`, `cache-control: public`, unkeyed `X-Forwarded-*`/`Accept-Encoding` handling; CDN cache-key config ignoring query params.

**References:** PortSwigger Web Cache Poisoning research, OWASP A04:2021

---

**Part of:** [web-api-security](../categories/web-api-security.md) · [web-client-security](../categories/web-client-security.md) · [backend](../domains/backend.md) · [frontend](../domains/frontend.md) · [SKILL.md](../SKILL.md)
