# Async Writes (ack now, persist later)

**MAY** acknowledge a request before durable persistence, but only when the durability gap is explicit and backed by a durable queue or WAL — never a bare in-memory buffer.

**Why:** Acking before persisting trades durability for latency: a crash with buffered writes and no durable log leaves the client told "saved" for data that never existed.

**Detect:** Trace the ack point relative to persistence: does the handler return 2xx before the enqueue is fsynced (Kafka `acks=all`, Redis AOF `everysec` vs `no`)? Grep for flusher threads with no crash-recovery path or backlog alerting.

**Bad:**
```python
buffer.append(event)
return {"status": "ok"}   # crash = events gone, client told saved
```

**Good:**
```python
producer.send(topic, event).get(timeout=5)  # acks=all first
return {"status": "ok"}
```

**References:** Kafka semantics docs (acks, idempotent producer), Redis AOF persistence docs, Arjay McCandless cheat sheet
