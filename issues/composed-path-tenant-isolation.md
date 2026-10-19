---
categories: [multi-tenancy]
domains: [backend]
---

# Composed-Path Tenant Isolation

**MUST** test tenant isolation end-to-end through every intermediary fronting a service, because shared gateway credentials can collapse per-tenant cache and quota isolation the backend believes it enforces.

**Why:** Each component can be correctly isolated and the composed path still shared, when a gateway authenticates every tenant with one upstream identity.

**Detect:** curl the same object as two tenants through the gateway and diff status and body for cache bleed

**References:** CacheProbe, https://arxiv.org/abs/2605.30613
