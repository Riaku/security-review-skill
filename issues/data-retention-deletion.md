---
categories: [compliance-privacy, database, multi-tenancy]
domains: [backend, data, governance]
---

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
