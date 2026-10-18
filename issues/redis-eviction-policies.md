---
categories: [caching]
domains: [reliability]
---

# Explicit eviction policy on every in-memory data store

**MUST** set an explicit memory limit and eviction policy on every in-memory data store, matched to the data it holds; unbounded growth, or a policy that can evict security-critical keys such as sessions and rate-limit counters, is a finding. Redis `maxmemory` left unbounded or `maxmemory-policy` at `noeviction`, or `allkeys-lru` on a mixed-purpose instance, is the common case.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `noeviction`; sessions and caches sharing one instance with `allkeys-*`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs
