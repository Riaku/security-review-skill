---
categories: [containers-k8s]
domains: [infrastructure]
---

# Pod Disruption Budgets

**SHOULD** define a PodDisruptionBudget for every highly-available workload so voluntary drains never take down all replicas at once.

**Why:** Without a budget, node upgrades or scale-downs can evict every replica simultaneously, causing an avoidable availability outage.

**Detect:** Deployments with `replicas > 1` and no matching `PodDisruptionBudget` kind; `minAvailable`/`maxUnavailable` unset cluster-wide.

**References:** K8s docs poddisruptionbudgets, SRE Workbook availability practices, NIST SP 800-190 5.4

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
