# caching — full checklist (10 items)

Cache correctness, performance, and eviction.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/caching.md](../categories/caching.md) · Index: [SKILL.md](../SKILL.md)

# Cache-Control Headers

**MUST** set explicit `Cache-Control` on every HTTP response; responses carrying auth tokens, PII, or CSRF values require `no-store`, never a bare default.

**Why:** Missing directives let browsers and proxies cache sensitive pages, exposing them via back-button or shared caches.

**Detect:** Responses lacking `Cache-Control`; `no-store` absent on login, account, admin routes; `public, max-age` on authenticated endpoints.

**References:** OWASP A04:2021, CWE-525, RFC 9111 §5.2.2.5 (no-store)

# Cache Hit Ratio

**SHOULD** monitor cache hit ratio per key namespace and alert when it collapses, since a miss storm pushes every request to the backing store.

**Why:** Sudden miss spikes are both a denial-of-service amplifier and a signal of key-cardinality attacks.

**Detect:** Metrics dashboards missing `cache_hits`/`cache_misses` counters; Redis INFO stats `keyspace_hits` untracked.

**References:** OWASP A05:2021, CWE-400, NIST SP 800-53 SC-5

# Cache Invalidation

**MUST** invalidate every cached entry that holds data changed by a write, privilege change, or credential rotation before the response returns, and for security-relevant keys (permissions, sessions) invalidate by versioned/generation key or tombstone with a bounded TTL, so a reader that loaded the old value cannot repopulate the entry after the invalidation.

**Why:** Stale cached permissions or secrets let revoked users keep acting on old data long after the change.

**Detect:** grep for cache.set without paired cache.delete/evict; keys like `user_perms:`, `session:` missing invalidation hooks.

**References:** OWASP A04:2021, CWE-613, NIST SP 800-53 AC-2

# Cache Warming

**SHOULD** restrict cache-warming jobs to authenticated internal triggers and rate-limit them, never exposing warm endpoints to unauthenticated callers.

**Why:** An open warm endpoint lets attackers stuff the cache with attacker-chosen keys, evicting legitimate entries or poisoning served content.

**Detect:** Routes named `/warm`, `/prefetch`, `cache.warm(` reachable without auth middleware; unbounded key lists in payloads.

**References:** OWASP A01:2021, CWE-420, CWE-770

# CDNs

**MUST NOT** allow CDNs to cache authenticated or per-user responses unless the origin marks them `private` and cache rules exclude them.

**Why:** A CDN caching a personalized response serves one user's data — tokens, PII, balances — to others sharing the URL.

**Detect:** CDN config caching paths like `/account`, `/api/me`; missing `Cache-Control: private` on authenticated responses at edge rules.

**References:** OWASP A01:2021, CWE-525, RFC 9111 section 3.5, Cloudflare cache rules docs

# Cross-Tenant Cache Key Collision

**MUST** include tenant identity in every cache key for tenant-scoped data (cache, CDN, search index, session store).

**Why:** A cache key like `user:1042` without tenant scope serves tenant A's data to tenant B on ID reuse — a silent, high-volume cross-tenant leak.

**Detect:** grep cache set/get calls for keys lacking `tenant`/`org` components; check CDN cache keys and vary headers for tenant-scoped pages; review Redis key naming convention.

**References:** OWASP Multi-Tenant Security Cheat Sheet, CWE-922 Insecure Storage of Sensitive Information

# ETags

**SHOULD NOT** generate ETags from data that leaks across users or tenants, and strong validators must change whenever the underlying resource changes.

**Why:** Weak or shared ETags cause stale conditional responses; content-derived tags can expose other tenants' data via cache reuse.

**Detect:** `ETag` built from user-independent hashes; `If-None-Match` handlers ignoring tenant ID; weak `W/` validators on auth-sensitive resources.

**References:** OWASP A04:2021, RFC 9110 8.8.3

# Explicit eviction policy on every in-memory data store

**MUST** set an explicit memory limit and eviction policy on every in-memory data store, matched to the data it holds; unbounded growth, or a policy that can evict security-critical keys such as sessions and rate-limit counters, is a finding. Redis `maxmemory` left at `0` (unbounded), `maxmemory-policy` left at the default `noeviction` with no write-failure alerting, or `allkeys-lru` on an instance that also holds sessions and rate-limit counters, is the common case.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling. The opposite policy fails the other way: under `noeviction` (the Redis default) nothing is evicted and, once `maxmemory` is reached, every write that would add data is rejected with an OOM error, so sessions and counters cannot be written at all.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `allkeys-*` on an instance whose keyspace mixes caches with sessions or rate-limit counters; `maxmemory` at `0`; `noeviction` with no alerting on `OOM command not allowed when used memory > 'maxmemory'`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs

# TTLs

**MUST NOT** cache authentication tokens, session identifiers, or password hashes with TTLs longer than the underlying credential's validity window.

**Why:** A cached session outliving its real expiry re-admits logged-out or rotated users for the full TTL.

**Detect:** `expires_in`, `ttl`, `EX` arguments on session/token cache writes exceeding session timeout config values.

**References:** OWASP A07:2021, CWE-613, NIST SP 800-63B-4 §5 (session management)

# Write-Through vs Write-Back

**MUST** use write-through persistence for security-relevant records (audit logs, ACLs, tokens); write-back caching is prohibited where a crash must not lose the write.

**Why:** Write-back buffers durable security events in volatile memory, so a crash silently drops audit trails and authorization changes.

**Detect:** Redis `appendonly no`, async flush settings, or deferred DB writes on audit/ACL tables; `write_back`, `async_write` flags.

**References:** OWASP A09:2021, CWE-758, NIST SP 800-53 AU-9, AU-4

