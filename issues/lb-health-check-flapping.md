---
categories: [cloud-network, sre-incidents]
domains: [infrastructure, reliability]
---

# Load balancer health-check flapping detected and damped

**SHOULD** configure hysteresis on health checks — separate healthy/unhealthy thresholds, realistic timeouts, and jittered intervals — and alert on state-transition rate, not just current state.

**Why:** A single slow response ejects a healthy backend; when the ejected node's traffic overloads its siblings, they fail too, and the whole pool oscillates in a cascade. Flapping also thrashes DNS/LB control planes and hides the true failure during postmortems.

**Detect:** Review health-check configs (ALB target groups, nginx `max_fails`/`fail_timeout`, HAProxy `fall`/`rise`, Consul health checks) for threshold=1 on removal and timeouts tuned to p50 instead of p99. Query LB metrics for backend health-state transitions per minute; check whether monitoring fires on flapping patterns rather than only fully-down states.

**Bad:**
```
health_check: {interval: 2s, timeout: 1s, unhealthy_threshold: 1}
# one GC pause ejects a perfectly healthy node
```

**Good:**
```
health_check: {interval: 10s, timeout: 5s,
               unhealthy_threshold: 3, healthy_threshold: 2}
```

**References:** AWS ELB health check best practices, HAProxy tuning docs, Google SRE Book (overloading & health checks)

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [sre-incidents](../categories/sre-incidents.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
