# caching

Cache correctness, performance, and eviction.

## What this category covers

This category covers caches between a client and the system of record: what they store, for how long, under which key, and how a stale or evicted entry changes behavior. Member items span HTTP cache semantics and CDN rules, cache keys and tenant scoping, TTLs relative to credential lifetime, invalidation on writes and privilege changes, eviction policy on in-memory stores, and the durability choice between write-through and write-back. They also cover the operational edges — hit ratio, warming endpoints, and ETag generation. A reviewer should expect findings about data served to the wrong caller, data that outlives its authority, or a miss pattern that collapses the backing store.

- HTTP and edge caching: cache directives, CDN rules, and exclusion of authenticated responses.
- Key design: tenant and user scoping, plus ETag derivation.
- Lifetime: TTLs against credential validity and invalidation on write or privilege change.
- Store behavior: eviction policy, memory limits, warming endpoints, and write-through versus write-back.
- Operating signals: hit ratio and miss storms.

## What it does not cover

- [database](../categories/database.md) — durable storage, indexing, and query correctness belong there.
- [multi-tenancy](../categories/multi-tenancy.md) — tenant isolation across the whole stack belongs there; this category covers only cache-key scoping.
- [web-client-security](../categories/web-client-security.md) — browser storage and cookie handling belong there.

## What a finding here looks like

- A cache key omits the tenant id, so a reused user id serves one tenant's entry to another.
- A CDN or shared proxy caches an authenticated response and serves it to a different user.
- A cached session or permission outlives the credential it represents, so a revoked user is still admitted.
- An in-memory store has no memory limit or eviction policy, or its policy can evict session and rate-limit keys under pressure.
- A write succeeds but its cached entry is not invalidated before the response returns, and a reader repopulates the stale value.
