---
categories: [compliance-privacy, multi-tenancy]
domains: [backend, governance]
---

# Tenant Offboarding Data Purge

**MUST** provide a verified, complete tenant purge: primary stores, replicas, caches, search indexes, backups policy, analytics, and third-party processors — with attestation evidence.

**Why:** Offboarded tenant data lingering in a warehouse layer or search index is a compliance breach waiting to be discovered; "we deleted the account" rarely means everything.

**Detect:** review offboarding runbook/code for coverage list vs actual datastore inventory; check for orphaned tenant rows (`SELECT tenant_id ... GROUP BY` vs active tenants); verify purge verification step exists.

**References:** GDPR Art. 17, SOC2 CC6, OWASP Multi-Tenant Security Guidance
