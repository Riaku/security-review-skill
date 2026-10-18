---
categories: [supply-chain]
domains: [infrastructure]
---

# Lockfiles

**MUST** commit and honor dependency lockfiles so every install resolves to identical, audited versions.

**Why:** Unpinned resolution lets a transitive dependency change silently between builds, opening the door to typosquat and version-rollback attacks.

**Detect:** Missing `package-lock.json`, `poetry.lock`, `go.sum`; CI flags like `--no-lock`, `npm install` without `ci`; `.gitignore` excluding lockfiles.

**References:** OWASP A06:2021, CWE-829, SCB-002

---

**Part of:** [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
