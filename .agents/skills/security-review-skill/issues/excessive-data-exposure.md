---
categories: [api-design, compliance-privacy]
domains: [backend, governance]
---

# Excessive Data Exposure in API Serialization

**MUST NOT** serialize whole ORM/model objects to API responses; project an explicit DTO containing only intended fields.

**Why:** Returning full models leaks password hashes, internal IDs, and PII that the UI never asked for but every caller now receives.

**Detect:** `jsonify(user)` / `resp.json(model)` patterns; serializers without field allowlists; `password`/`ssn` keys in response bodies.

**References:** OWASP API3:2023, CWE-213
