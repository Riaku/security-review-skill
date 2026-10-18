# Redis Eviction Policies

**MUST** set an explicit `maxmemory` cap and `maxmemory-policy` on every Redis instance, matched to the data it holds: an eviction policy (`allkeys-lru`, `volatile-ttl`) for cache data that can be recomputed, and `noeviction` with memory-pressure alerting for session, token, or rate-limit data that must never be silently dropped.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `noeviction`; sessions and caches sharing one instance with `allkeys-*`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs