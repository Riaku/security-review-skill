# Queue Depth and Consumer Lag Alerting

**MUST** page on queue depth and consumer lag thresholds so stalled processing is caught before data is lost or SLAs break.

**Why:** A stalled consumer (often from a poison message or credential expiry) silently accumulates backlog until the broker fills and producers block or messages drop.

**Detect:** grep alert rules for `rabbitmq_queue_messages_ready`, `kafka_consumergroup_lag`, `sqs ApproxAgeOfOldestMessage`; flag queues with no lag alert.

**References:** AWS SQS monitoring guide, RED/USE method, CWE-770, Google SRE Workbook

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [observability](../categories/observability.md) · [data](../domains/data.md) · [reliability](../domains/reliability.md) · [SKILL.md](../SKILL.md)
