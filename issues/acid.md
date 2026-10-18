---
categories: [database]
domains: [data]
---

# ACID

**MUST** rely on ACID guarantees only where the engine actually provides them; workflows spanning multiple stores MUST NOT assume cross-system atomicity.

**Why:** ACID holds inside one database, not across a database plus a queue plus a third-party API. Treating "we use Postgres" as blanket safety leaves balances and event logs silently diverging whenever the second write fails after the first commits.

**Detect:** A DB commit followed by a Kafka/queue publish with no outbox or saga pattern; no reconciliation job comparing stores; SQLite used for concurrent multi-writer workloads.

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

**References:** Kleppmann *DDIA* Ch. 7, Transactional Outbox pattern (Confluent), CWE-662

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
