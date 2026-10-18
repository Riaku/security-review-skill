---
categories: [payments-fraud, regulatory-frameworks]
domains: [governance, government-compliance]
---

# PCI DSS as Audit Regime (SAQ, CDE scoping)

**MUST** scope the cardholder data environment accurately and complete the correct SAQ level (or full ROC) for the actual card data flow, not the desired one.

**Why:** Under-scoped CDEs are the most common PCI failure: one stray database storing PANs drags the whole network into breach liability.

**Detect:** grep for "PAN", "cardholder", "CDE", "SAQ-" in configs; card data in logs, unsegmented networks, SAQ type mismatched to flow.

**References:** PCI DSS v4.0.1, SAQ A-D, PCI SSC scoping guidance

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
