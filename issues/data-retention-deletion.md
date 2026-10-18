# Data Retention & Deletion Pipelines

**MUST** automatically delete personal data when its retention period expires or a deletion request arrives, and prove deletion propagated to replicas, caches, and backups.

**Why:** Hoarding data beyond its purpose violates GDPR/CCPA erasure obligations and enlarges the breach blast radius — you cannot leak what you no longer hold.

**Detect:** Grep for retention jobs (`DELETE ... WHERE created_at < ...`), tombstone/outbox patterns feeding replicas, and whether deletion covers search indexes and backup expiry. A delete endpoint touching only the primary table is a gap.

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

**References:** GDPR Art. 17 Right to Erasure, CCPA deletion, NIST SP 800-53 MP-6, ISO 27018

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [database](../categories/database.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
