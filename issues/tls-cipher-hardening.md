# TLS/ Cipher Suite Hardening (Mozilla profiles, disable legacy)

**MUST** Terminating endpoints offer only modern suites per the Mozilla Intermediate (or Modern) profile, and MUST NOT negotiate RC4, 3DES, SHA-1 MACs, export, or anonymous suites.

**Why:** Legacy ciphers carry known breaks — Sweet32 against 3DES, Lucky13 against CBC, total break of RC4 — so one enabled weak suite lets an on-path attacker force the connection down to a level they can decrypt.

**Detect:** Probe with `nmap --script ssl-enum-ciphers -p 443 host` or SSL Labs. Grep nginx `ssl_ciphers`, Java `jdk.tls.disabledAlgorithms`, and LB security policies for `RC4`, `3DES`, `MD5`, `NULL`. Verify TLS 1.2+ with AEAD preference.

**Bad:**
```nginx
ssl_ciphers "ALL:eNULL:RC4:3DES:+HIGH";   # everything and the kitchen sink
```

**Good:**
```nginx
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-ECDSA-CHACHA20-POLY1305;
ssl_protocols TLSv1.2 TLSv1.3;
```

**References:** Mozilla Server-Side TLS (Intermediate profile), RFC 8446, CWE-326 Inadequate Encryption Strength
