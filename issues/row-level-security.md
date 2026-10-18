---
categories: [authorization-access-control]
domains: [backend]
---

# Row-Level Security

**MUST** enforce row-level security (RLS) or equivalent tenant scoping in the database layer for every multi-tenant table, not only in application queries.

**Why:** A single missed WHERE clause in one code path leaks every tenant's rows; database-enforced policies fail closed instead.

**Detect:** grep for `ENABLE ROW LEVEL SECURITY`, `CREATE POLICY`, tenant_id filters in ORM raw queries; flag tables lacking policies.

**References:** OWASP A01:2021 Broken Access Control, CWE-285, PostgreSQL RLS docs, NIST SP 800-53 AC-3

---

**Part of:** [authorization-access-control](../categories/authorization-access-control.md) · [backend](../domains/backend.md) · [SKILL.md](../SKILL.md)
