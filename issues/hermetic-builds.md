---
categories: [cicd-pipeline-security, supply-chain]
domains: [infrastructure]
---

# Hermetic Builds (no undeclared network/env deps during build)

**SHOULD NOT** let builds reach undeclared network or environment inputs; every dependency must be declared and cached.

**Why:** Non-hermetic builds silently pull mutated packages mid-build, leaving artifacts unreproducible and quietly tamperable.

**Detect:** grep CI for `--network=none`, unguarded `curl`/`pip install` outside lockfiles, ambient `export` in build scripts.

**References:** SLSA build isolation, NIST SP 800-218 (SSDF), Reproducible Builds project, CWE-494

---

**Part of:** [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [supply-chain](../categories/supply-chain.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
