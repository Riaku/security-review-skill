---
categories: [containers-k8s]
domains: [infrastructure]
---

# Resource Requests & Limits

**SHOULD** set explicit CPU/memory requests and limits on every container so one workload cannot starve the node or the scheduler cannot place blindly.

**Why:** Unbounded containers trigger noisy-neighbor degradation and OOM kills of unrelated pods under memory pressure.

**Detect:** Pod/Deployment YAML missing `resources.requests` or `resources.limits`; LimitRange absent in namespace.

**References:** CIS K8s 5.2.1, NIST SP 800-190 5.3, CWE-770, K8s docs resource-management

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
