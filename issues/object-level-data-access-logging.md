---
categories: [compliance-privacy, observability]
domains: [governance, reliability]
---

# Object-Level Data Access Logging

**SHOULD** enable data-plane (object/bucket-level) read and write logging on object storage holding sensitive data, not just control-plane API logging — management-plane logs record who created the bucket, but never who read the objects inside it.

**Why:** Object stores default to control-plane-only logging; a bulk exfiltration of customer records via thousands of `GetObject` calls is invisible until data-plane logging is turned on — after the incident. Compliance regimes (PCI, HIPAA, GDPR access-record duties) and forensic timelines both hinge on per-object access records that control-plane logs simply do not contain.

**Detect:** S3 server access logging or CloudTrail data events (`ReadOnly`/`WriteOnly` for the bucket prefix) enabled; GCS bucket audit configuration with `DATA_READ`/`DATA_WRITE` enabled; Azure Storage diagnostic settings including Read/Write/DELETE operations. Flag buckets with lifecycle policies but no data-event logging, and flag logging enabled only at management-event scope.

**References:** OWASP A09:2021 Logging and Monitoring Failures, AWS S3 data events / server access logging docs, GCP Cloud Storage audit logging, Azure Storage diagnostics, CIS AWS 3.x (logging), aquasecurity/trivy-checks storage logging rules
