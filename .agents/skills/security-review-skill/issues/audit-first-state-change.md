---
categories: [observability]
domains: [backend, infrastructure]
---

# Audit-First State Changes

**MUST** write the audit record in the same transaction as the state change, so neither commits without the other.

**Why:** A change that lands without its record leaves the audit trail asserting a world that is no longer true, and no later reconciliation can recover it.

**Detect:** grep state-changing handlers and deploy scripts for an audit write outside the same transaction, or after the mutation returns.

**References:** Audit-first rollback semantics (arXiv 2609.00406), https://arxiv.org/abs/2609.00406
