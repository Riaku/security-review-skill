---
categories: [observability]
domains: [reliability]
---

# Distributed Tracing

**MUST** propagate trace context across all service and queue boundaries so a single request is followable end to end.

**Why:** Without continuous traces, cross-service attacks (request tampering, lateral calls) fragment into unrelated spans nobody connects.

**Detect:** grep for `traceparent` / `tracestate` header propagation in HTTP clients and message producers; check tracer init covers every framework middleware.

**References:** W3C Trace Context, OpenTelemetry documentation

---

**Part of:** [observability](../categories/observability.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
