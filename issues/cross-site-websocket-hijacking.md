---
categories: [web-api-security, web-client-security]
domains: [backend, frontend]
---

# Cross-Site WebSocket Hijacking (CSWSH)

**MUST** validate the `Origin` header on the WebSocket upgrade handshake against an explicit allowlist.

**Why:** WebSockets ignore CORS; any malicious site can open a socket using the victim's cookies and act as them in real time.

**Detect:** grep `ws://`, `wss://`, `upgrade` handlers, `onConnection` without origin checks; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, OWASP A01:2021, RFC 6455 section 10.2
