# multi-tenancy — full checklist (4 items)

Tenant isolation across API, data, cache, queues, and lifecycle.

> Generated artifact. Canonical source: `issues/<slug>.md`.

# Tenant-ID Spoofing at API Boundary

**MUST** derive the tenant from the authenticated session/token on every request — never from a client-supplied tenant_id parameter or header.

**Why:** The classic cross-tenant breach: API trusts `?tenant_id=` from the caller, letting one tenant read or mutate another's data with a valid session.

**Detect:** grep handlers for `tenant_id`/`org_id` read from query params, headers, or request bodies rather than from auth context; check middleware sets tenant once and handlers cannot override.

**References:** OWASP API1:2023 broken object level authorization, OWASP Multi-Tenant Security GS

# Cross-Tenant Cache Key Collision

**MUST** include tenant identity in every cache key for tenant-scoped data (cache, CDN, search index, session store).

**Why:** A cache key like `user:1042` without tenant scope serves tenant A's data to tenant B on ID reuse — a silent, high-volume cross-tenant leak.

**Detect:** grep cache set/get calls for keys lacking `tenant`/`org` components; check CDN cache keys and vary headers for tenant-scoped pages; review Redis key naming convention.

**References:** OWASP Multi-Tenant Security Guidance, CWE-922 insecure storage

# Tenant Offboarding Data Purge

**MUST** provide a verified, complete tenant purge: primary stores, replicas, caches, search indexes, backups policy, analytics, and third-party processors — with attestation evidence.

**Why:** Offboarded tenant data lingering in a warehouse layer or search index is a compliance breach waiting to be discovered; "we deleted the account" rarely means everything.

**Detect:** review offboarding runbook/code for coverage list vs actual datastore inventory; check for orphaned tenant rows (`SELECT tenant_id ... GROUP BY` vs active tenants); verify purge verification step exists.

**References:** GDPR Art. 17, SOC2 CC6, OWASP Multi-Tenant Security Guidance

# Shared-Queue Tenant Isolation

**SHOULD** isolate tenant workloads in queues by partition, dedicated queue, or per-message tenant enforcement so one tenant's burst or poison message cannot starve or crash others.

**Why:** Shared queues turn noisy neighbors into outages and let a poison message from tenant A block tenant B's processing indefinitely.

**Detect:** check queue topology for tenant partitioning (Kafka partition key = tenant, per-tenant SQS), per-tenant rate limits on producers, DLQ handling segregated per tenant.

**References:** OWASP Multi-Tenant Security Guidance (queue isolation patterns), bulkheads pattern

