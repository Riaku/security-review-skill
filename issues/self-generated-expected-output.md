---
categories: [testing-strategy]
domains: [backend]
---

# Self-Generated Expected Output

**MUST NOT** derive a test's expected output from the code under test (golden files generated from current implementation, assertions copied from actual run).

**Why:** A test whose expectation came from the implementation can never catch the implementation being wrong — it enshrines today's bug as tomorrow's contract, especially dangerous for security golden-hashes.

**Detect:** review golden/expected files for how they were produced (independent source vs generated-from-implementation); flag "update goldens" workflows without review of what changed and why.

**References:** testing anti-pattern literature (tautological tests), characterization-testing caveats

---

**Part of:** [testing-strategy](../categories/testing-strategy.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
