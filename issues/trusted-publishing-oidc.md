---
categories: [supply-chain]
domains: [infrastructure]
---

# Tokenless Artifact Publishing

**SHOULD** publish artifacts through short-lived federated identity instead of long-lived registry API tokens stored in CI.

**Why:** A publish token is stealable, rarely rotated, and usually scoped wider than one release; a federated identity exists only for the job.

**Detect:** grep NPM_TOKEN, PYPI_API_TOKEN, or CARGO_REGISTRY_TOKEN secrets in publish workflows; expect id-token: write instead

**References:** zizmor, https://github.com/zizmorcore/zizmor
