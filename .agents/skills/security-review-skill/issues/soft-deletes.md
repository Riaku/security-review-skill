---
categories: [database]
domains: [data]
---

# Soft Deletes

**MUST** filter soft-deleted rows (`deleted_at IS NULL`) in every query path, and enforce that filter centrally rather than per-call.

**Why:** A tombstone column only hides data if every reader honors it; one forgotten predicate leaks "deleted" records into search results or exports — a privacy incident when the row held data a user asked to erase.

**Detect:** Audit each query against `deleted_at`/`is_deleted` tables; check whether the ORM applies a default scope or every call site repeats the condition by hand; inconsistent unique indexes over deleted rows.

**Bad:**
```python
User.query.all()   # includes users who requested deletion
```

**Good:**
```python
class UserQuery(db.Query):
    def all(self):
        return self.filter(User.deleted_at.is_(None)).all()  # default scope
```

**References:** OWASP ASVS 4.0.3 V8.3.8 (data retention), Rails default_scope docs, PostgreSQL Row Security, CWE-459
