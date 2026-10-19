---
categories: [authorization-access-control]
domains: [backend]
---

# Field-Level Authorization

**MUST** enforce read and write authorization per field, including rules that depend on the object's current state.

**Why:** Object-level checks let a caller who may read a record also read or write the fields reserved for another role or for a later stage.

**Detect:** grep serializers and update handlers for object-level-only checks and for a per-field policy map keyed by state.

**References:** OWASP ASVS v5.0 V8, https://github.com/OWASP/ASVS/blob/master/5.0/en/0x17-V8-Authorization.md, CWE-863
