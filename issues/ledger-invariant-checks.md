---
categories: [payments-fraud]
domains: [governance]
---

# Ledger Invariant Checks

**MUST** enforce ledger invariants continuously: sum of debits equals sum of credits, no negative balances where prohibited, every money movement has a counter-entry.

**Why:** Silent ledger drift (rounding, partial writes, bugs) compounds into real financial loss; systems without invariant checks discover errors at reconciliation time — too late to cheaply fix.

**Detect:** check for invariant assertions in the ledger layer (double-entry enforcement, balance checks in transactions), scheduled integrity queries, and alarm (not just log) on violation.

**References:** Double-entry bookkeeping in software (Martin Fowler), Stripe financial-modeling talks

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
