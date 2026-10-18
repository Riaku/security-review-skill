# caching — full checklist (10 items)

Cache correctness, performance, and eviction.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [caching](../categories/caching.md) · index: [SKILL.md](../SKILL.md)

# Cache-Control Headers

**MUST** set explicit `Cache-Control` on every HTTP response; responses carrying auth tokens, PII, or CSRF values require `no-store`, never a bare default.

**Why:** Missing directives let browsers and proxies cache sensitive pages, exposing them via back-button or shared caches.

**Detect:** Responses lacking `Cache-Control`; `no-store` absent on login, account, admin routes; `public, max-age` on authenticated endpoints.

**References:** OWASP A04:2021, CWE-525, RFC 7234, NIST SP 800-63B 2.4.1.1

---

**Part of:** [caching](../categories/caching.md) · [web-client-security](../categories/web-client-security.md) · [frontend](../domains/frontend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Cache Hit Ratio

**SHOULD** monitor cache hit ratio per key namespace and alert when it collapses, since a miss storm pushes every request to the backing store.

**Why:** Sudden miss spikes are both a denial-of-service amplifier and a signal of key-cardinality attacks.

**Detect:** Metrics dashboards missing `cache_hits`/`cache_misses` counters; Redis INFO stats `keyspace_hits` untracked.

**References:** OWASP A05:2021, CWE-400, NIST SP 800-53 SC-5

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Cache Invalidation

**MUST** invalidate every cached entry that holds data changed by a write, privilege change, or credential rotation before the response returns.

**Why:** Stale cached permissions or secrets let revoked users keep acting on old data long after the change.

**Detect:** grep for cache.set without paired cache.delete/evict; keys like `user_perms:`, `session:` missing invalidation hooks.

**References:** OWASP A04:2021, CWE-613, CWE-364, NIST SP 800-53 AC-2

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Cache Warming

**SHOULD** restrict cache-warming jobs to authenticated internal triggers and rate-limit them, never exposing warm endpoints to unauthenticated callers.

**Why:** An open warm endpoint lets attackers stuff the cache with attacker-chosen keys, evicting legitimate entries or poisoning served content.

**Detect:** Routes named `/warm`, `/prefetch`, `cache.warm(` reachable without auth middleware; unbounded key lists in payloads.

**References:** OWASP A01:2021, CWE-420, CWE-770

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# CDNs

**MUST NOT** allow CDNs to cache authenticated or per-user responses unless the origin marks them `private` and cache rules exclude them.

**Why:** A CDN caching a personalized response serves one user's data — tokens, PII, balances — to others sharing the URL.

**Detect:** CDN config caching paths like `/account`, `/api/me`; missing `Cache-Control: private` on authenticated responses at edge rules.

**References:** OWASP A01:2021, CWE-525, RFC 7234 section 3.2, Cloudflare cache rules docs

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Cross-Tenant Cache Key Collision

**MUST** include tenant identity in every cache key for tenant-scoped data (cache, CDN, search index, session store).

**Why:** A cache key like `user:1042` without tenant scope serves tenant A's data to tenant B on ID reuse — a silent, high-volume cross-tenant leak.

**Detect:** grep cache set/get calls for keys lacking `tenant`/`org` components; check CDN cache keys and vary headers for tenant-scoped pages; review Redis key naming convention.

**References:** OWASP Multi-Tenant Security Guidance, CWE-922 insecure storage

---

**Part of:** [caching](../categories/caching.md) · [multi-tenancy](../categories/multi-tenancy.md) · [backend](../domains/backend.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# ETags

**SHOULD NOT** generate ETags from data that leaks across users or tenants, and strong validators must change whenever the underlying resource changes.

**Why:** Weak or shared ETags cause stale conditional responses; content-derived tags can expose other tenants' data via cache reuse.

**Detect:** `ETag` built from user-independent hashes; `If-None-Match` handlers ignoring tenant ID; weak `W/` validators on auth-sensitive resources.

**References:** OWASP A04:2021, CWE-916, RFC 7232 section 2.3, RFC 9110 8.8.3

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Redis Eviction Policies

**MUST** set an explicit `maxmemory-policy` per Redis instance; default noeviction with unbounded growth, or allkeys-lru on a mixed-purpose instance, is a finding.

**Why:** Unchecked eviction can drop session or rate-limit keys under memory pressure, silently disabling auth throttling.

**Detect:** `redis-cli CONFIG GET maxmemory-policy` returning `noeviction`; sessions and caches sharing one instance with `allkeys-*`.

**References:** OWASP A05:2021, CWE-770, CWE-400, Redis maxmemory docs

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# TTLs

**MUST NOT** cache authentication tokens, session identifiers, or password hashes with TTLs longer than the underlying credential's validity window.

**Why:** A cached session outliving its real expiry re-admits logged-out or rotated users for the full TTL.

**Detect:** `expires_in`, `ttl`, `EX` arguments on session/token cache writes exceeding session timeout config values.

**References:** OWASP A07:2021, CWE-613, NIST SP 800-63B 5.1.1

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Write-Through vs Write-Back

**MUST** use write-through persistence for security-relevant records (audit logs, ACLs, tokens); write-back caching is prohibited where a crash must not lose the write.

**Why:** Write-back buffers durable security events in volatile memory, so a crash silently drops audit trails and authorization changes.

**Detect:** Redis `appendonly no`, async flush settings, or deferred DB writes on audit/ACL tables; `write_back`, `async_write` flags.

**References:** OWASP A09:2021, CWE-758, NIST SP 800-53 AU-9, AU-4

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

