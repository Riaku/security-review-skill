---
categories: [resilience]
domains: [backend]
---

# Per-Request Resource Budgets

**MUST** set explicit per-request ceilings on CPU time, memory, file descriptors, connections, and threads so one caller cannot exhaust shared capacity.

**Why:** Unbounded consumption by a single request is denial of service for every other user of the same process.

**Detect:** grep server and handler config for `timeout`, `max_connections`, `memory_limit`, `ulimit`, `worker` ceilings and unbounded `while`/queue reads on request-driven paths.

**References:** OWASP API4:2023 Unrestricted Resource Consumption, OWASP Denial of Service Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html
