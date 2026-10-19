---
categories: [web-client-security]
domains: [frontend]
---

# Fresh CSP Nonce Per Response

**MUST** generate a fresh CSP nonce for every response and verify no cache layer serves a nonce minted for another request.

**Why:** A reused nonce becomes a static allowlist token, so an attacker who sees one value can inject script the policy admits.

**Detect:** command `curl -sI` the same page repeatedly through the CDN and diff the `content-security-policy` nonce; grep cache config for how CSP is cached or shared.

**References:** CSP nonce reuse measurement, https://arxiv.org/abs/2309.07782
