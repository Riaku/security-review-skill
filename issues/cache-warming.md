---
categories: [caching]
domains: [reliability]
---

# Cache Warming

**SHOULD** restrict cache-warming jobs to authenticated internal triggers and rate-limit them, never exposing warm endpoints to unauthenticated callers.

**Why:** An open warm endpoint lets attackers stuff the cache with attacker-chosen keys, evicting legitimate entries or poisoning served content.

**Detect:** Routes named `/warm`, `/prefetch`, `cache.warm(` reachable without auth middleware; unbounded key lists in payloads.

**References:** OWASP A01:2021, CWE-420, CWE-770
