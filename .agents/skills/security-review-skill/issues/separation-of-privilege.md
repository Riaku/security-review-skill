---
categories: [authorization-access-control]
domains: [backend]
---

# Separation of Privilege

**MUST** require two independent conditions, such as a permission plus a second approval or factor, before any destructive or high-value operation.

**Why:** A single check that is buggy, phished, or over-granted hands over the whole operation; independent conditions fail independently.

**Detect:** grep destructive handlers (`delete`, `transfer`, `refund`, `role`, `key`) guarded only by one `is_admin`/`has_role` call, with no approval or step-up call nearby.

**References:** Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563
