---
categories: [database]
domains: [data]
---

# UUIDs vs Auto-Increment

**SHOULD NOT** expose sequential auto-increment identifiers in public URLs or API payloads for resources whose existence or volume is sensitive.

**Why:** Integer IDs leak business information — `orders/1001` today and `orders/1101` tomorrow reveals daily volume — and invite enumeration and IDOR probing. Random UUIDs remove the guesswork, though they carry indexing costs.

**Detect:** Routes using `:id` backed by serial integers on sensitive resources; UUID v1 leaking MAC/timestamps where v4 or ULID fits better.

**Bad:**
```
GET /invoices/4821          # sequential: attacker walks 4822, 4823...
```

**Good:**
```
GET /invoices/9f2c7a4e-1b3d-4e5f-8a6b-c0d1e2f3a4b5   # UUIDv4, unguessable
-- still pair with authorization checks; obscurity is not access control
```

**References:** OWASP ASVS V3.2 / V4.2.1, RFC 4122 (UUID), PostgreSQL uuid vs bigserial notes, CWE-639

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
