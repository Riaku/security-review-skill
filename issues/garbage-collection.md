---
categories: [scaling-capacity]
domains: [reliability]
---

# Garbage Collection

**MAY** tune GC pause targets and heap sizing per workload, but only after measuring pause distributions rather than defaulting to aggressive tuning.

**Why:** Untuned GC causes latency spikes at high allocation rates; blindly tuned GC causes thrashing and CPU starvation — both hurt tail latency under load.

**Detect:** grep for `GOGC`, `-Xmx`, `-XX:MaxGCPauseMillis`, `gc_pause_seconds` histograms in dashboards; check GC logs for pause p99 vs SLO and full-GC frequency.

**References:** CWE-400, Google SRE tail latency chapter, Java GC tuning guide (Oracle), Go runtime metrics docs

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
