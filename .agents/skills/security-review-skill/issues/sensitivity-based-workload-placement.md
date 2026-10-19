---
categories: [containers-k8s]
domains: [infrastructure]
---

# Sensitivity-Aware Workload Placement

**SHOULD** constrain placement so workloads of different data-sensitivity classes do not share a node by default, and treat the shared kernel as one failure domain.

**Why:** Namespace isolation is not a kernel boundary, so one kernel bug exposes every co-located workload regardless of what RBAC or NetworkPolicy says.

**Detect:** grep deployment manifests for nodeSelector, nodeAffinity, or tolerations keyed to a sensitivity class; their absence means default scheduling

**References:** NIST SP 800-190, https://doi.org/10.6028/NIST.SP.800-190
