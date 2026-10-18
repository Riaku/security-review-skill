---
categories: [api-design]
domains: [backend]
---

# WebSockets

**MUST** authenticate the upgrade handshake and validate the Origin header on every WebSocket connection.

**Why:** Cross-site WebSocket hijacking lets a victim's browser open an authenticated socket to your API, streaming private data to an attacker's page.

**Detect:** `Upgrade: websocket` handlers missing `checkOrigin`/`Origin` validation; auth deferred to post-open messages.

**References:** OWASP API 2023, CWE-346, RFC 6455 §10.2
