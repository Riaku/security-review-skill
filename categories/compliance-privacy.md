# compliance-privacy

Privacy operations and data protection in code.

## What this category covers

The class of problems here is privacy and data-protection obligations as they must be implemented in code and operations, not stated as policy. Items span data-subject rights and regional privacy statutes, retention and erasure across every copy of the data, classification and lineage for personal data, residency and cross-border transfer, redaction of PII from logs and outbound payloads, and the access governance and audit evidence that back those controls. A reviewer should expect to find PII handling paths, retention and deletion jobs, consent gates, export and delete endpoints, and the access-review and audit artifacts a regulator samples. The category is the home for obligations discharged by code or running controls; the certification programs that certify them live elsewhere.

- Data-subject rights and regional privacy statutes — access, deletion, portability, consent, and age assurance across jurisdictions (GDPR, CCPA/CPRA, China PIPL, India DPDP, Brazil LGPD, HIPAA, COPPA and the UK Online Safety Act).
- Retention, erasure, and offboarding — deletion pipelines that propagate to replicas, caches, search indexes, analytics, and backups, plus tenant purge with attestation.
- Classification, lineage, and residency — tagging PII at creation, tracking its flow through warehouse layers, and keeping it inside mandated geographic boundaries.
- Redaction and leakage control — logs, notebook outputs, API serialization, serverless container reuse, and payloads sent to third-party LLM APIs.
- Audit evidence and access governance — audit trails, object-level access logging, privileged-action attribution, JIT and break-glass access, and offboarding and role-change revocation.
- Audit regimes and third-party accountability — SOC 2 evidence collection, PCI DSS card-data prohibitions, NYDFS cyber requirements, vendor and subprocessor registers, and third-party license tracking.
- Consent-scoped client capture and disclosure — session replay and input recording gated on consent with capture-time field masking, and visitor IP or user-agent disclosure to third-party font and CDN hosts.

## What it does not cover

- [regulatory-frameworks](../categories/regulatory-frameworks.md) — certification programs, control catalogues, and cross-jurisdiction regimes (ISO 27001 ISMS, NIST CSF and SP 800-53, FedRAMP, CMMC) belong there; this category carries the privacy obligations themselves as implemented.
- [multi-tenancy](../categories/multi-tenancy.md) — per-tenant isolation mechanics such as tenant-id binding, cache-key partitioning, and shared-queue separation belong there; the tenant purge obligation lives here.
- [data-pipelines](../categories/data-pipelines.md) — pipeline immutability, backfills, and version pinning belong there; how PII is classified and traced through warehouses lives here.
- [third-party-integrations](../categories/third-party-integrations.md) — OAuth scope minimization, integration credential sprawl, and SaaS webhook consumer trust belong there; vendor risk registers and subprocessor terms live here.

## What a finding here looks like

- A delete-user endpoint that clears the primary table but leaves the row in a search index, analytics replica, or export bucket.
- Request logging that writes full bodies, tokens, or personal-data fields to disk or an aggregator with no redaction.
- A "Do Not Sell" or consent control with no backend enforcement, so opt-outs never reach the data stores.
- Non-essential cookies or tracking pixels initialized before the consent check runs.
- A serverless handler that caches request-derived customer data in module-level state a later invocation can read.
- A web font or library hot-linked from a third-party CDN, disclosing every visitor's IP address to that host.
- A session-replay SDK initializing before the consent check, or capturing password and payment fields unmasked.
