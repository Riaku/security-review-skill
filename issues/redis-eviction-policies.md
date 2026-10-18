# Redis Eviction Policies

**MUST** set an explicit `maxmemory-policy` per Redis instance; default noeviction with unbounded growth, or allkeys-lru on a mixed-purpose instance, is a finding.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `noeviction`; sessions and caches sharing one instance with `allkeys-*`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs
