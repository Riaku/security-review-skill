---
categories: [testing-strategy]
domains: [backend]
---

# Static Gate Not Sufficient

**MUST NOT** treat a clean static-analysis run as evidence that input-dependent paths are secure.

**Why:** Vulnerabilities that depend on adversarial input, execution context, or chaining evade static checks while remaining exploitable.

**Detect:** command run the dynamic or exploit suite for the changed surface (`schemathesis`, `zap-baseline`, PoC tests) alongside the static gate.

**References:** Static-pass / dynamic-fail gap, https://arxiv.org/abs/2609.10762
