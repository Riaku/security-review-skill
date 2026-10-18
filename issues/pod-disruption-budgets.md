# Pod Disruption Budgets

**SHOULD** define a PodDisruptionBudget for every highly-available workload so voluntary drains never take down all replicas at once.

**Why:** Without a budget, node upgrades or scale-downs can evict every replica simultaneously, causing an avoidable availability outage.

**Detect:** Deployments with `replicas > 1` and no matching `PodDisruptionBudget` kind; `minAvailable`/`maxUnavailable` unset cluster-wide.

**References:** K8s docs poddisruptionbudgets, SRE Workbook availability practices, NIST SP 800-190 5.4
