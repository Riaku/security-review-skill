---
categories: [observability]
domains: [reliability]
---

# Flame Graphs

**SHOULD** make flame graphs available for CPU and allocation hot spots so performance regressions and abuse patterns are visually diagnosable.

**Why:** Attackers probing expensive endpoints look like ordinary slowness until a flame graph reveals the exact hot function being hammered.

**Detect:** check profiling pipeline outputs renderable flame graphs (pprof collapsed stacks, Speedscope JSON); verify runbooks link to them.

**References:** Brendan Gregg flame graphs, Google SRE Workbook, CWE-400

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
