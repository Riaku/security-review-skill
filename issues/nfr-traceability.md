# Non-Functional Requirements Traceability

**SHOULD** record non-functional requirements (scale targets, latency SLOs, availability, durability, compliance) as explicit, testable constraints that architecture decisions reference.

**Why:** Untestable "should be fast" requirements hide their violation until production; hard constraints (10M DAU, <200ms p95, 99.99% uptime) make every design choice auditable and every gap visible before launch.

**Detect:** look for an NFR/requirements doc or ADRs citing concrete numbers; check SLO definitions trace back to stated requirements rather than post-hoc guesses.

**References:** Google SRE SLO chapter, DDIA requirements-driven design, ADR practice

---

**Part of:** [scaling-capacity](../categories/scaling-capacity.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
