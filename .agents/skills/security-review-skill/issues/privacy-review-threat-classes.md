---
categories: [compliance-privacy]
domains: [governance]
---

# Privacy Review Threat Classes

**SHOULD** run a privacy review separate from the security review, covering surveillance, aggregation, secondary use and exclusion.

**Why:** Security review asks who can read the data; privacy review asks whether collecting it causes harm even when access control holds. Conflating them approves lawful but harmful designs.

**Detect:** Design docs under `docs/` with no privacy section naming surveillance, aggregation, secondary use and exclusion.

**References:** RFC 6973 Privacy Considerations, https://www.rfc-editor.org/rfc/rfc6973.txt
