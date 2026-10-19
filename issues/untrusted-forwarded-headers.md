---
categories: [web-api-security]
domains: [backend]
---

# Untrusted Forwarded Headers

**MUST NOT** make security decisions from `X-Forwarded-For`, `Referer`, `User-Agent`, or client timestamps without validating the trusted proxy chain.

**Why:** Every one of those headers is client-writable, so an IP allowlist, CSRF check, or rate limit keyed on them is keyed on attacker input.

**Detect:** grep `X-Forwarded-For`, `X-Real-IP`, `Referer`, and `User-Agent` reads that feed allowlists, rate-limit keys, or audit fields; check the proxy config for trusted-proxy depth.

**References:** OWASP HTTP Headers Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
