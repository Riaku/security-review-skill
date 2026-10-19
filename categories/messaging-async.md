# messaging-async

Queues, delivery semantics, workers, jobs.

## What this category covers

This category covers asynchronous work: messages moving through brokers and the consumers, workers, and jobs that process them. Its member items span queue mechanics (queue depth limits, dead-letter queues, poison messages, priority and head-of-line blocking, partition keys, consumer groups), delivery semantics (at-least-once, exactly-once, idempotency keys, ordering), worker and job lifecycle (pool sizing, background job limits, checkpoints, cron overlap, job-age SLOs), and inbound webhooks (signature verification, replay protection, payment reconciliation). A reviewer here should trace a message from publish to acknowledgment and ask what happens on redelivery, on failure, and on a burst that exceeds capacity. The recurring failure is an async path that is correct on the first attempt and wrong on the second: a consumer that double-charges on redelivery, or a stuck message that retries forever.

- Queue configuration: depth limits, TTLs, dead-letter routing, priority separation.
- Delivery semantics and idempotency: at-least-once vs exactly-once, dedup keys.
- Ordering and partitioning keys across partitions and consumer groups.
- Worker and job lifecycle: pool sizing, timeouts, checkpoints, cron single-runner locks.
- Inbound webhook handling: signature verification and replay protection.
- Backlog, lag, and job-age alerting during outages and catch-up.

## What it does not cover

- [distributed-systems](../categories/distributed-systems.md) — consensus, leader election, and cross-node agreement belong there; broker configuration and consumer delivery semantics belong here.
- [resilience](../categories/resilience.md) — timeouts, retries, backoff, and circuit breakers around failing dependencies belong there; what a redelivered message does to state belongs here.
- [observability](../categories/observability.md) — the logging, metrics, and tracing pipeline belongs there; which queue and job signals must page belongs here.
- [payments-fraud](../categories/payments-fraud.md) — the ledger and fraud logic themselves belong there; reconciling a provider's webhook against that ledger belongs here.

## What a finding here looks like

- a consumer that charges a card again when an already-processed message is redelivered.
- a malformed message that crashes the consumer loop and blocks the rest of the partition.
- a single shared queue where one tenant's burst starves every other tenant.
- a webhook acted on from its payload before the HMAC over the raw body is verified.
- a scheduled job still running when the next tick fires, with no single-runner lock.
