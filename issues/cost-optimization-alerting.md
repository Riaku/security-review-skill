---
categories: [cloud-network, observability]
domains: [infrastructure, reliability]
---

# Cost Optimization & Cost Alerting (unit-economics tracking, budget alarms, anomaly detection)

**MUST** budget alarms exist at account and per-project level, wired to a channel someone actually reads, with thresholds low enough to catch a runaway resource before it becomes a five-figure month.
**SHOULD** track unit economics — cost per request, per user, per pipeline run — alongside raw spend, and enable native anomaly detection so a cost surprise pages someone before the invoice does.

**Why:** Compromised keys, crypto-mining spin-ups, and retry-storm Lambda loops all manifest first as a billing spike; teams without alarms discover them at invoice time, weeks after the abuse started. Aggregate budgets miss slow-burn regressions like an N+1 query tripling per-request cost, and anomaly detection is often the first visible signal of credential abuse mining compute.

**Detect:** Check IaC for AWS Budgets / GCP Budget Alerts / Azure Cost Management exports — absence is the finding. Verify recipients are distribution lists, not one departing engineer, and that daily-velocity checks exist alongside monthly totals. Check for Cost Anomaly Detection subscriptions and velocity-based thresholds. Flag teams tracking only monthly totals. Scan cost-explorer exports for idle resources: unattached EBS volumes, idle NAT gateways, oversized node pools.

**Bad:**
```
# no budgets defined at all; first signal is the month-end invoice: $41,000
# one monthly total budget alarm at 100%; regressions invisible until overrun
```

**Good:**
```
# weekly cost/1k-requests trend + anomaly detection (daily, $50 threshold)
# routed to the owning team's channel, not just finance
# plus account/per-project aws_budgets_budget at a low threshold -> ops-alerts@corp distribution list
```

**References:** AWS Budgets docs, GCP Budget alerts, CIS AWS Foundations 4.x, OWASP A09:2021 Logging & Monitoring Failures, AWS Cost Anomaly Detection docs, AWS Well-Architected Cost Optimization pillar, FinOps Framework (finops.org)
