---
categories: [data-pipelines]
domains: [data]
---

# Raw-Data Immutability

**MUST NOT** modify raw source data in place; transformations operate on copies, preserving the raw layer for re-derivation and audit.

**Why:** Edited raw data destroys the ability to re-audit cleaning decisions, re-run pipelines correctly, or prove what the original evidence said.

**Detect:** check storage layout for read-only raw layer (permissions, separate bucket/schema) vs in-place edits; review pipeline code for writes to raw datasets; check raw retention policy.

**References:** analysis data-management guidance (raw-as-read-only), medallion architecture raw-layer immutability
