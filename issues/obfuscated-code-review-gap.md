---
categories: [supply-chain]
domains: [backend, frontend]
---

# Obfuscated Code Review Gap

**MUST** require reviewable source for every shipped third-party bundle, and treat a clean scan over obfuscated or minified code as no evidence.

**Why:** An adversary can iterate obfuscation until the scanner reports clean, so the gate is defeated by transformation alone rather than by a novel bug.

**Detect:** grep for vendored `.min.js` bundles and packer output with no matching source-map or upstream source reference in the lockfile.

**References:** Analyzing obfuscation against SAST pipelines (arXiv 2604.01131), https://arxiv.org/abs/2604.01131
