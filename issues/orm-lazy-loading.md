---
categories: [database]
domains: [data]
---

# ORM Lazy Loading

**SHOULD NOT** rely on lazy-loaded relationships inside request handlers or loops; fetch required associations eagerly or via explicit joins.

**Why:** Lazy loading turns one query into N+1: every iteration fires a fresh round trip, multiplying latency and connection pressure. An attacker who controls collection size can make a single request saturate the database — a cheap denial-of-service amplifier.

**Detect:** Grep for SQLAlchemy without `joinedload`/`selectinload`, Hibernate `FetchType.LAZY` traversed in controllers, Django template loops missing `select_related`/`prefetch_related`. Check query logs for repeated identical SELECTs under one request ID.

**Bad:**
```python
for order in session.query(Order).all():
    print(order.customer.email)  # one SELECT per order
```

**Good:**
```python
orders = session.query(Order).options(
    joinedload(Order.customer)).all()
for order in orders:
    print(order.customer.email)  # single joined query
```

**References:** OWASP ORM cautions in SQLi prevention cheat sheet, CWE-400, Hibernate N+1 docs, SQLAlchemy eager loading docs

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
