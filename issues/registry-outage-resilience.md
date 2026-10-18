---
categories: [containers-k8s, supply-chain]
domains: [infrastructure]
---

# Registry Outage Tolerated via Cached/Pinned Images

**SHOULD** keep images cached on nodes and pinned by digest so a registry outage does not block scheduling or restarts.

**Why:** If a pod must pull during a registry outage, rescheduling and rollouts stall, turning a third-party outage into a cluster outage.

**Detect:** No `imagePullPolicy: IfNotPresent`/`Never` with pre-pulled images; no local registry mirror or pull-through cache configured.

**References:** K8s docs imagePullPolicy, NIST SP 800-190 4.4, Harbor/Docker registry mirror docs, OWASP A08

---

**Part of:** [containers-k8s](../categories/containers-k8s.md) · [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
