---
categories: [cloud-network, secrets-crypto]
domains: [infrastructure]
---

# Encrypt Operational Channels

**MUST** encrypt management, monitoring, database, and partner connections to the same standard as user-facing traffic.

**Why:** Operational links carry credentials and full records over the same hostile network, and are the ones built before anyone wrote a TLS policy.

**Detect:** grep connection strings and agent config for `sslmode=disable`, `tls=false`, `insecure: true`; nmap --script ssl-enum-ciphers on 5432, 9090, 22.

**References:** OWASP ASVS v5.0, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x21-V12-Secure-Communication.md, NIST SP 800-52 Rev 2
