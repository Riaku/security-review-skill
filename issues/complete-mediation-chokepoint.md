---
categories: [authorization-access-control]
domains: [backend]
---

# Complete Mediation at a Chokepoint

**MUST** route every access to every resource through one enforcement point that no request path can bypass.

**Why:** An attacker simply takes the unchecked path, so a control enforced on most routes is equivalent to no control at all.

**Detect:** grep handlers that fetch a record (`findById(`, `get_object_or_404(`, raw `SELECT`) with no `authorize(`, `can(`, or policy call in the same function.

**References:** OWASP Access Control Cheat Sheet, https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html, Saltzer & Schroeder, The Protection of Information in Computer Systems (1975), https://web.archive.org/web/2023/https://dl.acm.org/doi/10.1145/359545.359563
