# EXPLAIN ANALYZE

**SHOULD** review `EXPLAIN ANALYZE` plans for every new hot query before merging, rather than trusting that an index exists in theory.

**Why:** Planners skip or misprice indexes when statistics are stale, types mismatch, or predicates are non-sargable; a query that looked fine in development can scan millions of rows in production.

**Detect:** Look for queries wrapping columns in functions (`LOWER(email) = ?`, `date(col) = ?`) which defeat indexes; check for implicit casts between int and varchar join keys; require plan output in PR descriptions for new list endpoints.

**Bad:**
```sql
SELECT * FROM users WHERE lower(email) = lower($1);  -- index on email unused
```

**Good:**
```sql
CREATE INDEX users_email_lower ON users (lower(email));
SELECT * FROM users WHERE lower(email) = lower($1);  -- index-only lookup
```

**References:** PostgreSQL EXPLAIN documentation, Use The Index Luke, OWASP ASVS V3.1, CWE-400
