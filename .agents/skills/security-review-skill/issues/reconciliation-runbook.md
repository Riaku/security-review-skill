---
categories: [payments-fraud]
domains: [governance]
---

# Reconciliation Runbook

**SHOULD** maintain a tested reconciliation process between internal records and external sources (PSP settlement files, bank statements, partner reports) with discrepancy handling.

**Why:** Money systems disagree with their counterparties routinely; without a reconciliation runbook, every mismatch becomes a fire-drill, and real losses hide in the "we'll check later" pile.

**Detect:** look for reconciliation jobs comparing internal ledger vs PSP/bank files with tolerance thresholds; check discrepancy queue with owner and SLA; verify runbook covers partial settlements and currency mismatches.

**References:** Stripe reconciliation guidance, PCI DSS 4.0 Req 10 (logging and monitoring), payments-engineering practice guides
