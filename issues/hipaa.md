---
categories: [compliance-privacy, regulatory-frameworks]
domains: [governance, government-compliance]
---

# HIPAA (health data)

**MUST** safeguard protected health information with access controls, encryption in transit, and audit logs covering every system in the HIPAA covered entity or business associate chain.

**Why:** Unlogged PHI access and plaintext transmissions drive the largest class of healthcare breaches and OCR enforcement actions.

**Detect:** grep for PHI/ePHI handling without encryption/TLS, missing audit logging, third-party analytics SDKs receiving patient data.

**References:** HIPAA Security Rule 45 CFR 164, HHS OCR guidance, NIST HIPAA Security Series

---

**Part of:** [compliance-privacy](../categories/compliance-privacy.md) · [regulatory-frameworks](../categories/regulatory-frameworks.md) · [governance](../domains/governance.md) · [government-compliance](../domains/government-compliance.md) · [SKILL.md](../SKILL.md)
