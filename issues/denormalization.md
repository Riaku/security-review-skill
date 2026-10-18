# Denormalization

**SHOULD NOT** denormalize for read speed unless the write path maintaining the copies is explicitly designed, tested, and reconciled.

**Why:** Denormalization trades consistency for latency; without reliable propagation, derived copies drift, and dashboards, search indexes, and caches each tell a slightly different story.

**Detect:** Redundant columns updated from multiple code paths; aggregates like `user.total_spent` written by scattered `UPDATE`s instead of one event handler; no drift-check job in monitoring.

**Bad:**
```python
# three different services each do:
user.total_spent += order.total   # races, double-counts on retry
```

**Good:**
```python
# single writer consumes order events; idempotent upsert
upsert_user_stats(user_id, computed_from(order_events))  # replayable
```

**References:** Kleppmann *DDIA* Ch. 1, materialized view maintenance patterns, DynamoDB denormalization guide, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
