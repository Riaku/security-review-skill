---
categories: [cloud-network, web-api-security]
domains: [backend, infrastructure]
---

# HTTP Request Smuggling (CL.TE / TE.CL Desync)

**MUST** Front-end and back-end agree on one framing per request: reject requests carrying both `Content-Length` and `Transfer-Encoding`, and disable lenient chunked parsing downstream.

**Why:** When proxy and server disagree on where a request ends, an attacker smuggles a second request inside the first — hijacking someone else's credentials on the shared connection and poisoning caches with attacker-controlled responses.

**Detect:** Test the full proxy chain with the `http-request-smuggler` tool. Grep for proxies forwarding raw `Transfer-Encoding` to frameworks that also honor `Content-Length`; flag hops running different HTTP parser versions, and keepalive between desync-prone tiers.

**Bad:**
```
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked   # front-end trusts TE, back-end trusts CL

0

GET /admin HTTP/1.1         # smuggled request runs on the back-end
```

**Good:**
```nginx
# front-end rejects ambiguous framing before any parser sees it
if ($http_transfer_encoding) { return 400; }
proxy_set_header Transfer-Encoding "";   # normalize, never pass through raw
```

**References:** CWE-444, PortSwigger HTTP desync research, RFC 9112 §6.3 (reject both headers)

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
