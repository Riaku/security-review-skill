# RTO & RPO

**MUST** define a recovery time objective and recovery point objective per service, and size infrastructure to meet both.

**Why:** Without agreed targets, teams under-protect critical services and discover the mismatch only during a real outage.

**Detect:** `rto:`/`rpo:` in SLO config, backup interval vs stated RPO mismatch, no restore-time test reports.

**References:** NIST SP 800-34, ISO 22301, Google SRE Workbook
