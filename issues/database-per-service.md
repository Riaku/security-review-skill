# Database per Service

**SHOULD** give each service its own datastore and schema, accessed only through that service's API; **SHOULD NOT** let multiple services share a database instance or read each other's tables directly.

**Why:** Shared connection strings and cross-service table queries create hidden coupling — a schema change breaks unknown consumers — and widen the blast radius: one service's compromise or buggy migration can read or write another service's data, bypassing its authorization layer entirely.

**Detect:** identical DB connection strings across service repos; direct SQL against another service's tables; shared schema grants; cross-service joins in query code or reporting jobs.

**References:** martinfowler.com/articles/microservices.html (Decentralized Data Management), Martin Fowler Patterns of Enterprise Application Architecture (Shared Database anti-pattern)
