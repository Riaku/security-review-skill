---
categories: [testing-strategy]
domains: [backend]
---

# Contract Testing

**MUST** verify service-to-service API contracts (request/response schemas, auth headers) so a producer change cannot silently break consumer security assumptions.

**Why:** Undeclared schema drift lets unauthenticated or malformed payloads cross trust boundaries without detection.

**Detect:** Pact consumer/provider specs, OpenAPI schema validation in CI (`schemathesis`, `dredd`), missing contract checks on internal REST/gRPC services.

**References:** OWASP API Security Top 10 API2, CWE-20, NIST SP 800-218 (SSDF)
