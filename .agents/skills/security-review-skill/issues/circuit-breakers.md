---
categories: [resilience]
domains: [reliability]
---

# Circuit Breakers

**MUST** open the circuit to a failing dependency after an error threshold, fail through a cool-off, then half-open probe before closing.

**Why:** Endless calls into a dying service waste caller threads and prolong its recovery.

**Detect:** grep `CircuitBreaker`, `resilience4j.circuitbreaker`, `failure_threshold`, `open_duration`; absence on outbound calls is the finding.

**References:** Fowler CircuitBreaker, resilience4j docs, AWS Well-Architected REL11-BP04, CWE-1098
