---
categories: [messaging-async, scaling-capacity]
domains: [data, reliability]
---

# Worker Pools

**SHOULD** size worker pools against queue arrival rates and set autoscaling bounds with starvation detection; undersized pools silently age jobs.

**Why:** A pool too small for peak load creates growing latency invisible until customers complain, while an oversized one wastes capacity and hides throughput regressions.

**Detect:** grep for `concurrency`, `pool_size`, `num_workers` without autoscaling policy; metrics showing queue depth rising while workers idle or saturated.

**References:** CWE-400, NIST SP 800-53 SC-5, Kubernetes HPA guidance
