# Jitter

**MUST NOT** schedule retries, refreshes, or polling on exact fixed intervals; randomize timing so replica timers never align.

**Why:** Identical timers synchronize into spikes that repeatedly knock over a recovering service.

**Detect:** grep `sleep(2 ** n)` without `random`, fixed `retryInterval`, round-time cron shared by replicas, missing `jitter`.

**References:** AWS exponential backoff and jitter, Google SRE retry guidance, CWE-400, REL11-BP06

---

**Part of:** [resilience](../categories/resilience.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
