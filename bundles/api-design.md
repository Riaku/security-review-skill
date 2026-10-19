# api-design — full checklist (37 items)

Protocol and API contract design concerns.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/api-design.md](../categories/api-design.md) · Index: [SKILL.md](../SKILL.md)

# API Version Retirement

**MUST** assess every older API version against the security fixes shipped in newer ones, then backport the fix or retire the version by a deadline.

**Why:** An old version left running keeps the vulnerability the new one fixed, and clients have no incentive to move. Without a retirement date the insecure surface is permanent.

**Detect:** judgment: the version support matrix and route table — each live version mapped to a security-fix status and an announced end date.

**References:** OWASP API Security Top 10 (2023) API9 (improper inventory management), https://github.com/OWASP/API-Security

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

# Bounding Protocol Element Lengths

**MUST** cap the length of every parsed protocol element — method, header name and value, status phrase, numeric field, chunk size — not only the body.

**Why:** Unbounded element parsing is the substrate for arithmetic and buffer overflows, and the spec's own limits are minima rather than safe defaults.

**Detect:** grep edge and server config for header limits (`large_client_header_buffers`, `max-http-header-size`, `LimitRequestFields`) and flag services that limit bodies but not headers.

**References:** RFC 9110 HTTP Semantics, https://httpwg.org/specs/rfc9110.html

# Breaking-Change Linting in CI

**SHOULD** lint API changes against the previous published version for breaking changes (removed fields, changed types, new required params) before merge.

**Why:** Hand-review misses subtle contract breaks; automated diffing (oasdiff/buf breaking) catches them at the PR that introduces them, before consumers discover at runtime.

**Detect:** check CI for `oasdiff breaking`, `buf breaking`, `protolint`, or equivalent on API definition files; verify the comparison baseline is the last released version, not main.

**References:** oasdiff, buf breaking-change detection, Google AIP-180 backwards compatibility

# Capability Wrapper Types

**MUST** confine dangerous capabilities inside validated wrapper types so an untrusted value cannot reach the sink unparsed.

**Why:** A rule enforced by the type system cannot be forgotten at a new call site. Raw strings everywhere make every sink a fresh review question.

**Detect:** Inspect sink signatures: the safe API takes a wrapper (parsed URL, trusted markup, bound query) rather than a raw string.

**References:** Trusted Types, https://w3c.github.io/trusted-types/dist/spec/

# Compression

**SHOULD NOT** compress responses that contain attacker-controllable input alongside secrets in the same stream (CRIME/BREACH class).

**Why:** Adaptive compression of secrets with reflected input leaks tokens byte-by-byte through ciphertext length observations.

**Detect:** gzip/brotli on auth pages with CSRF tokens or API keys in body; `compression: true` with no secret-response exclusion.

**References:** CWE-203, CRIME (CVE-2012-4929), BREACH (CVE-2013-3587)

# Conformance Test Vectors

**SHOULD** publish test vectors and measurable conformance criteria with any protocol or interface that others must implement.

**Why:** Without shared vectors, every implementation interprets the specification differently and interoperability pressure spreads the weakest reading.

**Detect:** Check the spec or interface package for a vectors/testdata corpus and a statement of what passing means.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf

# Content-Type Enforcement

**MUST** reject request bodies whose declared Content-Type is not the one the endpoint expects, before parsing.

**Why:** Parsers disagree about ambiguous bodies, so a form-encoded or text payload can be read as JSON or the reverse. That disagreement turns cross-site protections and validation rules into no-ops.

**Detect:** grep route handlers and framework config for explicit content-type rejection (`415`, `UnsupportedMediaType`, `request.is_json`); flag endpoints that parse whatever arrives.

**References:** OWASP REST Security Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html, CWE-436 Interpretation Conflict

# CRDs Without OpenAPI Validation Schemas

**MUST** define a structural OpenAPI v3 validation schema (`spec.versions[*].schema.openAPIV3Schema`) for every CustomResourceDefinition so the API server rejects malformed objects before controllers see them.

**Why:** Schema-less CRDs admit arbitrary fields, letting a bad manifest crash controllers or smuggle input into privileged reconcile logic.

**Detect:** `kubectl get crd -o yaml` and inspect `spec.versions[*].schema.openAPIV3Schema` for `x-kubernetes-preserve-unknown-fields: true`, `additionalProperties: true`, or empty `properties` objects — for `apiextensions.k8s.io/v1` a structural schema is required, so validation is only ever absent by explicit opt-out.

**References:** Kubernetes CRD validation docs, CWE-20, K8s API conventions

# WebSockets: Upgrade Authentication & Origin Validation (CSWSH)

**MUST** authenticate the upgrade handshake and validate the `Origin` header against an explicit allowlist on every WebSocket connection.

**Why:** WebSockets ignore CORS, so any malicious site can open a socket using the victim's cookies and act as them in real time, streaming private data to the attacker's page.

**Detect:** grep `ws://`, `wss://`, `Upgrade: websocket` upgrade handlers, `onConnection` without origin checks (missing `checkOrigin`/`Origin` validation) or with auth deferred to post-open messages; nginx `proxy_set_header Origin` passthrough config.

**References:** CWE-1385, CWE-346, OWASP A01:2021, OWASP API 2023, RFC 6455 section 10.2

# Excessive Data Exposure in API Serialization

**MUST NOT** serialize whole ORM/model objects to API responses; project an explicit DTO containing only intended fields.

**Why:** Returning full models leaks password hashes, internal IDs, and PII that the UI never asked for but every caller now receives.

**Detect:** `jsonify(user)` / `resp.json(model)` patterns; serializers without field allowlists; `password`/`ssn` keys in response bodies.

**References:** OWASP API3:2023, CWE-213

# Extension Threat Review

**MUST** re-check every new use case or extension against the threat model the design was reviewed under before shipping it.

**Why:** An extension inherits the old guarantees without inheriting the assumptions that produced them, converting a reviewed design into an unreviewed one.

**Detect:** List the shipped extensions and confirm each has a threat-model entry dated after the extension.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf

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

**References:** RFC 9113 §6.5.2 and §6.9, CWE-400, nginx http2 directives

# HTTP/3 / QUIC

**SHOULD** validate that UDP 443 QUIC traffic passes the same authn/authz and rate limits as TCP TLS, since connection semantics differ.

**Why:** Middleboxes and legacy WAF rules keyed on TCP bypass QUIC entirely, giving attackers an unfiltered path to the origin.

**Detect:** `alt-svc: h3` advertised with no UDP firewall rules or QUIC-aware WAF; rate limiters bound to TCP sockets only.

**References:** RFC 9000, CWE-693, Cloudflare HTTP/3 deployment guidance

# Out-of-Band Control Signals

**MUST** carry authentication and routing control signals out-of-band, or authenticate them independently, when payload data shares the same channel.

**Why:** Anyone able to inject into the shared channel can forge control semantics, and the receiver cannot distinguish a forgery from a legitimate signal.

**Detect:** judgment: the protocol framing — whether control fields sit in the same stream as user data and how they are authenticated

**References:** Anderson, Security Engineering 3rd ed., ch.22, https://www.cl.cam.ac.uk/~rja14/Papers/SEv3-ch22.pdf

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

# Mandatory Extension Enforcement

**MUST** fail the connection when a peer does not acknowledge a security-critical protocol extension, even where the feature it protects is unused locally.

**Why:** An extension that is negotiated but not required lets a downgrade happen quietly, which is how renegotiation and triple handshake attacks survived patches.

**Detect:** testssl.sh --severity HIGH against the endpoint; it reports Secure Renegotiation and Extended Master Secret support.

**References:** RFC 9325 §3.5, https://www.rfc-editor.org/rfc/rfc9325.html, RFC 7627 (extended master secret), CVE-2009-3555

# Minimize Configuration Modes

**SHOULD** delete configuration modes and options the actual use case does not need, rather than shipping every mode the design can express.

**Why:** Each mode multiplies the testable surface and adds a deployable-insecure state that no test covers.

**Detect:** grep for mode/algorithm/profile switches reading from config or environment, and count the combinations the test suite actually exercises.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf

# Misuse-Resistant Security APIs

**SHOULD** make the safe path the default in security APIs, with every opt-out explicit, named and greppable.

**Why:** Developers use the default, so an unsafe default ships vulnerabilities at scale; an opt-out buried in configuration cannot be inventoried or restricted.

**Detect:** Security wrappers whose defaults disable checks: `verify=False`, `dangerouslyAllow*`, `Insecure*`, or `allow_all` as a parameter default.

**References:** Tink misuse-resistant crypto APIs, https://github.com/tink-crypto/tink

# No Caller-Supplied Security Config

**MUST** let a caller pass in the sanitizer, validator or policy that governs its own operation.

**Why:** A pass-through parameter turns the safety check into an argument the attacker controls, and each call site can opt out without touching the library.

**Detect:** Security-helper signatures taking `sanitizer=`, `validator=`, `policy=` or `trusted=` and forwarding them to the sink.

**References:** Trusted Types, https://w3c.github.io/trusted-types/dist/spec/

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

# Shared Field Semantics

**MUST** document, for every field crossing a component boundary, who may write it and what each consumer interprets it to mean.

**Why:** Differential parsing turns a shared struct into a bypass: the front end validates one interpretation while the back end acts on another. Ambiguous fields are where those disagreements live.

**Detect:** Inspect the shared schema or IDL for per-field comments naming the writer and each reader's interpretation.

**References:** Orange Tsai: confusion attacks, https://blog.orange.tw/posts/2024-08-confusion-attacks-en/

# Third-Party Response Validation

**MUST** validate and sanitize data returned by third-party APIs before using it in queries, rendering, or authorization decisions.

**Why:** An integration is another input channel: a compromised or misconfigured provider can return markup, a query fragment, or an unexpected type. Trusting it moves an injection sink inside your trust boundary.

**Detect:** grep integration response handling for provider fields interpolated directly into SQL, HTML, shell, or policy checks without schema validation.

**References:** OWASP API Security Top 10 (2023) API10 (unsafe consumption of APIs), https://github.com/OWASP/API-Security, CWE-20 Improper Input Validation

# Timeout Budgets / Deadline Propagation

**MUST** propagate an end-to-end deadline through every downstream hop, each consuming from the remaining budget.

**Why:** Without a shared deadline, work continues on abandoned requests, burning capacity on results nobody reads.

**Detect:** check `context.WithTimeout` propagation, `grpc-timeout` / `X-Request-Deadline` headers, per-hop timeouts exceeding entry timeout.

**References:** gRPC Deadlines, Google SRE Book deadline propagation, CWE-400

# Token Revocation & Logout Invalidation

**MAY** rely on short expiry alone for stateless tokens, but MUST provide a revocation list or denylist for high-value sessions where immediate logout is required.

**Why:** A pure stateless JWT cannot be logged out; a stolen token keeps working until expiry even after the user hits logout.

**Detect:** grep logout handler for missing token blacklist/`jti` denylist, no `/revoke` endpoint, Redis denylist absent, logout only clears client cookie.

**References:** RFC 7009 §2.1 (revocation request), OWASP A02:2021, NIST SP 800-53 SC-23

# Unsafe Boundary Obligations

**MUST** document the caller preconditions of every unsafe or privilege-crossing API at the function itself.

**Why:** An unsafe boundary is safe only if callers uphold specific invariants. Undocumented obligations get violated by the next developer and surface as memory corruption or privilege escalation.

**Detect:** `unsafe fn` blocks with no `# Safety` section; FFI/syscall wrappers and `raw`/`trusted` parameters with no documented precondition.

**References:** arXiv:2308.04785, https://arxiv.org/abs/2308.04785

