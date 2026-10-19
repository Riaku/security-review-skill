---
categories: [security-practices]
domains: [backend]
---

# Explicit Security Requirements in Specs

**MUST** state security behavior as explicitly and traceably as functional behavior in the specification that drives implementation or generation.

**Why:** A spec that describes function explicitly and security implicitly yields code that satisfies the visible requirements while dropping authorization and validation.

**Detect:** judgment: the spec — for each entity, a named requirement covering access, input validation, and failure behavior

**References:** SDD security benchmark, https://arxiv.org/abs/2606.00167
