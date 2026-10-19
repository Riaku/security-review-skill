---
categories: [compliance-privacy]
domains: [governance]
---

# PCI DSS

**MUST NOT** store sensitive authentication data (full track, CVV, PIN block) after authorization completes.

**Why:** Retaining cardholder authentication data massively expands breach impact and violates contractual obligations with card brands.

**Detect:** grep for `cvv`, `track_data`, `pin_block` persisted post-auth; check database schemas, logs, and backups for prohibited fields.

**References:** PCI DSS 3.2.1 Req 3.2, PCI DSS 4.0 Req 3.3.1, CWE-312
