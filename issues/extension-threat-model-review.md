---
categories: [api-design]
domains: [backend]
---

# Extension Threat Review

**MUST** re-check every new use case or extension against the threat model the design was reviewed under before shipping it.

**Why:** An extension inherits the old guarantees without inheriting the assumptions that produced them, converting a reviewed design into an unreviewed one.

**Detect:** List the shipped extensions and confirm each has a threat-model entry dated after the extension.

**References:** NCSC Protocol Design Principles, https://www.ncsc.gov.uk/sites/default/files/2026-06/Protocol-Design-Principles.pdf
