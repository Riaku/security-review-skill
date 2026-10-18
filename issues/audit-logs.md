---
categories: [compliance-privacy]
domains: [governance]
---

# Audit Logs

**MUST** record security-relevant events (auth, access, privilege changes) with tamper-evident integrity and retention aligned to policy.

**Why:** Missing or mutable audit trails prevent incident reconstruction and violate compliance requirements for non-repudiation.

**Detect:** grep for auth/access handlers missing audit calls; check `audit_log`, `log_event`, HMAC signing, retention config absent.

**References:** CWE-778, NIST SP 800-92, SOC 2 CC7.2, PCI DSS 10.2
