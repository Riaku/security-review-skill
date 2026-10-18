---
categories: [caching]
domains: [reliability]
---

# Cache Hit Ratio

**SHOULD** monitor cache hit ratio per key namespace and alert when it collapses, since a miss storm pushes every request to the backing store.

**Why:** Sudden miss spikes are both a denial-of-service amplifier and a signal of key-cardinality attacks.

**Detect:** Metrics dashboards missing `cache_hits`/`cache_misses` counters; Redis INFO stats `keyspace_hits` untracked.

**References:** OWASP A05:2021, CWE-400, NIST SP 800-53 SC-5

---

**Part of:** [caching](../categories/caching.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
