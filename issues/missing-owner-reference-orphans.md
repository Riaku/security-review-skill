---
categories: [containers-k8s]
domains: [infrastructure]
---

# Missing ownerReferences Causing Orphaned Managed Resources

**SHOULD** set `ownerReferences` on every resource a controller creates so cascading deletion reclaims them automatically.

**Why:** Orphaned resources accumulate invisibly, leaking quotas, secrets, and network policies after their parent is gone.

**Detect:** Created resources lacking `metadata.ownerReferences`; garbage collector cannot trace children; orphan count grows over time.

**References:** K8s docs garbage collection, ownerReferences, CWE-404, operator-sdk ownership patterns
