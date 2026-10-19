---
categories: [authorization-access-control, payments-fraud]
domains: [backend, governance]
---

# Dual Approval Irreversible

**MUST** require two independent approvers for high-value, irreversible actions such as large transfers, contract approvals, or safety overrides.

**Why:** A single actor who can both initiate and release an irreversible action is indistinguishable from an attacker holding that account.

**Detect:** trace the approval workflow and confirm no single identity can complete both the request and the release step.

**References:** OWASP ASVS v5.0 V2, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x11-V2-Validation-and-Business-Logic.md, NIST SP 800-53 AC-5
