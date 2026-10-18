# Memory Leaks

**MUST NOT** ship long-running services without leak detection (heap trend monitoring or periodic profiling) wired into alerting.

**Why:** A slow leak stays invisible for days, then triggers OOM kills at the worst moment — during peak traffic — rather than at deploy time.

**Detect:** grep for `heap_dump`, `tracemalloc`, `pprof`, `jcmd`, `memory_usage` alerts with trend/slope thresholds; check for unbounded caches (`lru_cache` without maxsize, growing global dicts).

**References:** CWE-401, OWASP ASVS 14.2, NIST SP 800-53 SI-7

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
