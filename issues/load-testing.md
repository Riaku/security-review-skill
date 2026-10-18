---
categories: [scaling-capacity]
domains: [reliability]
---

# Load Testing

**SHOULD** load-test at or above expected peak with realistic traffic mix, including failure injection, before committing to a capacity number.

**Why:** Untested capacity claims collapse under real traffic composition — burst patterns, hot keys, and slow dependencies never appear in synthetic averages.

**Detect:** grep repo for `k6`, `locust`, `gatling`, `wrk`, `chaos`, test reports with `p99` and error-rate thresholds; flag tests that only check mean latency or run below peak.

**References:** OWASP ASVS 14.2, NIST SP 800-184, AWS Well-Architected REL11-BP04
