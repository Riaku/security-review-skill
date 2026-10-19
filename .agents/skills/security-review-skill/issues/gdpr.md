---
categories: [compliance-privacy]
domains: [governance]
---

# GDPR

**MUST** process personal data of EU residents only under a documented lawful basis, with data minimization enforced at collection, and maintain the accountability artifacts regulators expect: DPO appointment where required (Art. 37), DPIAs for high-risk processing (Art. 35), and records of processing.

**Why:** Unlawful processing exposes organizations to fines up to 4% of global annual turnover under GDPR Article 83 — and enforcement is complaint- and breach-driven, so undocumented processing decisions become the fine's evidence.

**Detect:** grep for personal data fields collected without consent flags; check privacy policy config, `lawful_basis`, `consent_required` keys absent from data models; missing DPIAs, DPO designation, records of processing, consent logs, cross-border transfer clauses.

**References:** GDPR Arts. 5, 6, 35, 37, 83; ISO 27701; EDPB guidelines; ICO enforcement register
