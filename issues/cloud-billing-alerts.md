---
categories: [cloud-network]
domains: [infrastructure]
---

# Cloud Billing Alerts

**MUST** Budget alarms exist at account and per-project level, wired to a channel someone actually reads, with thresholds low enough to catch a runaway resource before it becomes a five-figure month.

**Why:** Compromised keys, crypto-mining spin-ups, and retry-storm Lambda loops all manifest first as a billing spike; teams without alarms discover them at invoice time, weeks after the abuse started.

**Detect:** Check IaC for AWS Budgets / GCP Budget Alerts / Azure Cost Management exports — absence is the finding. Verify recipients are distribution lists, not one departing engineer, and that daily-velocity checks exist alongside monthly totals.

**Bad:**
```
# no budgets defined; first signal is the month-end invoice: $41,000
```

**Good:**
```hcl
resource "aws_budgets_budget" "acct" {
  budget_limit { amount = 2000 cost_types { include_tax = true } }
  notification_type { threshold = 500 comparison_operator = "GREATER_THAN"
    subscriber_info { subscription_type = "EMAIL" address = "ops-alerts@corp" } }
}
```

**References:** AWS Budgets docs, GCP Budget alerts, CIS AWS Foundations 4.x, OWASP A09:2021 Logging & Monitoring Failures

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
