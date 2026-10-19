---
categories: [supply-chain]
domains: [backend, infrastructure]
---

# Binary Composition Verification

**MUST** inventory third-party components from the shipped binary itself and reconcile that list against the build's declared dependencies.

**Why:** Declared manifests omit statically linked and vendored libraries, so a binary can carry an unpatched component that no SBOM records.

**Detect:** Run `syft <image-or-binary>` and diff its package list against the SBOM generated at build time.

**References:** AutoFirm (arXiv 2406.12947), https://arxiv.org/abs/2406.12947, OWASP CycloneDX specification
