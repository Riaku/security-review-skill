---
categories: [database]
domains: [data]
---

# Transactions

**SHOULD** wrap multi-statement writes that must all succeed together in a single database transaction, and keep those transactions short.

**Why:** Without atomicity a crash between statements leaves half-applied state — money debited but not credited. Long transactions are equally dangerous: they hold row locks across network calls, inviting contention and timeouts.

**Detect:** Consecutive writes outside `BEGIN/COMMIT` or a session context manager; `autocommit=True` around paired writes; HTTP or external API calls made inside an open transaction block.

**Bad:**
```python
conn.execute("UPDATE accounts SET bal = bal - 100 WHERE id = 1")
call_external_api()   # crash here = lost debit
conn.execute("UPDATE accounts SET bal = bal + 100 WHERE id = 2")
```

**Good:**
```python
with conn.transaction():
    conn.execute("UPDATE accounts SET bal = bal - 100 WHERE id = 1")
    conn.execute("UPDATE accounts SET bal = bal + 100 WHERE id = 2")
# external call moved outside the lock window
```

**References:** PostgreSQL Transactions docs, MySQL InnoDB Transaction Model, CWE-662
