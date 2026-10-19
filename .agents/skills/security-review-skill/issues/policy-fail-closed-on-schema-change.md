---
categories: [containers-k8s]
domains: [infrastructure]
---

# Policy Fail-Closed on Schema Change

**MUST** fail closed when a policy rule no longer matches a changed request schema, instead of silently admitting traffic that stopped matching.

**Why:** Policy rules keyed to field paths break quietly on schema evolution: unmatched traffic keeps flowing while the control reports healthy.

**Detect:** grep admission, WAF, and gateway rules for field paths (`spec.`, `request.object.`) and check a test pins each rule to the schema version it targets.

**References:** Kubernetes Security Concepts, https://kubernetes.io/docs/concepts/security/
