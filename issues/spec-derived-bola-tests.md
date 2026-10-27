---
categories: [authorization-access-control]
domains: [backend]
---

# Spec-Derived Authorization Tests

**MUST** generate object-level authorization tests from the API specification, crossing each identity with every object identifier it must not reach.

**Why:** Reviewers cannot reliably remember which endpoints own objects, so unscoped lookups pass review and surface only when one customer reads another's record.

**Detect:** command generate cases from the OpenAPI spec (`schemathesis`) pairing token A with object IDs owned by B, and fail on any 2xx.

**References:** OWASP API1:2023 Broken Object Level Authorization, Spec-driven IDOR/BOLA test generation, https://arxiv.org/abs/2201.10833, CWE-639 (Authorization Bypass Through User-Controlled Key)
