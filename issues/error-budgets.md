# Error Budgets

**SHOULD** spend the gap between 100% and the SLO as a budget for risky releases, freezing changes when exhausted.

**Why:** Without a shared budget, reliability debates become endless opinion fights instead of an agreed mechanical tradeoff.

**Detect:** `error_budget` in SLO config, multi-window multi-burn-rate alert thresholds, no freeze policy on exhaustion.

**References:** Google SRE Workbook (error budgets), Prometheus multi-window multi-burn-rate alerting
