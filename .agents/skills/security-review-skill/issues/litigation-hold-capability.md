---
categories: [compliance-privacy]
domains: [governance]
---

# Litigation Hold Capability

**SHOULD** be able to suspend retention/deletion policies on demand for legal preservation (litigation hold) across all data stores and logs.

**Why:** Automated retention deletion that can't be paused becomes spoliation of evidence; legal needs a kill-switch on the shredder.

**Detect:** review retention jobs for a hold flag respected at deletion time; check backup lifecycle, log rotation, and SaaS retention can be frozen per custodian/case; verify hold procedure is documented and tested.

**References:** EDRM (edrm.net), FRCP 37(e), NIST SP 800-53 SI-12/AU-11, legal hold vendor docs (Exterro, Relativity)
