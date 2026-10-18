---
categories: [resilience]
domains: [reliability]
---

# Cascading Failures

**MUST** contain each failure at its origin with isolation, timeouts, and limits so faults cannot propagate downstream as overload.

**Why:** One slow dependency holds resources across every caller, turning a slowdown into an outage.

**Detect:** trace fan-out for missing `timeout` on HTTP/DB clients; no breaker on cross-service calls.

**References:** Google SRE Book cascading failures, AWS Well-Architected REL11, CWE-400

---

**Part of:** [resilience](../categories/resilience.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
