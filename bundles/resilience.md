# resilience — full checklist (17 items)

Fault-tolerance patterns under dependency failure.

> Generated artifact — edit the issue files, not this one. Manifest: [categories/resilience.md](../categories/resilience.md) · Index: [SKILL.md](../SKILL.md)

# Admission Webhook failurePolicy:Fail Deadlock and TLS Misconfig

**SHOULD** set `failurePolicy: Fail` only where the webhook is highly available, with valid TLS certs and namespace exclusions for its own namespace.

**Why:** A failing fail-closed webhook blocks all API writes cluster-wide; bad TLS makes every admission request error the same way.

**Detect:** ValidatingWebhookConfiguration with `failurePolicy: Fail` and no `namespaceSelector` excluding kube-system/webhook ns; expired or self-signed `caBundle`.

**References:** CIS K8s 5.2, K8s docs admission-webhook, CWE-833, SRE postmortem patterns

# Backlog Catch-Up Throttling

**SHOULD** throttle post-outage backlog replay below full consumer capacity so catch-up traffic does not overwhelm downstream services still recovering.

**Why:** Releasing a queued storm at full speed after an outage can knock over the very dependency that just came back, restarting the failure cycle.

**Detect:** grep recovery/runbook configs for missing `rate_limit`, `throttle`, `max_concurrency` on replay; consumers configured to drain queues unbounded on startup.

**References:** AWS SQS long polling backpressure, NIST SP 800-61 incident containment, Google SRE overload handling

# Backpressure

**MUST** reject or delay requests once queues pass a high-water mark, signaling overload upstream instead of absorbing unbounded inflow.

**Why:** A spike fills queues until memory exhaustion, turning a slowdown into a total outage for every tenant.

**Detect:** grep `queue_size`, `max_concurrent_requests`, `high_watermark`, `429 Too Many Requests`, unbounded `Queue()`.

**References:** RFC 6585, Netflix Hystrix concurrency limits, CWE-770, AWS REL11-BP04

# Bulkheads

**MUST** partition threads, connections, and pools per dependency or tenant so one saturated component cannot drain shared capacity.

**Why:** A slow downstream exhausting the common thread pool kills unrelated features that never touched it.

**Detect:** grep one global `ThreadPoolExecutor`, shared `HikariCP` pool, missing per-dependency `maxConnections`.

**References:** Fowler Bulkhead pattern, Hystrix thread isolation, AWS Well-Architected REL11-BP03, CWE-400

# Cascading Failures

**MUST** contain each failure at its origin with isolation, timeouts, and limits so faults cannot propagate downstream as overload.

**Why:** One slow dependency holds resources across every caller, turning a slowdown into an outage.

**Detect:** trace fan-out for missing `timeout` on HTTP/DB clients; no breaker on cross-service calls.

**References:** Google SRE Book cascading failures, AWS Well-Architected REL11, CWE-400

# Circuit Breakers

**MUST** open the circuit to a failing dependency after an error threshold, fail through a cool-off, then half-open probe before closing.

**Why:** Endless calls into a dying service waste caller threads and prolong its recovery.

**Detect:** grep `CircuitBreaker`, `resilience4j.circuitbreaker`, `failure_threshold`, `open_duration`; absence on outbound calls is the finding.

**References:** Fowler CircuitBreaker, resilience4j docs, AWS Well-Architected REL11-BP04, CWE-1098

# Graceful Degradation

**SHOULD** define a fallback per dependency so optional features shed instead of failing the whole request when a non-critical service is down.

**Why:** One optional enrichment service erroring should cost features, not the whole request.

**Detect:** grep `fallback`, `default_value`, cached-response fallbacks, per-dependency feature flags.

**References:** Netflix fallback patterns, Google SRE Book graceful degradation

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes; retried requests, network timeouts, and scripted replays trigger refund cascades that erode customer trust.

**Detect:** Check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache; grep payment API routes and migration files for `dedupe`.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key-header, CWE-837, AWS REL11-BP08

# Jitter

**MUST NOT** let retries, refreshes, or polling across replicas or clients share exact fixed intervals; randomize the timing (full/decorrelated jitter on retries) so timers never align.

**Why:** Identical timers synchronize into spikes that repeatedly knock over a recovering service.

**Detect:** grep `sleep(2 ** n)` without `random`, fixed `retryInterval`, round-time cron shared by replicas, missing `jitter`.

**References:** AWS exponential backoff and jitter, Google SRE retry guidance, CWE-400, REL11-BP06

# Kill-Switch Verification

**SHOULD** test that emergency feature kill-switches actually work (flip in staging, verify behavior) before relying on them in production.

**Why:** An untested kill-switch is a rumor: the flag path may be dead code, the config may not propagate, or the dependency may be the very thing that's failing.

**Detect:** check for scheduled kill-switch drills with recorded results; verify each critical feature has a flag whose off-path is exercised in tests; confirm flag-service outage behavior is a defined, tested state.

**References:** Netflix chaos/kill-switch practice, feature-flag resilience patterns, circuit-breaker companion issue

# Load Shedding

**SHOULD** drop low-priority traffic under saturation so core transactions keep latency and availability targets.

**Why:** Undifferentiated processing lets bulk or abusive requests starve revenue-critical paths, so the worst case hurts everyone equally.

**Detect:** grep `shed`, `admission_control`, `priority_queue`, feature-flag gating of non-critical endpoints.

**References:** AWS Architecture Center load shedding, Google SRE Book SLO shedding, CWE-400, REL11-BP05

# Retry Storms

**MUST NOT** retry without a hard budget shared across the call graph; nested retries multiply one failure into dozens.

**Why:** Three layers each retrying twice turns one blip into eight requests per caller.

**Detect:** count nested `@Retryable`, `max_retries`, `retry_times` per path; flag retry-on-timeout with no `retry_budget`.

**References:** Google SRE Book retry storms, AWS retry budget guidance, CWE-400, REL11-BP06

# Retry with Backoff (explicit policy: bounded retries, exponential + jitter)

**SHOULD** declare retry policy per call site: bounded count, exponential delay, randomized jitter; never infinite immediate retries.

**Why:** Unbounded or instant retries on transient errors become self-inflicted denial-of-service against recovering infrastructure; fixed-interval webhook delivery retries amplify a receiver outage into a hammering loop.

**Detect:** Grep `maxRetries`, `backoff_multiplier`, `jitter`, `RetryPolicy`; webhook senders lacking backoff/jitter/capped attempts or a terminal failure path; receivers lacking idempotent handling of repeated deliveries.

**References:** AWS exponential backoff and jitter, resilience4j Retry, CWE-400, OWASP Webhook Security Best Practices, Stripe retry docs

# Self-Healing Systems (auto-restart, auto-failover, self-repair loops)

**SHOULD** automate restart and failover only for known failure modes, keeping each repair loop bounded, observable, and rate-limited.

**Why:** Unmonitored auto-repair oscillates between nodes and masks root causes until capacity is silently exhausted.

**Detect:** review `restartPolicy`, `livenessProbe`, `auto_failover`, `recovery_loop`; check max-restart backoff and remediation alerting.

**References:** Kubernetes restartPolicy/livenessProbe, NIST SP 800-34 auto-recovery

# Startup Dependency Ordering

**MUST** have services retry with backoff until backends (DB, cache, queues) are reachable, rather than crash-on-first-failure at boot.

**Why:** A pod that dies because the database was seconds from ready enters CrashLoopBackOff, cascading restarts across the fleet during every rolling deploy.

**Detect:** grep readiness/liveness probes and init containers for backend-wait logic; check app boot for missing retry/backoff on connection errors and `initContainers` gating startup.

**References:** Kubernetes init containers & probes docs, AWS retry/backoff patterns, CWE-756 missing custom error handling, resilience4j patterns

# Thundering Herd

**SHOULD** stop many waiters waking at once on one cache expiry via single-flight refresh, stale-while-revalidate, or randomized TTLs.

**Why:** A hot key expiring sends thousands of requests straight to the database.

**Detect:** grep identical `ttl` on hot keys, fixed `expireAt`, missing `singleflight` or `stale-while-revalidate`, notify-all locks.

**References:** Thundering herd problem, Cloudflare stale-while-revalidate, nginx cache lock, CWE-770, REL11-BP04

# Timeout Budgets / Deadline Propagation

**MUST** propagate an end-to-end deadline through every downstream hop, each consuming from the remaining budget.

**Why:** Without a shared deadline, work continues on abandoned requests, burning capacity on results nobody reads.

**Detect:** check `context.WithTimeout` propagation, `grpc-timeout` / `X-Request-Deadline` headers, per-hop timeouts exceeding entry timeout.

**References:** gRPC Deadlines, Google SRE Book deadline propagation, CWE-400

