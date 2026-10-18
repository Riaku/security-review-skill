# Audit-Log Chain of Custody

**SHOULD** make audit evidence tamper-evident: append-only/WORM storage, integrity hashing or signing, and documented custody for compliance artifacts.

**Why:** Audit findings you can't prove weren't altered are worthless in court or a regulator's hands; tampering by an insider must be detectable.

**Detect:** check log destinations for immutability (S3 Object Lock, BigQuery time-travel, blockchain/hash-chained logs); verify hash/signature chain continuity; check deletion of audit logs is itself alarmed.

**References:** NIST 800-92 log management, AWS S3 Object Lock WORM, SOC2 CC4 evidence integrity
