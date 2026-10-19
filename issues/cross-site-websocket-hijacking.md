---
categories: [api-design, web-api-security, web-client-security]
domains: [backend, frontend]
---

# WebSockets: Upgrade Authentication & Origin Validation (CSWSH)

**MUST** authenticate the upgrade handshake and validate the `Origin` header against an explicit allowlist on every WebSocket connection.

**Why:** WebSockets ignore CORS, so any malicious site can open a socket using the victim's cookies and act as them in real time, streaming private data to the attacker's page.

**Detect:** grep `ws://`, `wss://`, `Upgrade: websocket` upgrade handlers, `onConnection` without origin checks (missing `checkOrigin`/`Origin` validation) or with auth deferred to post-open messages; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, CWE-346, OWASP A01:2021, OWASP API 2023, RFC 6455 section 10.2
