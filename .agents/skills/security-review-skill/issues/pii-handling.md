---
categories: [compliance-privacy]
domains: [governance]
---

# PII Handling

**SHOULD NOT** transmit or store unencrypted personally identifiable information outside designated secure stores.

**Why:** Unencrypted PII in transit or at rest enables mass identity theft and triggers mandatory breach disclosure obligations.

**Detect:** grep for SSN, email, phone fields serialized without encryption; check TLS enforcement, `encrypt_pii`, field-level encryption config keys.

**References:** CWE-311, CWE-312, NIST SP 800-122, GDPR Art. 32
