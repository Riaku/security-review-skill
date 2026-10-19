---
categories: [observability, secrets-crypto]
domains: [infrastructure]
---

# Key Use Logging

**MUST** log every use of a key-management key with caller identity, operation, and target resource.

**Why:** Key use without an audit trail hides both misuse and the blast radius of a stolen credential. The log is the only record separating a legitimate decrypt from an exfiltration.

**Detect:** grep key-management client wrappers for audit emission on encrypt, decrypt, and sign calls; flag direct key-service calls that bypass the wrapper.

**References:** OWASP Proactive Controls C9, https://github.com/OWASP/www-project-proactive-controls, NIST SP 800-57 key management
