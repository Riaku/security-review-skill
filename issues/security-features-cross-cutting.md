---
categories: [security-practices]
domains: [backend]
---

# Security Is Cross-Cutting

**MUST** review every call site of an access-control decision in the change, not only the module that appears to own it.

**Why:** Access control and auth logic scatter through the codebase and interleave, so a review confined to the security package misses most of the code that decides access.

**Detect:** judgment — trace each security feature's call sites and integration glue (`authorize`, `can?`, `has_permission`, policy checks) across the diff, not only the security module.

**References:** Mining security features as cross-cutting concerns, https://arxiv.org/abs/2610.06132
