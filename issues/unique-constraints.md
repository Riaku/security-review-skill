---
categories: [database]
domains: [data]
---

# Unique Constraints

**MUST** enforce business-level uniqueness (email, username, SKU per tenant) with database UNIQUE constraints, not just a pre-insert existence check in code.

**Why:** A "check if absent, then insert" sequence is a race: two concurrent requests both pass and both insert, creating duplicate accounts that break login, billing, and support flows. Only the database can arbitrate atomically.

**Detect:** Existence-check-then-create patterns without a unique index behind them; login by email on a table lacking `UNIQUE(email)`; multi-tenant tables missing `UNIQUE(tenant_id, sku)`.

**Bad:**
```python
if not User.query.filter_by(email=e).first():
    db.add(User(email=e))   # two requests, two users, same email
```

**Good:**
```sql
CREATE UNIQUE INDEX users_email_uniq ON users (email);
-- races resolve: one wins, one gets a violation to handle
```

**References:** SQL UNIQUE constraint, OWASP ASVS V3.2, Rails uniqueness-validation index caveat, CWE-362

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
