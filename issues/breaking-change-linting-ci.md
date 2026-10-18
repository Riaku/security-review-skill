# Breaking-Change Linting in CI

**SHOULD** lint API changes against the previous published version for breaking changes (removed fields, changed types, new required params) before merge.

**Why:** Hand-review misses subtle contract breaks; automated diffing (oasdiff/buf breaking) catches them at the PR that introduces them, before consumers discover at runtime.

**Detect:** check CI for `oasdiff breaking`, `buf breaking`, `protolint`, or equivalent on API definition files; verify the comparison baseline is the last released version, not main.

**References:** oasdiff, buf breaking-change detection, Google AIP-180 backwards compatibility

---

**Part of:** [api-design](../categories/api-design.md) · [cicd-pipeline-security](../categories/cicd-pipeline-security.md) · [backend](../domains/backend.md) · [infrastructure](../domains/infrastructure.md) · [SKILL.md](../SKILL.md)
