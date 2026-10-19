---
categories: [cicd-pipeline-security]
domains: [infrastructure]
---

# Checkout Credential Persistence

**MUST** disable credential persistence in CI checkout steps and clear any token the runner writes into the workspace before later steps run.

**Why:** A token left in the git config by checkout is readable by every subsequent step, including third-party actions and build scripts.

**Detect:** grep actions/checkout steps that do not set persist-credentials: false

**References:** zizmor, https://github.com/zizmorcore/zizmor
