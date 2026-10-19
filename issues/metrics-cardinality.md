---
categories: [observability]
domains: [reliability]
---

# Metrics Cardinality

**MUST NOT** label metrics with unbounded values like user IDs, emails, session tokens, or raw URLs.

**Why:** High-cardinality labels explode the time-series database, and attacker-crafted unique values can weaponize this into a denial-of-service against monitoring itself.

**Detect:** grep metric definitions for labels like `user=`, `email=`, `url=`, `path=` with raw request data; review Prometheus `label_replace` and histogram bucket counts.

**References:** Prometheus cardinality guidance, CWE-400
