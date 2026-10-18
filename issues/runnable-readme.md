---
categories: [documentation-quality]
domains: [backend]
---

# Runnable README

**MUST** provide a README that takes a newcomer from zero to running the project: prerequisites, install, run, test commands — each verified to actually work.

**Why:** The README is the first attack surface for wasted time and a common failure point in onboarding and incident response; untested commands rot within weeks and erode trust in all documentation.

**Detect:** run README commands verbatim in a clean environment (CI doc-testing where possible); flag missing install/run/test sections, version-pinned prerequisites that no longer exist, or "TODO" placeholders.

**References:** Google style guide (readme content), docs-as-code tested-README practice, twelve-factor dev-environment onboarding
