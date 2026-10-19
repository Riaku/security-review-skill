# multi-tenancy

Tenant isolation across API, data, cache, queues, and lifecycle.

## What this category covers

This category covers the isolation guarantees that keep one tenant's activity from touching another's, and the honest accounting when a tenant leaves. The items span tenant identity at the API boundary (derived from the authenticated session, never from a client-supplied identifier), the data layer (database-enforced row-level security for tenant-scoped tables), and shared infrastructure (cache keys that carry tenant identity, queue separation so one tenant's burst or poison message cannot starve others, and per-tenant resource quotas against noisy neighbors). Lifecycle is the closing edge: a departing tenant's data must be purged from primary stores, replicas, caches, search index, analytics, and third-party processors with evidence. It is a small, deliberately cross-cutting category — seven items — because the same tenant identity has to hold from the request, through every cache and queue, down to the row, and out again at offboarding. Expect findings where an isolation boundary is enforced in one layer and assumed absent in another.

- Tenant identity at the API boundary: derived from the authenticated session, never from a query parameter, header, or request body.
- Data-layer isolation: database-enforced row-level security for every tenant-scoped table.
- Shared cache isolation: tenant identity in every cache, CDN, search-index, and session-store key.
- Shared queue and compute isolation: per-tenant separation, per-tenant quotas, and noisy-neighbor limits.
- Lifecycle: verified tenant purge across primary stores, replicas, caches, search index, analytics, and processors.

## What it does not cover

- [authorization-access-control](../categories/authorization-access-control.md) — general role and policy models belong there, beyond the tenant dimension.
- [caching](../categories/caching.md) — general cache design and invalidation belong there, including non-tenant-scoped data.
- [containers-k8s](../categories/containers-k8s.md) — cluster resource governance and namespace configuration belong there beyond tenant quotas.
- [compliance-privacy](../categories/compliance-privacy.md) — the regulatory erasure obligation and privacy handling belong there rather than the purge mechanism.

## What a finding here looks like

- A cache key built from a bare resource id with no tenant component, so one tenant reads another's entry on id reuse.
- A handler that reads the tenant from a query parameter or header instead of the authenticated token.
- A multi-tenant table whose isolation lives only in application WHERE clauses, with no database policy as a backstop.
- A shared queue where one tenant's backlog or poison message blocks every other tenant's processing.
- An offboarded tenant's rows still present in a search index, warehouse, or backup because the purge covered only the primary database.
