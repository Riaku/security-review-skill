---
categories: [api-design]
domains: [backend]
---

# Server-Sent Events

**SHOULD** set `Cache-Control: no-store` and enforce authentication on SSE endpoints, since EventSource cannot send custom headers.

**Why:** Proxies may cache an event stream containing user data, and token-in-URL patterns leak credentials into logs and referrers.

**Detect:** SSE routes without `Cache-Control`, `text/event-stream` handlers taking `?token=` query params.

**References:** CWE-525, OWASP ASVS V9.1, MDN EventSource security notes
