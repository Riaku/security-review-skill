---
categories: [secrets-crypto, supply-chain]
domains: [backend, infrastructure]
---

# Secret Scanning

**MUST** run automated secret scanning (gitleaks, trufflehog, GitHub push protection) on every commit and full-history scans before publishing any repository.

**Why:** Developers routinely commit live credentials under deadline pressure; without scanning, leaks ship silently to public or shared remotes — and a secret once committed stays in git history forever, so rotation is the only true fix and is often missed.

**Detect:** `.gitleaks.toml`, `.pre-commit-config.yaml` with gitleaks/trufflehog hooks that reject at commit/push time, absent GitHub `secret_scanning`/push-protection settings in org config.

**References:** OWASP ASVS V2.10.2, CWE-540, CWE-319, NIST SP 800-218 (SSDF), GitHub push protection docs

---

**Part of:** [secrets-crypto](../categories/secrets-crypto.md) · [supply-chain](../categories/supply-chain.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
