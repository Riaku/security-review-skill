---
categories: [mobile]
domains: [mobile]
---

# Mobile Certificate Pinning

**MUST** pin the server's certificate or public key (SPKI hash) for API traffic, with a documented rotation plan and backup pins.

**Why:** Without pinning, a user-installed root CA or compromised CA lets attackers intercept and modify all app traffic via MITM proxies.

**Detect:** grep for `certificatePinner`, `TrustKit`, `ServerTrustPolicy`, `network_security_config.xml` with `pin-set`; absence in Retrofit/OkHttp/URLSession configs.

**References:** OWASP MASVS-NETWORK-4, CWE-295, OWASP MAS Testing Guide Network Interception

---

**Part of:** [mobile](../categories/mobile.md) · [mobile](../domains/mobile.md) · [SKILL.md](../SKILL.md)
