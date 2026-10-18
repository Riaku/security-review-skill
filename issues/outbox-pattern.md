---
categories: [distributed-systems]
domains: [data]
---

# Outbox Pattern

**MUST** write domain changes and their outbox events in one atomic database transaction, never publishing before commit.

**Why:** Publishing outside the transaction causes phantom events on rollback or lost events on crash, corrupting downstream consumers.

**Detect:** grep for `publish(` or `kafka.send` outside `@Transactional`/`BEGIN...COMMIT`; outbox table missing `status`, `created_at`, or relay poller queries.

**References:** CWE-662 Improper Synchronization, AWS Outbox Pattern, NIST SP 800-53 SI-7
