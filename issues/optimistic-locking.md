---
categories: [database]
domains: [data]
---

# Optimistic Locking

**SHOULD** use optimistic concurrency control (version or ETag column) for user-facing edits where concurrent modification is possible but rare.

**Why:** Without a version check, two admins editing the same record produce a silent lost update — last write wins and the first change vanishes with no error. A version column turns that collision into a detectable conflict.

**Detect:** UPDATEs over user-editable rows with no `WHERE version = :expected` guard; ORMs not configured for `optimistic_locking`; APIs accepting full-object PUTs with no ETag/If-Match header.

**Bad:**
```sql
UPDATE docs SET body = :new_body WHERE id = :id;  -- clobbers concurrent edit
```

**Good:**
```sql
UPDATE docs SET body = :new_body, version = version + 1
WHERE id = :id AND version = :expected;
-- 0 rows affected => conflict, tell the user
```

**References:** Hibernate `@Version` docs, Rails `lock_version`, RFC 7232 If-Match, CWE-362
