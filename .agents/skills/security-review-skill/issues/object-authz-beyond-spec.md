---
categories: [authorization-access-control]
domains: [backend]
---

# Object Authorization Beyond Spec

**MUST** treat an API specification's security schemes as evidence of authentication only, and verify object-level authorization separately in code and tests.

**Why:** Schema languages describe shape and transport authentication only, so a spec that looks covered ships endpoints with no per-object ownership check at all.

**Detect:** list endpoints declared in the spec, then grep their handlers for an ownership or policy check on the referenced object.

**References:** Object authorization in web API specifications (arXiv 2212.06606), https://arxiv.org/abs/2212.06606
