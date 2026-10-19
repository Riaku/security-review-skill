---
categories: [supply-chain]
domains: [infrastructure]
---

# Toolchain Compromise Modeling

**MUST** include build and design toolchains such as firmware compilers, hardware design flows, and training pipelines in the supply-chain threat model.

**Why:** A purely software compromise of the tooling rewrites the artifact, so hardware-grade assurance is only as strong as the pipeline that produced it.

**Detect:** compare the provenance and SBOM scope against the toolchain inventory; build tooling absent from both is unmodelled trust.

**References:** SOLARBURST-go-silicon (arXiv 2610.22580), https://arxiv.org/abs/2610.22580
