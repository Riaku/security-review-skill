---
categories: [containers-k8s, correctness-pitfalls]
domains: [backend, infrastructure]
---

# Missing ownerReferences Causing Orphaned Managed Resources

**SHOULD** set `ownerReferences` on every resource a controller creates so cascading deletion reclaims them automatically.

**Why:** Orphaned resources accumulate invisibly, leaking quotas, secrets, and network policies after their parent is gone.

**Detect:** Created resources lacking `metadata.ownerReferences`; garbage collector cannot trace children; orphan count grows over time.

**References:** K8s docs garbage collection, ownerReferences, CWE-404, operator-sdk ownership patterns

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [correctness-pitfalls](../categories/correctness-pitfalls.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
