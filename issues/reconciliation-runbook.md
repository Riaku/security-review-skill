# Reconciliation Runbook

**SHOULD** maintain a tested reconciliation process between internal records and external sources (PSP settlement files, bank statements, partner reports) with discrepancy handling.

**Why:** Money systems disagree with their counterparties routinely; without a reconciliation runbook, every mismatch becomes a fire-drill, and real losses hide in the "we'll check later" pile.

**Detect:** look for reconciliation jobs comparing internal ledger vs PSP/bank files with tolerance thresholds; check discrepancy queue with owner and SLA; verify runbook covers partial settlements and currency mismatches.

**References:** Stripe reconciliation guidance, PCI-DSS 9/10 financial monitoring, payments-engineering practice guides

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [sre-incidents](../categories/sre-incidents.md) · [reliability](../domains/reliability.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
