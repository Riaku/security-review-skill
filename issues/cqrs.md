# CQRS

**SHOULD** validate and authorize commands against the write model's current state, never trusting the read model's possibly stale projection for access control.

**Why:** A command approved on lagging read data can violate invariants or grant access the write side has since revoked, opening a TOCTOU window.

**Detect:** grep command handlers reading from read-store/query-side for authz, missing `expected_version`/optimistic concurrency on command, projection lag unbounded.

**References:** Fowler CQRS, Greg Young CQRS docs, CWE-367 Time-of-Check Time-of-Use
