---
categories: [secrets-crypto]
domains: [backend]
---

# Secrets Management

**MUST** source all secrets from a dedicated store (Vault, 1Password Connect, SOPS, cloud secret manager) rather than embedding them in images, repos, or plain ConfigMaps.

**Why:** Secrets baked into artifacts leak through registries, backups, and logs where they cannot be revoked cleanly.

**Detect:** `Secret` manifests with plaintext `data:`, `stringData:` without ESO/ExternalSecret, `secretKeyRef` absence alongside hardcoded tokens.

**References:** OWASP ASVS V2.10, CWE-259, NIST SP 800-57

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
