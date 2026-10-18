---
categories: [resilience]
domains: [reliability]
---

# Bulkheads

**MUST** partition threads, connections, and pools per dependency or tenant so one saturated component cannot drain shared capacity.

**Why:** A slow downstream exhausting the common thread pool kills unrelated features that never touched it.

**Detect:** grep one global `ThreadPoolExecutor`, shared `HikariCP` pool, missing per-dependency `maxConnections`.

**References:** Fowler Bulkhead pattern, Hystrix thread isolation, AWS Well-Architected REL11-BP03, CWE-400

---

**Part of:** [resilience](../categories/resilience.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
