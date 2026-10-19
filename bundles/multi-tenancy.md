# multi-tenancy — full checklist (6 items)

Tenant isolation across API, data, cache, queues, and lifecycle.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/multi-tenancy.md](../categories/multi-tenancy.md) · Index: [SKILL.md](../SKILL.md)

# Cross-Tenant Cache Key Collision

**MUST** include tenant identity in every cache key for tenant-scoped data (cache, CDN, search index, session store).

**Why:** A cache key like `user:1042` without tenant scope serves tenant A's data to tenant B on ID reuse — a silent, high-volume cross-tenant leak.

**Detect:** grep cache set/get calls for keys lacking `tenant`/`org` components; check CDN cache keys and vary headers for tenant-scoped pages; review Redis key naming convention.

**References:** OWASP Multi-Tenant Security Cheat Sheet, CWE-922 Insecure Storage of Sensitive Information

# Data Retention, Erasure & Tenant Offboarding Purge

**MUST** automatically delete personal data when its retention period expires or a deletion request arrives, and propagate and verify the deletion across every secondary copy: search indexes, caches, analytics, replicas, export buckets, and backups; a departing tenant's data **MUST** be purged from primary stores, replicas, caches, search indexes, analytics, backups policy, and third-party processors, with verification and attestation evidence that the purge completed.

**Why:** Hoarding data beyond its purpose violates GDPR/CCPA erasure obligations and enlarges the breach blast radius — you cannot leak what you no longer hold. Offboarded tenant data lingering in a warehouse layer or search index is the same breach waiting to be discovered, and "we deleted the account" rarely means everything.

**Detect:** Grep for retention jobs (`DELETE ... WHERE created_at < ...`), tombstone/outbox patterns feeding replicas, and whether deletion covers search indexes and backup expiry; map the erasure workflow against a datastore inventory and require every store to have a verified delete-by-user step. A delete endpoint touching only the primary table is a gap. For offboarding, review the tenant purge runbook and code against the actual datastore inventory, look for orphaned tenant rows (`SELECT tenant_id ... GROUP BY` compared with the active-tenant set), and confirm a purge verification/attestation step exists.

**Bad:**
```python
@app.delete("/users/{id}")
def delete_user(id):
    db.users.delete(id)   # analytics replica keeps the row
```

**Good:**
```python
db.users.mark_deleted(id)          # tombstone
outbox.publish("user.deleted", id) # replicas, index, cache
```

**References:** GDPR Art. 17 Right to Erasure (and Art. 19 notification), CCPA deletion, NIST SP 800-53 SI-12 / AU-11, ISO 27018, SOC 2 CC6, OWASP Multi-Tenant Security Cheat Sheet

# Noisy-neighbor isolation between tenants/workloads

**MUST** enforce per-tenant or per-workload resource quotas (CPU, memory, I/O, connection rate) so one tenant's burst cannot degrade others sharing the host.
**SHOULD** apply ResourceQuota and LimitRange to every tenant namespace so one team cannot consume the whole cluster's compute.

**Why:** Without isolation, a single abusive or misbehaving tenant saturates shared CPU, disk I/O, or network, violating SLAs for everyone co-located, and a runaway or malicious workload in an unbounded namespace exhausts shared CPU/memory, degrading every other namespace on the cluster.

**Detect:** grep for `ResourceQuota`, `LimitRange`, `CPUShares`/`cpu_weight`, `blkio`/`IOClass`, per-tenant `rate_limit` in gateway config; flag shared pools with no per-tenant caps, namespaces with no `ResourceQuota`/`LimitRange` objects, and tenant namespaces sharing unbounded node pools.

**References:** CWE-770, Kubernetes QoS/ResourceQuota docs, CIS K8s 5.2.1, K8s quotas/limitranges docs, NIST SP 800-190 5.3

# Row-Level Security

**MUST** enforce row-level security (RLS) or equivalent tenant scoping in the database layer for every multi-tenant table, not only in application queries.

**Why:** A single missed WHERE clause in one code path leaks every tenant's rows; database-enforced policies fail closed instead.

**Detect:** grep for `ENABLE ROW LEVEL SECURITY`, `CREATE POLICY`, tenant_id filters in ORM raw queries; flag tables lacking policies.

**References:** OWASP A01:2021 Broken Access Control, CWE-285, PostgreSQL RLS docs, NIST SP 800-53 AC-3

# Shared-Queue Tenant Isolation

**SHOULD** isolate tenant workloads in queues by partition, dedicated queue, or per-message tenant enforcement so one tenant's burst or poison message cannot starve or crash others.

**Why:** Shared queues turn noisy neighbors into outages and let a poison message from tenant A block tenant B's processing indefinitely.

**Detect:** check queue topology for tenant partitioning (Kafka partition key = tenant, per-tenant SQS), per-tenant rate limits on producers, DLQ handling segregated per tenant.

**References:** OWASP Multi-Tenant Security Cheat Sheet (queue isolation patterns), bulkheads pattern

# Tenant-ID Spoofing at API Boundary

**MUST** derive the tenant from the authenticated session/token on every request — never from a client-supplied tenant_id parameter or header.

**Why:** The classic cross-tenant breach: API trusts `?tenant_id=` from the caller, letting one tenant read or mutate another's data with a valid session.

**Detect:** grep handlers for `tenant_id`/`org_id` read from query params, headers, or request bodies rather than from auth context; check middleware sets tenant once and handlers cannot override.

**References:** OWASP API1:2023 broken object level authorization, OWASP Multi-Tenant Security Cheat Sheet

