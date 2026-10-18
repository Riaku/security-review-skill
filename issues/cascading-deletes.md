# Cascading Deletes

**SHOULD NOT** use `ON DELETE CASCADE` on chains of tables holding financial, audit, or otherwise irreplaceable data.

**Why:** One careless delete of a parent row — a test account, a "leftover" tenant — silently erases an entire subtree: orders, payments, audit trails. The cascade executes exactly as designed; backups become the only recovery.

**Detect:** Schema grep for `ON DELETE CASCADE`, especially nested several levels deep; delete endpoints with no dry-run; absence of `RESTRICT` where children must survive.

**Bad:**
```sql
CREATE TABLE orders (id INT, user_id INT REFERENCES users(id) ON DELETE CASCADE);
CREATE TABLE payments (order_id INT REFERENCES orders(id) ON DELETE CASCADE);
-- DELETE user -> orders -> payments: audit trail gone
```

**Good:**
```sql
REFERENCES users(id) ON DELETE RESTRICT  -- force explicit, reviewed cleanup
```

**References:** PostgreSQL ON DELETE actions, OWASP ASVS V6.4 (data retention), CWE-459

---

**Part of:** [database](../categories/database.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
