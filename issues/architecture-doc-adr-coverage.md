---
categories: [documentation-quality, security-practices]
domains: [backend]
---

# Architecture Doc & ADR Coverage

**SHOULD** maintain a current architecture overview (components, data flow, trust boundaries) plus ADRs for settled design decisions, kept in the repo.

**Why:** Without a current overview, every reviewer and new engineer rebuilds the mental model from code — and without ADRs, settled decisions get re-litigated endlessly or silently violated by people who never knew they were settled.

**Detect:** check for architecture doc with a diagram covering current components (compare against actual services/dirs); check docs/adr/ (or equivalent) exists with dated, numbered records; flag overview last-updated far behind structural changes.

**References:** C4 model, ADR practice (Nygard)
