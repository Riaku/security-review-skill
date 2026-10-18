# Architecture Fitness Functions in CI

**SHOULD** encode architectural constraints (dependency direction and depth, layering rules, latency budgets, secrets-only-via-secrets-layer) as executable checks that run in CI on every change, not as documentation reviewed once.

**Why:** ADRs record that a boundary was decided; fitness functions keep it from eroding over the next 200 commits. Unenforced architectural rules drift silently until they fail at scale, and a stated boundary with no automated check is indistinguishable from no boundary.

**Detect:** presence of ArchUnit, import-linter, dependency-cruiser, or custom structural validators wired into CI config; absence of any automated structural check is the finding.

**References:** catio.tech/blog/architecture-as-code, Ford/Parsons/Kua "Building Evolutionary Architectures" (fitness functions)

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
