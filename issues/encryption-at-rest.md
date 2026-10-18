# Encryption at Rest

**MUST** enable encryption at rest for databases, object storage, backups, and node disks holding sensitive data, with keys managed in a KMS rather than locally.

**Why:** Stolen drives, leaked snapshots, and misconfigured bucket exports expose everything unencrypted, bypassing every access control.

**Detect:** RDS/S3 `encrypted = false`, `storageClass` without SSE-KMS, Longhorn/Vault unencrypted PVCs, backup files with plaintext contents.

**References:** OWASP ASVS V0.9.2, CWE-311, NIST SP 800-53 SC-28
