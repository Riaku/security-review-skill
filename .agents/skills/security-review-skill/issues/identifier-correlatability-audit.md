---
categories: [compliance-privacy]
domains: [governance]
---

# Identifier Correlatability Audit

**SHOULD** audit every identifier a design emits for what it links, and drop or weaken identifiers that are not required.

**Why:** Individual identifiers look harmless; together they join activity across time, devices and contexts into a profile nobody consented to. Traffic metadata identifies users even with no identifier in the payload.

**Detect:** List every emitted identifier and metadata signal (IDs, timestamps, ordering, TLS quirks) and record what each one links.

**References:** RFC 6973 Privacy Considerations, https://www.rfc-editor.org/rfc/rfc6973.txt
