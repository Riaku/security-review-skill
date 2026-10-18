---
categories: [compliance-privacy, database]
domains: [data, governance]
---

# Erasure Propagation to Secondary Stores

**MUST** propagate deletion/erasure requests to every secondary copy: search indexes, caches, analytics, replicas, export buckets — and verify completion.

**Why:** Deleting the user row is the easy 20%; GDPR erasure fails on the other 80% — the Elastic index, the marketing export, the warehouse snapshot that still shows their email.

**Detect:** map erasure workflow against datastore inventory; check each secondary store has a delete-by-user step with verification; flag stores reachable only by "rebuild the whole index" with no SLA.

**References:** GDPR Art. 17 + Art. 19 notification, Google erasure guidance, DSAR automation practice

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [database](../categories/database.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
