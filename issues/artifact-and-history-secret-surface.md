---
categories: [secrets-crypto]
domains: [infrastructure]
---

# Build Artifact Secret Scanning

**MUST** scan every built package and image layer for credentials before publishing it, not only the source tree.

**Why:** A credential baked into a package or image layer ships to every consumer and is invisible to working-tree scans.

**Detect:** `trufflehog filesystem` or `gitleaks dir` against the built artifact and each extracted image layer before publish.

**References:** Threagile accidental-secret-leak risk, https://github.com/Threagile/threagile/blob/master/pkg/risks/scripts/accidental-secret-leak.yaml, Docker image secret leakage study (arXiv 2307.03958), https://arxiv.org/abs/2307.03958
