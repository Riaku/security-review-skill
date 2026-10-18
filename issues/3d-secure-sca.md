---
categories: [payments-fraud]
domains: [governance]
---

# 3D Secure / SCA

**MUST** trigger 3DS2 challenge flows for high-risk transactions and honor the issuer's authentication result before capturing funds.

**Why:** Skipping SCA shifts liability onto the merchant and exposes EU/UK cards to fraudulent chargebacks under PSD2 rules.

**Detect:** grep for `three_d_secure`, `sca_required`, `exemption`, `ds.transstatus` in payment service code and gateway config.

**References:** PSD2 Article 97, EMV 3-D Secure 2.x (EMVCo), CWE-287, Stripe 3DS2 docs

---

**Part of:** [payments-fraud](../categories/payments-fraud.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)
