---
categories: [api-design]
domains: [backend]
---

# OpenAPI Specs

**MUST** validate incoming requests against the OpenAPI schema at the edge; the spec is enforcement, not just documentation.

**Why:** Docs-only specs let malformed or malicious payloads reach handlers that assume validated shapes, enabling injection and mass-assignment.

**Detect:** spec files present but no `openapi-validator`/`schemathesis` middleware; handlers ignoring `request.body` schema checks.

**References:** OWASP API3:2023, CWE-915, Schemathesis docs
