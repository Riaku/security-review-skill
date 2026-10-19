---
categories: [resilience]
domains: [reliability]
---

# Jitter

**MUST NOT** let retries, refreshes, or polling across replicas or clients share exact fixed intervals; randomize the timing (full/decorrelated jitter on retries) so timers never align.

**Why:** Identical timers synchronize into spikes that repeatedly knock over a recovering service.

**Detect:** grep `sleep(2 ** n)` without `random`, fixed `retryInterval`, round-time cron shared by replicas, missing `jitter`.

**References:** AWS exponential backoff and jitter, Google SRE retry guidance, CWE-400, REL11-BP06
