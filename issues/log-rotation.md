# Log Rotation

**MUST** configure rotation and retention for every locally written log file so disks never fill and evidence survives long enough to investigate.

**Why:** Unrotated logs fill the volume and crash the service, while over-short retention erases the audit trail mid-incident.

**Detect:** check logrotate configs, `maxSize`/`maxBackups` in winston/pino, `--log-opt max-size` in compose, or absent rotation on file appenders.

**References:** NIST SP 800-92, CWE-400, CIS Docker 2.4

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
