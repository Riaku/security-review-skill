# correctness-pitfalls

Language-agnostic code-level failure modes.

## What this category covers

This category covers the classes of bug that have nothing to do with an attacker and everything to do with the code being wrong: arithmetic and representation, bounds and ordering, concurrency, and the error handling that decides whether a fault stays local. The items span numeric correctness (floating-point comparison and accumulation, currency as integers, integer overflow and range checks), text handling (character encoding, code-point versus byte length, and truncation assumptions, off-by-one bounds), and time (time zones, daylight-saving transitions). They also cover concurrency and async behavior (thread safety, blocking a shared event loop, unhandled async errors, trigger throttling), algorithmic cost on unbounded input, edge cases and schema validation, structured exception handling, and code-hygiene traps such as merge conflicts, config-example drift, business-logic bypass, dead code, and tracked technical debt. Expect findings that describe wrong behavior with an input a user or caller can actually supply, not a style preference.

- Numeric correctness: floating-point comparison and accumulation, currency as integers, and integer overflow.
- Bounds and indexing: off-by-one errors in loops, slices, pagination, and buffer sizes.
- Text and encoding: character encoding, code-point versus byte length, and truncation assumptions.
- Time and scheduling: time-zone handling and daylight-saving transitions.
- Concurrency and async: shared mutable state, blocking a shared event loop, unhandled async errors, and trigger throttling.
- Complexity and control flow: cost on unbounded input, edge cases, schema validation, structured exceptions, dead code, and merge hygiene.

## What it does not cover

- [api-design](../categories/api-design.md) — the external API contract (versioning, status codes, transport) belongs there rather than the code implementing it.
- [testing-strategy](../categories/testing-strategy.md) — test design and quality gates belong there rather than the defect classes themselves.
- [distributed-systems](../categories/distributed-systems.md) — partial failure, ordering, and delivery guarantees across services belong there.
- [caching](../categories/caching.md) — cache invalidation and consistency concerns belong there rather than in-process state.

## What a finding here looks like

- Currency accumulated in binary floating point, so totals drift and repeated runs disagree.
- A loop bound or slice range off by one, dropping or duplicating records.
- A scheduled job that fires twice or not at all across a daylight-saving transition.
- Shared mutable state mutated from multiple threads without a lock or atomic.
- A CPU-bound call inside a shared event loop, stalling every concurrent request.
