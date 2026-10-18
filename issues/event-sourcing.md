# Event Sourcing

**MUST** make stored events immutable and append-only, with schema-versioned payloads and cryptographic integrity checks on the event log.

**Why:** Mutable or unsigned events let an attacker rewrite history to forge balances or erase audit trails, destroying the ledger's trustworthiness.

**Detect:** grep for UPDATE/DELETE on events table, missing `event_version`/`schema_version`, no hash/signature chaining (`prev_hash`), events deserialized without version dispatch.

**References:** Fowler Event Sourcing, Greg Young versioning, CWE-393, NIST SP 800-53 AU-9

---

**Part of:** [distributed-systems](../categories/distributed-systems.md) · [data](../domains/data.md) · [SKILL.md](../SKILL.md)
