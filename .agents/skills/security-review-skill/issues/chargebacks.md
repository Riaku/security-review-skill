---
categories: [payments-fraud]
domains: [governance]
---

# Chargebacks

**SHOULD** implement fraud detection and transaction verification to keep chargeback ratios below card brand monitoring thresholds.

**Why:** Excessive chargebacks trigger card brand fines, higher processing rates, or termination of merchant privileges.

**Detect:** grep for missing 3D Secure, AVS, velocity checks in payment flows; check `chargeback_rate`, `fraud_score`, `three_ds` config absent.

**References:** Visa VDMP, Mastercard ECP
