# resilience

Fault-tolerance patterns under dependency failure.

## What this category covers

This category covers how a running system behaves when a dependency is slow, failing, or returning errors. Member items span the request-path patterns that contain that failure — timeouts and deadline propagation, bounded retries with backoff and jitter, circuit breakers, bulkheads, backpressure, and load shedding — plus the recovery patterns that follow an outage, such as throttled backlog catch-up and bounded self-healing. They also cover idempotency for retried side effects, startup ordering against a recovering backend, and verification of emergency controls. A reviewer should expect findings about a failure that is amplified rather than contained: retries that multiply, timers that synchronize, or one slow dependency that consumes shared capacity.

- Time control: timeout budgets, deadline propagation, and retry policy.
- Failure containment: circuit breakers, bulkheads, and graceful degradation.
- Overload behavior: backpressure, load shedding, and queue high-water marks.
- Synchronization hazards: jitter, thundering herd, and retry storms across the call graph.
- Recovery: backlog catch-up throttling, bounded self-healing, and kill-switch verification.
- Autonomous-loop bounds: iteration and wall-clock budgets on agent loops with a declared degraded exit.

## What it does not cover

- [sre-incidents](../categories/sre-incidents.md) — incident command, on-call, SLOs, and DR drills belong there; this category is the in-system behavior.
- [distributed-systems](../categories/distributed-systems.md) — consensus, replication, and consistency models belong there.
- [messaging-async](../categories/messaging-async.md) — broker delivery semantics, consumer groups, and dead-letter handling belong there.

## What a finding here looks like

- A call site has no deadline, or a downstream hop resets the deadline instead of consuming the remaining budget.
- Retries are unbounded, immediate, or stacked across layers, so one blip becomes a multiplicative load increase.
- A single thread or connection pool serves every dependency, so one slow backend starves unrelated features.
- A hot cache key expires and every waiter queries the backing store at once.
- A post-outage backlog is replayed at full speed and knocks over the dependency that just recovered.
