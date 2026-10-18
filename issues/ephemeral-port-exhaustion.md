---
categories: [cloud-network]
domains: [infrastructure]
---

# Ephemeral port / TIME_WAIT exhaustion on busy clients

**SHOULD** pool and reuse outbound connections on high-fan-out clients so the ephemeral port range and TIME_WAIT backlog never become the bottleneck.

**Why:** Every unclosed TCP connection from a client burns a local port for 60 seconds in TIME_WAIT; a chatty service opening a fresh socket per request can exhaust the ~28k available ports and fail with `EADDRNOTAVAIL` — a self-inflicted outage triggered by success, not attack.

**Detect:** Watch `ss -s` / `netstat -an | grep TIME_WAIT | wc -l` against `net.ipv4.ip_local_port_range`; grep code for HTTP clients constructed per request (`requests.get(...)` without a session, `new HttpClient()` inside loops) instead of shared pooled clients. Check keep-alive settings, pool max-size, and whether the platform's port range is unusually narrow.

**Bad:**
```python
for url in urls:
    requests.get(url)          # fresh socket + TIME_WAIT each time
```

**Good:**
```python
s = requests.Session()         # one pooled, keep-alive client
adapter = HTTPAdapter(pool_maxsize=100)
s.mount("https://", adapter)
for url in urls:
    s.get(url)
```

**References:** RFC 9293 (TIME-WAIT), Cloudflare "Why your server runs out of ports", nginx/HAProxy connection pooling docs
