# Read Replicas

**MUST** route write-critical reads to the primary and reserve replicas for traffic that tolerates staleness; never send a read-your-own-write query to a replica.

**Why:** Replicas lag by definition. A user who saves a profile and is routed to a replica sees the old data, concludes the save failed, and retries — duplicating records. Auth checks on replicas can honor revoked state for the lag window.

**Detect:** Read/write splitting config audited per query; INSERT-then-SELECT hitting a replica; permission lookups on replicas with no "primary after write" rule.

**Bad:**
```python
db.primary.create_order(o)
return db.replica.get_order(o.id)   # replica may not have it yet
```

**Good:**
```python
db.primary.create_order(o)
return db.primary.get_order(o.id)   # read-your-writes on primary
# analytics and reports go to replicas
```

**References:** PostgreSQL Hot Standby docs, AWS RDS replica lag guidance, Kleppmann *DDIA* Ch. 5, CWE-362
