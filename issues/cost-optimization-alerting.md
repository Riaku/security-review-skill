# Cost Optimization & Cost Alerting (unit-economics tracking, budget alarms, anomaly detection)

**SHOULD** Track unit economics — cost per request, per user, per pipeline run — alongside raw spend, and enable native anomaly detection so a cost surprise pages someone before the invoice does.

**Why:** Aggregate budgets miss slow-burn regressions like an N+1 query tripling per-request cost, and anomaly detection is often the first visible signal of credential abuse mining compute.

**Detect:** Check for Cost Anomaly Detection subscriptions and velocity-based thresholds. Flag teams tracking only monthly totals. Scan cost-explorer exports for idle resources: unattached EBS volumes, idle NAT gateways, oversized node pools.

**Bad:**
```
# one monthly total budget alarm at 100%; regressions invisible until overrun
```

**Good:**
```
# weekly cost/1k-requests trend + anomaly detection (daily, $50 threshold)
# routed to the owning team's channel, not just finance
```

**References:** AWS Cost Anomaly Detection docs, AWS Well-Architected Cost Optimization pillar, FinOps Framework (finops.org)

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
