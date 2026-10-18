---
categories: [cloud-network, secrets-crypto]
domains: [backend, infrastructure]
---

# PQC readiness of TLS/VPN termination (hybrid KEM deployment)

**SHOULD** inventory every TLS and VPN termination point today and plan hybrid post-quantum key agreement (X25519 + ML-KEM) for long-lived, harvest-now-decrypt-later traffic before the client ecosystem forces a rushed rollout.

**Why:** Adversaries can record encrypted sessions now and decrypt them years later once quantum computers mature; data with a multi-decade confidentiality lifetime — VPN tunnels, backups, personal data — needs the quantum transition clocked deliberately, not in a panic.

**Detect:** Enumerate termination points (nginx/Apache, Envoy, cloud LBs, WireGuard/IPsec concentrators) and their TLS library versions; check for `ML-KEM`/`X25519MLKEM768` support (OpenSSL 3.5+, BoringSSL, cloud KMS PQC offerings), client-population coverage, and whether the inventory records each endpoint's data-sensitivity lifetime. Review VPN cipher suites for absence of any KEM upgrade path.

**Bad:**
```
# nginx pinned to OpenSSL 1.1.1 — no PQC group available, no upgrade plan
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384;
```

**Good:**
```
ssl_conf_param groups=X25519MLKEM768:X25519:secp384r1;  # hybrid, OpenSSL 3.5+
```

**References:** NIST FIPS 203 (ML-KEM), NIST PQC migration white papers, Cloudflare PQC deployment reports, IETF TLS hybrid KEM RFCs

---

**Part of:** [cloud-network](../categories/cloud-network.md) · [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
