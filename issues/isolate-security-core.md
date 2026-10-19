---
categories: [security-practices]
domains: [backend]
---

# Isolate the Security Core

**MUST** isolate the code that must always be correct into a small, separately owned component with its own review and tests.

**Why:** High assurance is only achievable for code small enough to audit exhaustively; authorization smeared across services makes every service part of the trusted base.

**Detect:** judgment: the auth/authz module and its callers — list every service that makes its own trust decision instead of delegating to the core.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563
