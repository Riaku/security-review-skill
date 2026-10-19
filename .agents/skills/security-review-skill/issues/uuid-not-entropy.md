---
categories: [secrets-crypto]
domains: [backend]
---

# UUIDs Are Not Secrets

**MUST NOT** use time-ordered or MAC-derived identifiers (UUIDv1, UUIDv7, ULID) as unguessable tokens or secret material.

**Why:** Time-ordered identifiers disclose their creation instant and host, and their structure shrinks the search space a capability token must make infeasible.

**Detect:** grep token, reset, and API-key generation for `uuid1`, `uuid7`, `ulid`, and `uuid4()` where the value is used as a capability.

**References:** OWASP ASVS v5.0 V11.5.1, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x20-V11-Cryptography.md, CWE-330
