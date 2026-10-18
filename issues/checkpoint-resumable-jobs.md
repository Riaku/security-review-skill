---
categories: [database, messaging-async]
domains: [data]
---

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
