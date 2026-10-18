# messaging-async — full checklist (22 items)

Queues, delivery semantics, workers, jobs.

> Generated artifact — edit the issue files, not this one. Sources: [issues/](../issues/) · manifest: [messaging-async](../categories/messaging-async.md) · index: [SKILL.md](../SKILL.md)

# At-Least-Once Delivery

**SHOULD** document at-least-once semantics explicitly and require idempotent consumers, since redelivery on ack failure is guaranteed.

**Why:** Duplicate charges, double emails, and duplicated inventory movements arise when handlers assume single delivery.

**Detect:** grep for `ack` after processing, `auto_ack=True`, missing idempotency keys, `at_least_once`, unguarded side effects in consumers.

**References:** CWE-362, AWS SQS delivery semantics, NIST SP 800-171 3.1.1

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Background Jobs

**MUST** enforce timeouts and retry limits on background jobs; a hung job holding a lock or connection pool slot can cascade into outage.

**Why:** Untimed jobs accumulate, exhaust DB pools and workers, and mask failures that surface only as total system stall.

**Detect:** grep for job definitions missing `timeout`, `max_retries`, `dead_timeout`; Sidekiq/Celery configs without `soft_time_limit` or `expires`.

**References:** OWASP ASVS 7.4, CWE-400, Celery task timeout guidance

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Backlog Catch-Up Throttling

**SHOULD** throttle post-outage backlog replay below full consumer capacity so catch-up traffic does not overwhelm downstream services still recovering.

**Why:** Releasing a queued storm at full speed after an outage can knock over the very dependency that just came back, restarting the failure cycle.

**Detect:** grep recovery/runbook configs for missing `rate_limit`, `throttle`, `max_concurrency` on replay; consumers configured to drain queues unbounded on startup.

**References:** AWS SQS long polling backpressure, NIST SP 800-61 incident containment, Google SRE overload handling

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [resilience](../categories/resilience.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Long-running jobs checkpoint so restarts resume, not restart

**MUST** persist progress checkpoints in long-running batch jobs so an interrupted run resumes from the last checkpoint instead of reprocessing from the beginning.

**Why:** A six-hour job that restarts from zero after an hour-five crash can never finish — every attempt dies at the same wall, or completes while re-emitting side effects for the replayed range.

**Detect:** Inspect job code for a persisted cursor (last processed ID, offset, timestamp) written at intervals and read on startup. Grep for jobs that recompute `MIN(id)` at start instead of loading the stored watermark.

**Bad:**
```python
rows = db.rows.all()          # 6h job, from zero every crash
for r in rows: process(r)
```

**Good:**
```python
cur = store.get("job_cursor", 0)
for r in db.rows.gt(cur).limit(1000):
    process(r); store.put("job_cursor", r.id)
```

**References:** Arjay McCandless cheat sheet (checkpointing), Kafka consumer offset docs, AWS fault-tolerant batch guidance

---

**Part of:** [database](../categories/database.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Overlapping cron executions guarded by single-runner locks

**MUST** guard scheduled jobs with a single-runner lock (advisory lock, flock, or leader election) so a slow run cannot overlap the next scheduled tick.

**Why:** If a nightly job outlives its interval, two copies run at once: duplicate charges, double-sent emails, deadlocked locks, corrupted aggregates. The failure is intermittent — it appears only when data grows past the schedule window.

**Detect:** Inspect crontabs and systemd timers for jobs with no lock acquisition. Grep for `pg_try_advisory_lock`, `flock`, or distributed locks; check Kubernetes CronJobs for `concurrencyPolicy: Forbid`.

**Bad:**
```bash
# if the 02:00 run spills past 03:00, two run at once
0 2 * * * /app/report.sh
```

**Good:**
```bash
0 2 * * * flock -n /run/report.lock /app/report.sh || \
  logger "report skipped: already running"
```

**References:** Kubernetes CronJob concurrencyPolicy docs, PostgreSQL advisory locks, CWE-662 Improper Synchronization

---

**Part of:** [database](../categories/database.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Dead Letter Queues

**MUST** route messages that exhaust retries to a monitored dead letter queue instead of silently discarding them.

**Why:** Dropped messages mean lost transactions, audit gaps, and undetected data corruption between services.

**Detect:** grep for `dead_letter`, `DLQ`, `x-dead-letter-exchange`, `maxReceiveCount`, `redrive`, `purge` in queue configs and consumer handlers.

**References:** OWASP ASVS 7.4, CWE-390, NIST SP 800-53 AU-9

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Exactly-Once Semantics

**MUST NOT** claim exactly-once delivery unless transactional produce/consume (or equivalent dedup store) is actually configured end to end.

**Why:** Marketing-level guarantees without transactions hide duplicates at the consumer boundary, corrupting financial and audit records.

**Detect:** grep for `exactly_once`, `isolation.level=read_committed`, `transactional.id`, then verify no non-transactional side effects (HTTP calls, DB writes) inside the transaction.

**References:** Kafka EOS docs, CWE-662, NIST SP 800-53 SI-7

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Idempotency (idempotency keys)

**MUST** accept a client-supplied idempotency key on non-idempotent operations and deduplicate replays before executing side effects.

**Why:** A retried charge or webhook without deduplication bills the customer twice and corrupts state no rollback cleanly undoes; retried requests, network timeouts, and scripted replays trigger refund cascades that erode customer trust.

**Detect:** Check POST endpoints for `Idempotency-Key` handling, `idempotency_key` unique constraint, dedupe cache; grep payment API routes and migration files for `dedupe`.

**References:** Stripe Idempotent Requests, draft-ietf-httpapi-idempotency-key, CWE-1394, AWS REL11-BP08, OWASP ASVS 14.3.3

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [resilience](../categories/resilience.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Job Age SLO

**MUST** track age of the oldest pending job as a first-class SLO with alerting, not merely queue count or throughput.

**Why:** A backlog of 100 items averaging 1 second looks healthy while one job waits 45 minutes — count-based metrics hide tail latency entirely.

**Detect:** grep dashboards/alerts for `oldest_job_age`, `job_age_seconds`, `head_of_line_blocking`; absence of max-age alerts alongside queue-depth alerts.

**References:** Google SRE Workbook tail latency, NIST SP 800-53 AU-6, SLI/SLO practice

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [observability](../categories/observability.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Kafka Consumer Groups

**MUST** assign each application a distinct consumer group ID; sharing one group between services silently splits the message stream.

**Why:** Two services sharing a group each receive a disjoint partition subset, so neither sees the full event feed — silent data loss.

**Detect:** grep configs for duplicated `group.id` values across services, hardcoded shared groups, `group.instance.id` collisions.

**References:** Kafka consumer group docs, CWE-664, OWASP ASVS 6.1

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Message Ordering

**SHOULD** preserve ordering only where required (per-key, not global) and document where reordering is tolerated; never assume FIFO across partitions.

**Why:** Out-of-order events corrupt state machines — a "cancel" processed before its "create" leaves orphaned records.

**Detect:** grep for `partition_key`, `ordering_key`, `enable.idempotence`, consumers processing multi-partition topics with order-dependent logic.

**References:** Kafka ordering guarantees, CWE-362, AWS SQS FIFO ordering notes

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Message Queues

**MUST** set queue depth limits, TTLs, and alerting thresholds; unbounded buffering hides downstream failure until memory or disk exhaustion.

**Why:** A queue that grows silently becomes a time bomb — messages expire or the broker crashes exactly when the backlog peaks.

**Detect:** grep broker configs for missing `max_length`, `message_ttl`, `max_memory`, `x-max-priority`; dashboards tracking only rate, not depth.

**References:** OWASP ASVS 7.4, CWE-770, RabbitMQ memory alarms docs

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Partition Keys

**SHOULD** choose partition keys with high cardinality and even distribution; low-cardinality or null keys hot-spot a single partition.

**Why:** A skewed key (e.g. tenant ID of one giant customer) overloads one broker and consumer while others idle, degrading throughput and latency SLOs.

**Detect:** grep producer code for `key=`, `partition_key`, constant or nullable keys; check broker metrics for per-partition byte imbalance.

**References:** Kafka partitioning docs, CWE-400, NIST SP 800-53 SC-5

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Payment Webhook Reconciliation

**SHOULD NOT** treat webhook payloads as authoritative until the signature is verified and the event is matched against a ledger entry.

**Why:** Unsigned or unreconciled webhooks let attackers forge payment confirmations and create phantom orders at zero cost.

**Detect:** check for `webhook_secret`, `stripe-signature`, `HMAC verify`, idempotency keys in webhook handler config and DB schema.

**References:** OWASP WSTG-ATHN-02, CWE-347, PCI DSS 4.0 Req 6.2, Stripe webhook signing guide

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [payments-fraud](../categories/payments-fraud.md) · [data](../domains/data.md) · [governance](../domains/governance.md) · [SKILL.md](../SKILL.md)

# Poison Messages

**MUST NOT** let a single malformed message crash or stall a consumer loop indefinitely; bound retries and eject it to quarantine.

**Why:** One crafted payload can halt an entire worker, turning a validation bug into a denial-of-service amplification vector.

**Detect:** grep consumer code for bare `except:` around handlers, missing `max_retries`, unbounded `while True: receive_message`, absent quarantine paths.

**References:** CWE-754, OWASP ASVS 5.1, AWS SQS poison pill guidance

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Priority Queues & Head-of-Line Blocking

**MUST NOT** let large or slow jobs block small/urgent ones on a shared queue; separate queues (or priority classes) for high-priority, fast, and bulk work.

**Why:** One huge job on a shared queue starves thousands of small requests — the classic unbounded-queue failure where latency grows without end until consumers never catch up.

**Detect:** grep for a single queue serving mixed job sizes; check for priority queue config (SQS FIFO priorities, Celery queues, RabbitMQ x-max-priority); review job-duration vs SLA mismatch.

**References:** AWS SQS priority patterns, RabbitMQ priority queues, DDIA queueing chapter

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Queue Depth and Consumer Lag Alerting

**MUST** page on queue depth and consumer lag thresholds so stalled processing is caught before data is lost or SLAs break.

**Why:** A stalled consumer (often from a poison message or credential expiry) silently accumulates backlog until the broker fills and producers block or messages drop.

**Detect:** grep alert rules for `rabbitmq_queue_messages_ready`, `kafka_consumergroup_lag`, `sqs ApproxAgeOfOldestMessage`; flag queues with no lag alert.

**References:** AWS SQS monitoring guide, RED/USE method, CWE-770, Google SRE Workbook

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [observability](../categories/observability.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Shared-Queue Tenant Isolation

**SHOULD** isolate tenant workloads in queues by partition, dedicated queue, or per-message tenant enforcement so one tenant's burst or poison message cannot starve or crash others.

**Why:** Shared queues turn noisy neighbors into outages and let a poison message from tenant A block tenant B's processing indefinitely.

**Detect:** check queue topology for tenant partitioning (Kafka partition key = tenant, per-tenant SQS), per-tenant rate limits on producers, DLQ handling segregated per tenant.

**References:** OWASP Multi-Tenant Security Guidance (queue isolation patterns), bulkheads pattern

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [multi-tenancy](../categories/multi-tenancy.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Webhook Replay Protection

**MUST NOT** rely on signatures alone for webhook authenticity; add timestamp windows and nonce deduplication to block valid-signature replays.

**Why:** A captured signed webhook stays replayable forever without expiry — an attacker resends a legitimate payment event days later undetected.

**Detect:** grep webhook receivers for missing `timestamp` validation, absent `nonce`/`event_id` dedup store, signature checks with no freshness window.

**References:** OWASP Webhook Security Best Practices, CWE-294, Stripe/GitHub webhook verification docs

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Webhook Signature Verification

**MUST** Verify the provider HMAC over the raw body with constant-time comparison before acting on any webhook.

**Why:** Unsigned endpoints accept forged events — fake payments, refunds, account changes.

**Detect:** Handlers with no signature check; `hmac.compare_digest` absent; verification skipped in dev branches.

**References:** CWE-347, CWE-208, Stripe/GitHub webhook signing docs

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [web-api-security](../categories/web-api-security.md) · [backend](../domains/backend.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

# Worker Pools

**SHOULD** size worker pools against queue arrival rates and set autoscaling bounds with starvation detection; undersized pools silently age jobs.

**Why:** A pool too small for peak load creates growing latency invisible until customers complain, while an oversized one wastes capacity and hides throughput regressions.

**Detect:** grep for `concurrency`, `pool_size`, `num_workers` without autoscaling policy; metrics showing queue depth rising while workers idle or saturated.

**References:** CWE-400, NIST SP 800-53 SC-5, Kubernetes HPA guidance

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [scaling-capacity](../categories/scaling-capacity.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)

# Workflow Engines

**MUST** keep durable workflow steps idempotent and side-effect-free at replay time, since Temporal/Step Functions re-execute steps after failure or recovery.

**Why:** Non-idempotent steps (emails, charges, HTTP POSTs) fire again on every replay, duplicating real-world effects across restarts.

**Detect:** grep workflow definitions for external calls outside activity/task wrappers, missing `idempotencyKey`, non-deterministic code (random, clock reads) inside workflow code.

**References:** Temporal determinism docs, AWS Step Functions error handling, CWE-662

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)

