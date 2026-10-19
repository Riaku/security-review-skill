---
categories: [database]
domains: [data]
---

# Deadlocks

**MUST** acquire locks on multiple resources in a consistent global order across all code paths, and retry deadlock aborts.

**Why:** Two transactions locking rows A and B in opposite orders will eventually deadlock; the database kills one, but without an idempotent retry users lose writes and queues jam. Timing-dependent, so they hide in testing and appear at peak traffic.

**Detect:** `deadlock detected` in DB logs (40P01/1213); transactions touching several tables in differing orders across services; updates inside loops over unordered result sets.

**Bad:**
```python
# service X: locks order then inventory
# service Y: locks inventory then order  -> circular wait
for item in items:
    inventory.decrement(item)
order.update(status='paid')
```

**Good:**
```python
with txn:
    lock_rows(sorted(table_names))   # every path locks in the same order
    ...
# plus: retry once on 40P01 / 1213
```

**References:** PostgreSQL Deadlock Detection docs, MySQL InnoDB deadlock docs, CWE-833
