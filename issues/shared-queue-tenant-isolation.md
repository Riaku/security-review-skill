# Shared-Queue Tenant Isolation

**SHOULD** isolate tenant workloads in queues by partition, dedicated queue, or per-message tenant enforcement so one tenant's burst or poison message cannot starve or crash others.

**Why:** Shared queues turn noisy neighbors into outages and let a poison message from tenant A block tenant B's processing indefinitely.

**Detect:** check queue topology for tenant partitioning (Kafka partition key = tenant, per-tenant SQS), per-tenant rate limits on producers, DLQ handling segregated per tenant.

**References:** OWASP Multi-Tenant Security Guidance (queue isolation patterns), bulkheads pattern
