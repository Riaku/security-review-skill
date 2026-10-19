---
categories: [sre-incidents]
domains: [reliability]
---

# Connection Draining

**SHOULD** drain established connections at the load balancer before removing a backend from rotation.

**Why:** Abrupt backend removal mid-request severs long-poll and upload sessions, surfacing as random 502s during deploys.

**Detect:** `drain_timeout`, `idle_timeout` on Envoy/HAProxy, `notReadyBeforeDrainDelay`, missing `connectionDraining` in cloud LB config.

**References:** AWS ELB connection draining, Envoy drain documentation
