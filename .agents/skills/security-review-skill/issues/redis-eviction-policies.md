---
categories: [caching]
domains: [reliability]
---

# Explicit eviction policy on every in-memory data store

**MUST** set an explicit memory limit and eviction policy on every in-memory data store, matched to the data it holds; unbounded growth, or a policy that can evict security-critical keys such as sessions and rate-limit counters, is a finding. Redis `maxmemory` left at `0` (unbounded), `maxmemory-policy` left at the default `noeviction` with no write-failure alerting, or `allkeys-lru` on an instance that also holds sessions and rate-limit counters, is the common case.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling. The opposite policy fails the other way: under `noeviction` (the Redis default) nothing is evicted and, once `maxmemory` is reached, every write that would add data is rejected with an OOM error, so sessions and counters cannot be written at all.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `allkeys-*` on an instance whose keyspace mixes caches with sessions or rate-limit counters; `maxmemory` at `0`; `noeviction` with no alerting on `OOM command not allowed when used memory > 'maxmemory'`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs
