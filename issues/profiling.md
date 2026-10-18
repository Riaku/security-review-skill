# Profiling

**MAY** run continuous CPU/heap profiling in production at low overhead to catch performance anomalies early.

**Why:** Profilers expose hot paths where resource-exhaustion attacks (ReDoS, decompression bombs) concentrate, but only if capture is already running when the incident hits.

**Detect:** grep for `py-spy`, `pprof`, `async-profiler`, `continuous profiling` in deployment manifests; verify overhead budget documented.

**References:** Google SRE Book Ch.6 monitoring, CWE-400, Datadog continuous profiling docs

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
