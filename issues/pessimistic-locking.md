# Pessimistic Locking

**MAY** hold explicit row locks (`SELECT ... FOR UPDATE`) for hot contended resources, but only inside short transactions with a lock timeout configured.

**Why:** Pessimistic locks prevent lost updates on counters or seat inventory, yet a lock held across an external API call blocks every other writer — one slow dependency becomes a fleet-wide stall.

**Detect:** Audit what runs between `FOR UPDATE` acquisition and commit; missing `lock_timeout` / `NOWAIT`; locks spanning HTTP calls or user-input waits.

**Bad:**
```sql
SELECT * FROM seats WHERE id = 42 FOR UPDATE;
-- then the app calls the payment gateway... lock held for seconds
```

**Good:**
```sql
SET lock_timeout = '2s';
SELECT * FROM seats WHERE id = 42 FOR UPDATE NOWAIT;
-- payment happens after commit; reservation released fast
```

**References:** PostgreSQL SELECT FOR UPDATE docs, MySQL locking reads (InnoDB), CWE-662

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
