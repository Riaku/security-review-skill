---
categories: [database, sre-incidents]
domains: [data, reliability]
---

# Backup Encryption & Immutable/Offsite Copies

**MUST** encrypt backups at rest and keep copies that are immutable (object-lock/WORM) and offsite, so a compromised production environment cannot destroy or tamper with every copy.

**Why:** Ransomware crews target backup repositories first: if backups are writable with production credentials, "we have backups" is an illusion. Encryption blocks exposure of regulated data; immutability survives both the ransomware and the burning building.

**Detect:** Bucket policies allowing `s3:BypassGovernanceRetention`, missing object lock/versioning, backup keys reachable from the production IAM role. Grep backup configs for absent encryption flags (`--encrypt`, SSE-KMS) and single-region destinations.

**Bad:**
```bash
# same writable bucket, same creds, plaintext
aws s3 cp /backups/db.tar s3://app-backups/db.tar
```

**Good:**
```bash
gpg --symmetric --cipher-algo AES256 db.tar
aws s3 cp db.tar.gpg s3://vault-backups/db/ \
  --server-side-encryption aws:kms
# bucket: object lock COMPLIANCE + cross-region replication
```

**References:** CIS Control 11 (immutable backups), NIST SP 800-53 CP-9, AWS S3 Object Lock docs, CWE-311
