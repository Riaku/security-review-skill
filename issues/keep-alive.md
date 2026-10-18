---
categories: [api-design]
domains: [backend]
---

# Keep-Alive

**SHOULD** cap keep-alive idle timeouts and max requests per connection to bound resource hold per client.

**Why:** Unlimited persistent connections let a few clients exhaust the server's file descriptors, enabling slow-drain denial of service.

**Detect:** `keepalive_timeout 0`, absent `keepalive_requests`, nginx `worker_connections` vs unbounded upstream pools.

**References:** CWE-400, OWASP ASVS V5.1, nginx keepalive directive docs
