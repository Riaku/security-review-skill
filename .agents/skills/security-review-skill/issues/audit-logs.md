---
categories: [compliance-privacy, observability]
domains: [governance, reliability]
---

# Audit Logs

**MUST** record security-relevant events (auth, access, privilege changes) with tamper-evident integrity and retention aligned to policy; **SHOULD** keep compliance-relevant audit evidence on append-only/WORM storage with integrity hashing or signing and documented custody, so insider tampering is detectable.

**Why:** Missing or mutable audit trails prevent incident reconstruction and violate compliance requirements for non-repudiation.

**Detect:** grep for auth/access handlers missing audit calls; check `audit_log`, `log_event`, HMAC signing, retention config absent; check log destinations for immutability (S3 Object Lock, BigQuery time-travel, hash-chained logs), verify hash/signature chain continuity, and confirm audit-log deletion is itself alarmed.

**References:** CWE-778, NIST SP 800-92, AWS S3 Object Lock WORM, SOC 2 CC7.2/CC4, PCI DSS 10.2
