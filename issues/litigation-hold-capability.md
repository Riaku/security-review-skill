# Litigation Hold Capability

**SHOULD** be able to suspend retention/deletion policies on demand for legal preservation (litigation hold) across all data stores and logs.

**Why:** Automated retention deletion that can't be paused becomes spoliation of evidence; legal needs a kill-switch on the shredder.

**Detect:** review retention jobs for a hold flag respected at deletion time; check backup lifecycle, log rotation, and SaaS retention can be frozen per custodian/case; verify hold procedure is documented and tested.

**References:** EDRR model (NIST SP 800-221), FRCP 37(e), legal hold vendor docs (Exterro, Relativity)
