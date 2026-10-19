---
categories: [database, distributed-systems]
domains: [data]
---

# ACID & Transactional Outbox

**MUST** rely on ACID guarantees only where the engine actually provides them; workflows spanning multiple stores MUST NOT assume cross-system atomicity, and domain changes along with their outbox events **MUST** be written in one atomic database transaction, never publishing before commit.

**Why:** ACID holds inside one database, not across a database plus a queue plus a third-party API. Treating "we use Postgres" as blanket safety leaves balances and event logs silently diverging whenever the second write fails after the first commits. Publishing outside the transaction causes phantom events on rollback or lost events on crash, corrupting downstream consumers.

**Detect:** A DB commit followed by a Kafka/queue publish with no outbox or saga pattern; no reconciliation job comparing stores; SQLite used for concurrent multi-writer workloads. Grep for `publish(` or `kafka.send` outside `@Transactional`/`BEGIN...COMMIT`; an outbox table missing `status`, `created_at`, or a relay poller is a gap.

**Bad:**
```python
db.commit()
kafka.publish("order-created", order)   # publish fails -> event lost forever
```

**Good:**
```python
with db.transaction():
    db.insert_order(order)
    outbox.enqueue("order-created", order)  # relay process publishes reliably
```

**References:** Kleppmann *DDIA* Ch. 7, Transactional Outbox pattern (Confluent), AWS Outbox Pattern, NIST SP 800-53 SI-7, CWE-662
