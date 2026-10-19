---
categories: [database]
domains: [data]
---

# N+1 Queries

**MUST NOT** issue one query per row inside an application loop when a single batched query can fetch the same data.

**Why:** An endpoint that loads 200 parent records and lazily touches a relation per row fires 201 round trips; a modest page view becomes a database meltdown, and attackers deliberately hit such endpoints to exhaust connections.

**Detect:** ORM lazy-access patterns: `for x in items: x.author.name` in Django without `select_related`/`prefetch_related`; SQLAlchemy without `joinedload`/`selectinload`; Hibernate `FetchType.LAZY` traversed in controllers; `.include()` missing in Parse/GraphQL resolvers; count queries per request in logs (one SELECT repeated N times with varying IDs).

**Bad:**
```python
books = Book.objects.all()
for b in books:
    print(b.author.name)   # one SELECT per book
```

**Good:**
```python
books = Book.objects.select_related('author').all()
for b in books:
    print(b.author.name)   # single JOIN
```

**References:** Django ORM performance docs, nplusone (N+1 detection library), CWE-400
