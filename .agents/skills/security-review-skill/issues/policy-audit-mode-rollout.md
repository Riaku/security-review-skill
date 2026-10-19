---
categories: [deployment-release]
domains: [infrastructure]
---

# Policy Audit-Mode Rollout

**SHOULD** roll each new enforcement policy out in audit or dry-run mode first, converting every would-be denial into a reviewed exception before blocking is enabled.

**Why:** Blocking policy enabled on first deploy breaks legitimate workloads and teaches teams to route around the control instead of fixing the finding.

**Detect:** grep policy manifests and Helm values for enforcementMode: dryrun|audit or --dry-run flags on the admission controller

**References:** Gatekeeper audit mode, https://github.com/open-policy-agent/gatekeeper
