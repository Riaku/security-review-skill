---
categories: [scaling-capacity]
domains: [backend]
---

# Per-User Storage Quotas

**MUST** enforce per-user quotas on total stored bytes and object count, not only on individual request size.

**Why:** Per-request limits leave the aggregate unbounded, so a patient client fills the volume and the bill with millions of individually legal uploads.

**Detect:** grep upload handlers for a per-user aggregate check and for the quota record it consults; its absence means only per-request limits apply.

**References:** OWASP ASVS v5.0 V5, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x14-V5-File-Handling.md
