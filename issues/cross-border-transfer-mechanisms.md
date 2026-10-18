---
categories: [compliance-privacy, regulatory-frameworks]
domains: [governance, government-compliance]
---

# Cross-border data transfer mechanisms post-Schrems II

**SHOULD** use Standard Contractual Clauses with transfer impact assessments for EU data leaving adequacy-decision countries.

**Why:** Transferring EU data without valid safeguards violates GDPR Chapter V post-Schrems II, risking transfer bans and fines.

**Detect:** grep for EU data flows to non-adequate regions without SCC/TIA references; check `transfer_impact_assessment`, `scc_modules`, `adequacy` config absent.

**References:** GDPR Ch. V, Schrems II (C-311/18), EU SCC 2021/914, EDPB Recommendations 01/2020

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
