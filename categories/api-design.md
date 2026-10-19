# api-design

Protocol and API contract design concerns.

## What this category covers

This category covers the contract and transport an API exposes, independent of whether anyone is attacking it: how it versions, what it guarantees across releases, which protocol and semantics it uses, and how it behaves at its limits. The items span versioning and deprecation, backward compatibility and breaking-change linting, HTTP method and status-code semantics, request-size and content-encoding limits, OpenAPI specs as enforcement plus the drift check against the implementation, and CRD validation schemas. They also cover protocol and transport selection (HTTP/2, HTTP/3 and QUIC, gRPC, protocol buffers, content encoding, and idle connection reuse), streaming transports (WebSockets, server-sent events, long polling, real-time streaming), call coalescing, deadline propagation, and token revocation at the boundary. Expect findings phrased as contract defects: a live field removed without a deprecation path, a mutation carried on a safe method, a status code that lies, or an endpoint with no request-size or deadline limit.

- Versioning and compatibility: explicit versions, deprecation windows, breaking-change linting, and removal of fields or enum values.
- HTTP contract semantics: method safety, status codes, request-size limits, content encoding, and idle connection reuse.
- Schema and spec discipline: OpenAPI as enforcement, CRD validation schemas, protocol buffers, and spec-to-implementation drift.
- Protocol and transport selection: HTTP/2, HTTP/3 and QUIC, gRPC, and content encoding.
- Streaming and real-time APIs: WebSockets, server-sent events, long polling, and per-subscription authorization.
- Performance-shaping concerns: call coalescing, deadline propagation, and token revocation at the boundary.

## What it does not cover

- [web-api-security](../categories/web-api-security.md) — the attack surface on those endpoints belongs there rather than the contract itself.
- [correctness-pitfalls](../categories/correctness-pitfalls.md) — language-level code failure modes belong there rather than the API's external contract.
- [distributed-systems](../categories/distributed-systems.md) — cross-service coordination such as retries and delivery semantics belongs there.
- [documentation-quality](../categories/documentation-quality.md) — prose documentation standards belong there, distinct from the machine-checked contract.

## What a finding here looks like

- A response field or enum value removed on a live version with no deprecation window, breaking clients already in the wild.
- A state-changing operation reachable through GET, so a prefetch or crawler performs it.
- A 200 response carrying an error body instead of 401, 403, or 404.
- An endpoint accepting an unbounded request body or stream because no edge size cap exists.
- A service that does not propagate a deadline, so a downstream hop can hang past the caller's timeout.
