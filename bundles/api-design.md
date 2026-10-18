# api-design — full checklist (23 items)

Protocol and API contract design concerns.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/api-design.md](../categories/api-design.md) · Index: [SKILL.md](../SKILL.md)

# API Versioning

**SHOULD** version APIs explicitly via URL path or header from day one, keeping the breaking-change policy documented per version.

**Why:** Unversioned APIs force simultaneous upgrades of every consumer, turning one breaking change into a coordinated outage.

**Detect:** routes lacking `/v1/` prefix, absent `Accept-Version`/`Api-Version` header handling, no deprecation policy doc.

**References:** OWASP API 2023, Microsoft REST API Guidelines §10, Google AIP-180

# Backward Compatibility

**MUST NOT** remove or rename fields, endpoints, or enum values in a live API without a deprecation window and consumer migration path.

**Why:** Old clients in the wild — mobile apps, webhooks, cached integrations — break instantly on removal, and you cannot force their upgrade.

**Detect:** git diffs deleting response fields/routes without `@deprecated` markers; breaking-change linter (optic, oasdiff) absent from CI.

**References:** OWASP API 2023, Google AIP-180, oasdiff breaking-change rules

# Batching (many writes/calls, one trip)

**SHOULD** coalesce many small writes or downstream calls into batches sized to the workload instead of one network round trip per record.

**Why:** Per-record round trips multiply latency and connection consumption linearly; a burst that a batched writer absorbs in seconds can exhaust the connection pool and queue the whole service behind it — a self-inflicted availability problem.

**Detect:** Look for `for` loops calling `insert()`, `publish()`, or POST per item where a `bulk_insert`/`executemany`/bulk API exists. Check producers for missing batch tuning (Kafka `linger.ms`/`batch.size`, flush intervals in log and metrics shippers).

**Bad:**
```python
for row in rows:
    db.execute("INSERT INTO t VALUES (%s)", row)  # N trips
```

**Good:**
```python
execute_values(insert_stmt, rows, page_size=1000)  # one trip per page
```

**References:** Arjay McCandless System Design Cheat Sheet (batching), psycopg execute_values docs, Kafka batch.size/linger.ms docs

# Breaking-Change Linting in CI

**SHOULD** lint API changes against the previous published version for breaking changes (removed fields, changed types, new required params) before merge.

**Why:** Hand-review misses subtle contract breaks; automated diffing (oasdiff/buf breaking) catches them at the PR that introduces them, before consumers discover at runtime.

**Detect:** check CI for `oasdiff breaking`, `buf breaking`, `protolint`, or equivalent on API definition files; verify the comparison baseline is the last released version, not main.

**References:** oasdiff, buf breaking-change detection, Google AIP-180 backwards compatibility

# Compression

**SHOULD NOT** compress responses that contain attacker-controllable input alongside secrets in the same stream (CRIME/BREACH class).

**Why:** Adaptive compression of secrets with reflected input leaks tokens byte-by-byte through ciphertext length observations.

**Detect:** gzip/brotli on auth pages with CSRF tokens or API keys in body; `compression: true` with no secret-response exclusion.

**References:** CWE-310, CRIME (CVE-2012-4929), BREACH (CVE-2013-3587)

# CRDs Without OpenAPI Validation Schemas

**MUST** define an OpenAPI v3 validation schema for every CustomResourceDefinition so the API server rejects malformed objects before controllers see them.

**Why:** Schema-less CRDs admit arbitrary fields, letting a bad manifest crash controllers or smuggle input into privileged reconcile logic.

**Detect:** `kubectl get crd -o yaml` showing empty `validation.openAPIV3Schema`; CRDs missing `x-kubernetes-*` structural markers.

**References:** Kubernetes CRD validation docs, CWE-20, K8s API conventions

# Excessive Data Exposure in API Serialization

**MUST NOT** serialize whole ORM/model objects to API responses; project an explicit DTO containing only intended fields.

**Why:** Returning full models leaks password hashes, internal IDs, and PII that the UI never asked for but every caller now receives.

**Detect:** `jsonify(user)` / `resp.json(model)` patterns; serializers without field allowlists; `password`/`ssn` keys in response bodies.

**References:** OWASP API3:2023, CWE-213, Twitter CVE-2010-3851

# gRPC

**SHOULD** terminate gRPC behind a proxy that enforces TLS, message-size limits, and method-level authz rather than trusting plaintext backends.

**Why:** gRPC over h2c without interception skips WAF and auth layers, exposing every RPC method to anyone who can reach the port.

**Detect:** `grpc.InsecureServerCreds`, absent `max_receive_message_size`, Envoy routes without `ext_authz`/`jwt_authn` filters.

**References:** CWE-319, OWASP API 2023, gRPC security best practices

# HTTP Method Semantics

**MUST NOT** perform state-changing operations via GET or other safe methods; mutations belong in POST/PUT/PATCH/DELETE only.

**Why:** Crawlers, prefetchers, and proxies replay safe requests, turning a link click into unintended deletes or purchases.

**Detect:** grep GET route handlers for DB writes, `session.destroy`, token revocation, or side-effect service calls.

**References:** OWASP API3:2023, CWE-650, RFC 9110 §9.2

# HTTP Status Codes

**MUST** return accurate status codes: 401 for unauthenticated, 403 for unauthorized, 404 for missing resources, never 200 with an error body.

**Why:** Masking failures as 200 breaks client retry logic and lets attackers probe auth boundaries without signal.

**Detect:** grep handlers for `return 200` alongside error payloads; missing `401`/`403`/`404` in route error paths.

**References:** OWASP API2:2023, CWE-390, RFC 9110 §15

# HTTP/2

**SHOULD** enable HTTP/2 only with tuned flow-control windows and stream concurrency limits at the edge.

**Why:** Untuned multiplexing amplifies small-request floods into stream-exhaustion and slow-client window stalls across many logical streams.

**Detect:** `http2_max_concurrent_streams`, `initial_stream_window_size`, absent h2 settings in Envoy/nginx `http2` blocks.

**References:** RFC 9113 §6.9, CWE-400, nginx http2 directives

# HTTP/3 / QUIC

**SHOULD** validate that UDP 443 QUIC traffic passes the same authn/authz and rate limits as TCP TLS, since connection semantics differ.

**Why:** Middleboxes and legacy WAF rules keyed on TCP bypass QUIC entirely, giving attackers an unfiltered path to the origin.

**Detect:** `alt-svc: h3` advertised with no UDP firewall rules or QUIC-aware WAF; rate limiters bound to TCP sockets only.

**References:** RFC 9000, CWE-492, Cloudflare HTTP/3 deployment guidance

# Keep-Alive

**SHOULD** cap keep-alive idle timeouts and max requests per connection to bound resource hold per client.

**Why:** Unlimited persistent connections let a few clients exhaust the server's file descriptors, enabling slow-drain denial of service.

**Detect:** `keepalive_timeout 0`, absent `keepalive_requests`, nginx `worker_connections` vs unbounded upstream pools.

**References:** CWE-400, OWASP ASVS V5.1, nginx keepalive directive docs

# Long Polling

**MAY** use long polling where SSE or WebSockets are unavailable, but each held request MUST have a server-side timeout and per-client connection cap.

**Why:** Held-open requests with no timeout let clients pin worker threads indefinitely, collapsing capacity under modest concurrency.

**Detect:** polling handlers with no `setTimeout`/deadline, absent per-IP connection limits on `/poll` endpoints.

**References:** CWE-400, OWASP ASVS V5.2, MDN long polling guidance

# OpenAPI–Implementation Drift Check

**SHOULD** verify in CI that the served API matches its OpenAPI spec (request/response validation against the contract), failing on drift.

**Why:** A spec that lies is worse than no spec: consumers code against documented behavior the implementation quietly diverged from, and breaking changes ship "documented as safe."

**Detect:** check CI for contract tests (Dredd, Schemathesis, Prism, schemathesis fuzz mode), response-middleware spec validation, or oasdiff between released spec versions.

**References:** Schemathesis/Dredd docs, contract-testing practice, OWASP API Security (improper inventory)

# OpenAPI Specs

**MUST** validate incoming requests against the OpenAPI schema at the edge; the spec is enforcement, not just documentation.

**Why:** Docs-only specs let malformed or malicious payloads reach handlers that assume validated shapes, enabling injection and mass-assignment.

**Detect:** spec files present but no `openapi-validator`/`schemathesis` middleware; handlers ignoring `request.body` schema checks.

**References:** OWASP API3:2023, CWE-915, Schemathesis docs

# Protocol Buffers

**MUST NOT** reuse or repurpose reserved field numbers in .proto definitions; mark removed fields `reserved` to prevent wire-level confusion.

**Why:** A redeployed service decoding an old message under a reassigned field silently misinterprets data, corrupting records across versions.

**Detect:** .proto diffs removing fields without adding `reserved N;`; missing `reserved` blocks in evolved messages.

**References:** CWE-707, protobuf docs field reserved, Buf breaking-change rules

# Real-time Streaming

**MUST** authorize each stream subscription per-user; never broadcast a channel that any authenticated client can name and join.

**Why:** Predictable stream IDs let one user subscribe to another's private feed, turning a chat or notification channel into a data leak.

**Detect:** `channel.subscribe(channelName)` without per-user ACL check; predictable IDs like `order-{id}` with no ownership verification.

**References:** OWASP API1:2023, CWE-285, Ably/Pusher channel authorization docs

# Request Size Limits

**MUST** enforce a maximum request body size at the edge before parsing, rejecting oversized payloads with 413.

**Why:** Unbounded bodies let an attacker exhaust memory or CPU with one giant upload, bypassing per-request rate limits entirely.

**Detect:** `client_max_body_size 0`, absent `maxBodySize`/`limit` in Express/Flask/Spring config, no 413 handling.

**References:** CWE-400, OWASP ASVS V5.2, nginx client_max_body_size directive

# Server-Sent Events

**SHOULD** set `Cache-Control: no-store` and enforce authentication on SSE endpoints, since EventSource cannot send custom headers.

**Why:** Proxies may cache an event stream containing user data, and token-in-URL patterns leak credentials into logs and referrers.

**Detect:** SSE routes without `Cache-Control`, `text/event-stream` handlers taking `?token=` query params.

**References:** CWE-525, OWASP ASVS V9.1, MDN EventSource security notes

# Timeout Budgets / Deadline Propagation

**MUST** propagate an end-to-end deadline through every downstream hop, each consuming from the remaining budget.

**Why:** Without a shared deadline, work continues on abandoned requests, burning capacity on results nobody reads.

**Detect:** check `context.WithTimeout` propagation, `grpc-timeout` / `X-Request-Deadline` headers, per-hop timeouts exceeding entry timeout.

**References:** gRPC Deadlines, Google SRE Book deadline propagation, OWASP ASVS V5, CWE-400

# Token Revocation & Logout Invalidation

**MAY** rely on short expiry alone for stateless tokens, but MUST provide a revocation list or denylist for high-value sessions where immediate logout is required.

**Why:** A pure stateless JWT cannot be logged out; a stolen token keeps working until expiry even after the user hits logout.

**Detect:** grep logout handler for missing token blacklist/`jti` denylist, no `/revoke` endpoint, Redis denylist absent, logout only clears client cookie.

**References:** RFC 7009, RFC 8725 §4.1, OWASP A02:2021, NIST SP 800-53 SC-23

# WebSockets

**MUST** authenticate the upgrade handshake and validate the Origin header on every WebSocket connection.

**Why:** Cross-site WebSocket hijacking lets a victim's browser open an authenticated socket to your API, streaming private data to an attacker's page.

**Detect:** `Upgrade: websocket` handlers missing `checkOrigin`/`Origin` validation; auth deferred to post-open messages.

**References:** OWASP API 2023, CWE-346, RFC 6455 §10.2

