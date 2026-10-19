---
categories: [cloud-network]
domains: [backend, infrastructure]
---

# Trusted Proxy Headers

**MUST** accept client-IP, scheme, and host headers only from a known edge that overwrites them, and treat them as attacker-controlled everywhere else.

**Why:** Anything upstream or direct can set those headers, so rate limits, audit trails, and HTTPS redirects keyed on them are bypassable.

**Detect:** grep for `X-Forwarded-For`, `X-Real-IP`, `X-Forwarded-Proto` reads with no check that the immediate peer is a trusted proxy.

**References:** RFC 9110 HTTP Semantics, https://httpwg.org/specs/rfc9110.html
