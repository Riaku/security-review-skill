# Data Exfiltration Monitoring

**SHOULD** baseline per-host and per-account egress volume and alert on anomalous outbound transfers, especially off-hours and to untrusted destinations.

**Why:** Stolen data must leave the network eventually; without egress baselines, a multi-gigabyte dump to an unknown endpoint looks like ordinary traffic.

**Detect:** grep flow-log analytics for `bytes_out` thresholds, new-destination first-seen alerts, and DB export / S3 egress alarms; verify egress paths are actually observable.

**References:** MITRE ATT&CK T1048 Exfiltration Over Alternative Protocol, T1567, CWE-200, NIST SP 800-53 AC-4

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [observability](../categories/observability.md) · [infrastructure](../domains/infrastructure.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
