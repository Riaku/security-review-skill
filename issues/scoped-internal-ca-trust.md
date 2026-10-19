---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Scoped Internal CA Trust

**MUST** trust only the specific internal authority or certificate each peer actually uses, rather than a broad system trust store.

**Why:** Trusting every public CA for an internal hop lets any certificate holder impersonate the service, which is the whole point of a private deployment.

**Detect:** grep client config for `NODE_EXTRA_CA_CERTS` pointing at the system bundle, `ssl_ca_certs` with a shared bundle, or `InsecureSkipVerify`.

**References:** OWASP ASVS v5.0 V12, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x21-V12-Secure-Communication.md, CWE-295
