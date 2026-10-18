# Priority Queues & Head-of-Line Blocking

**MUST NOT** let large or slow jobs block small/urgent ones on a shared queue; separate queues (or priority classes) for high-priority, fast, and bulk work.

**Why:** One huge job on a shared queue starves thousands of small requests — the classic unbounded-queue failure where latency grows without end until consumers never catch up.

**Detect:** grep for a single queue serving mixed job sizes; check for priority queue config (SQS FIFO priorities, Celery queues, RabbitMQ x-max-priority); review job-duration vs SLA mismatch.

**References:** AWS SQS priority patterns, RabbitMQ priority queues, DDIA queueing chapter

---

**Part of:** [messaging-async](../categories/messaging-async.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
