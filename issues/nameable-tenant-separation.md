---
categories: [multi-tenancy]
domains: [backend, infrastructure]
---

# Nameable Tenant Separation

**MUST** document, for every shared store, cache, queue, and search index, the mechanism that enforces tenant isolation and whether it is inherited or implemented.

**Why:** A boundary nobody can describe cannot be assessed, and inherited isolation is exactly where nested services quietly assume someone else's guarantee.

**Detect:** For each shared store, cache, queue, and search index, read the isolation design and confirm a named mechanism per layer.

**References:** NCSC Cloud Security Principles, https://www.ncsc.gov.uk/collection/cloud/the-cloud-security-principles
