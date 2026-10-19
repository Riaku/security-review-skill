---
categories: [sre-incidents]
domains: [reliability]
---

# Multi-Region

**SHOULD** deploy across regions only when latency and data residency allow, with explicit region-failure semantics.

**Why:** Cross-region replication lags or split-brains; without a defined loss model, a region outage corrupts what redundancy was meant to protect.

**Detect:** `region:` keys, `global-load-balancer`, `cross-region` replication flags, DNS failover records, GDPR data-residency config.

**References:** NIST SP 800-34, AWS Well-Architected reliability pillar, GDPR Art. 44
